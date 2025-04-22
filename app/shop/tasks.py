import base64
import json
import os
import re
import shutil
from typing import Any

import requests
from celery import shared_task
from django.conf import settings
from django.core.files import File
from django.core.paginator import Paginator
from django.db.models import OuterRef, Subquery
from django.test import RequestFactory
from django.utils import timezone
from openai import OpenAI
from salesman.core.utils import get_salesman_model

from shop.email_notifications import (
    send_basket_notification,
    send_new_images_notification,
)
from shop.models import (
    ImageCategory,
    ImageOrientation,
    ImageProduct,
    OpenAISettings,
    SubscriptionPlan,
)

SYSTEM_PROMPT = 'You are an assistant that analyzes images and returns responses in JSON format only. The response must include three keys: "name" should be a 1-5 word name of the image in Hebrew, "orientation", "tags", and "description."name" "orientation" must be chosen from the provided list. "tags" should be 5-10 keywords in Hebrew separated by commas. "description" should be a 20-40 word description of the image in Hebrew. Do not add any additional information or comments.'
PROMPT = 'Analyze the image and provide the response in JSON format. The response must include the following keys: "name", "orientation", "tags", and "description". 1) "name" should be a 1-5 word name of the image in Hebrew, 2) "orientation" must be one of {orientations}. 3) "tags" should be 5-10 keywords in Hebrew separated by commas. 4) "description" must be a 20-40 word description of the image in Hebrew.'


@shared_task
def check_unpaid_basket() -> None:
    today = timezone.now().date()

    filtered_baskets = get_salesman_model('Basket').objects.filter(date_updated__date__lte=today)
    latest_basket_per_user = filtered_baskets.filter(
        user=OuterRef('user'),
        date_updated__date=Subquery(
            filtered_baskets.filter(
                user=OuterRef('user'),
            ).order_by('-date_updated').values('date_updated__date')[:1],
        ),
    )
    baskets = get_salesman_model('Basket').objects.filter(id__in=Subquery(latest_basket_per_user.values('id')),
                                                          ).order_by('user', '-date_updated').distinct('user')
    for basket in baskets:
        if basket.count > 0:
            send_basket_notification(basket)


@shared_task
def checkout_ZCreditPayment(url: str) -> None:  # noqa: N802
    requests.get(url, timeout=10)


@shared_task(bind=True)
def request_images_info(self: Any, images_info_file: str) -> None:
    def image_to_str(path_to_image: str) -> str:
        with open(path_to_image, 'rb') as image_file:
            print(path_to_image)
            return base64.b64encode(image_file.read()).decode('utf-8')

    request = RequestFactory().get('/')
    open_ai_settings = OpenAISettings.load(request_or_site=request)
    with open(os.path.join(settings.MEDIA_ROOT, images_info_file), encoding='utf-8') as file:
        images_info = json.loads(file.read())

    client = OpenAI(api_key=open_ai_settings.openai_api_key)
    paginator = Paginator(images_info, 20)

    self.update_state(
            state='PROGRESS',
            meta={'current': 0, 'total': paginator.num_pages},
        )

    for page_number in range(1, paginator.num_pages + 1):
        for image_index, image in enumerate(paginator.page(page_number).object_list):
            img_format = os.path.splitext(image['source'])[1]
            img_b64_str = image_to_str(image['source'])
            response = client.chat.completions.create(
                model='gpt-4o-mini',
                messages=[
                    {
                        'role': 'system',
                        'content': [{'type': 'text', 'text': SYSTEM_PROMPT}],
                    },
                    {
                        'role': 'user',
                        'content': [
                            {'type': 'text', 'text': PROMPT.format(orientations=[orientation.slug for orientation in ImageOrientation.objects.filter(available=True)])},
                            {
                                'type': 'image_url',
                                'image_url': {
                                    'url': f'data:image/{img_format};base64,{img_b64_str}',
                                },
                            },
                        ],
                    },
                ],
            )
            if response.choices[0].finish_reason == 'stop':
                match = re.search(r"{.*?}", response.choices[0].message.content, re.DOTALL)
                try:
                    image_info = json.loads(match.group(0))
                    images_info[(page_number - 1) * 20 + image_index]['name'] = image_info['name']
                    images_info[(page_number - 1) * 20 + image_index]['orientation'] = image_info['orientation']
                    images_info[(page_number - 1) * 20 + image_index]['tags'] = image_info['tags']
                    images_info[(page_number - 1) * 20 + image_index]['description'] = image_info['description']
                except Exception:
                    pass

        with open(os.path.join(settings.MEDIA_ROOT, images_info_file), 'w', encoding='utf-8') as file:
            file.write(json.dumps(images_info))

        self.update_state(
            state='PROGRESS',
            meta={'current': page_number, 'total': paginator.num_pages},
        )


@shared_task(bind=True)
def save_images(self: Any, images_info_file: str) -> None:
    new_images = []

    with open(os.path.join(settings.MEDIA_ROOT, images_info_file), encoding='utf-8') as file:
        images_info = json.loads(file.read())

    try:
        for image_index, image in enumerate(images_info):

            image_product = ImageProduct(
                name=image['name'],
                price=float(image['price'].replace(',', '.')),
                premium=image['selling_option'] == 'premium',
                description=image['description'],
            )

            with open(image['source'], 'rb') as file:
                image_product.image.save(os.path.split(image['source'])[1], File(file))

            if ImageOrientation.objects.filter(slug=image['orientation']).exists():
                image_product.orientation = ImageOrientation.objects.get(slug=image['orientation'])

            if ImageCategory.objects.filter(slug=image['category']).exists():
                image_product.category = ImageCategory.objects.get(slug=image['category'])

            image_product.save()

            for tag in image['tags'].split(','):
                image_product.tags.add(tag.strip())

            if image['selling_option'] == 'subscription':
                image_product.subscription_plans.set(SubscriptionPlan.objects.all())
            else:
                new_images.append(image_product.id)

            self.update_state(
                state='PROGRESS',
                meta={'current': image_index, 'total': len(images_info)},
            )

        send_new_images_notification(new_images[:20])

    except Exception:
        pass

    shutil.rmtree(os.path.join(settings.MEDIA_ROOT, images_info_file.replace('.json', '')))
    os.remove(os.path.join(settings.MEDIA_ROOT, images_info_file))
