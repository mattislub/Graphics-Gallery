import json
import os
import re
import tempfile
import urllib.parse
import uuid
import zipfile

from celery.result import AsyncResult  # type: ignore
from core.models import (
    Newsletter,
    Wishlist,
)
from django.conf import settings  # type: ignore
from django.contrib.auth.decorators import login_required  # type: ignore
from django.contrib.contenttypes.models import ContentType  # type: ignore
from django.core.paginator import Paginator
from django.db.models import (  # type: ignore
    Q,
    QuerySet,
    Sum,
)
from django.http import (  # type: ignore
    FileResponse,
    Http404,
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import (  # type: ignore
    redirect,
    render,
)
from django.utils.translation import gettext_lazy as _  # type: ignore
from pages.templatetags.pages import get_url_by_page_name
from PIL import Image  # type: ignore
from salesman.checkout.payment import PaymentError  # type: ignore
from salesman.core.utils import get_salesman_model  # type: ignore
from wagtail.admin.views.reports import ReportView  # type: ignore

from shop.forms import EarningFilterForm
from shop.models import (
    BalanceProduct,
    ImageCategory,
    ImageOrientation,
    ImageProduct,
    SubscriptionPlan,
    UserSubscription,
)
from shop.payments import BalancePayment, ZCreditPayment
from shop.tasks import request_images_info, save_images


def quick_purchase(request: HttpRequest) -> JsonResponse:
    if request.method == 'POST':
        current_basket, _ = get_salesman_model('Basket').objects.get_or_create_from_request(request)

        product_code = request.POST.get('product_code')
        product = ImageProduct.objects.get(id=int(product_code[1:]))

        for basket_item in current_basket.items.all():
            if basket_item.product.code == product_code:
                basket_item.delete()

        size = request.POST.get('size', None)
        email = request.POST.get('email', '')
        payment_method = request.POST.get('payment_method', None)

        basket = get_salesman_model('Basket').objects.create(
            user=request.user if request.user.is_authenticated else None,
            extra={'email': request.user.email if request.user.is_authenticated else email},
        )
        basket.add(
            product=product,
            quantity=1,
            ref=None,
            extra={'size': size} if size is not None else {},
        )
        basket.update(request)

        if payment_method == 'balance-payment':
            payment = BalancePayment()
        elif payment_method == 'zcredit-payment':
            payment = ZCreditPayment()

        try:
            return JsonResponse({'Content-Type': 'text/html; charset=utf-8', 'Location': payment.basket_payment(basket, request).url}, status=201)
        except PaymentError as error:
            return JsonResponse({'detail': str(error)}, status=402)

    raise Http404


def api_wishlist(request: HttpRequest, code: str) -> HttpResponse:
    if request.user.is_authenticated:
        user_wishlist = Wishlist.objects.get(user=request.user)
        product = ImageProduct.objects.get(id=int(code[1:]))

        if request.method == 'POST':
            if product not in user_wishlist.images.all():
                user_wishlist.images.add(product)
                return HttpResponse(status=201)

        elif request.method == 'DELETE':
            user_wishlist.images.remove(product)
            return HttpResponse(status=204)

    return HttpResponse(status=404)


@login_required
def replenish_balance(request: HttpResponse) -> HttpResponseRedirect:
    balance_product_id = request.POST.get('balance_product_id')
    balance = BalanceProduct.objects.get(id=int(balance_product_id))

    content_type = ContentType.objects.get_for_model(BalanceProduct)
    product = content_type.get_object_for_this_type(id=balance.id)
    basket = get_salesman_model('Basket').objects.create(
        user=request.user,
        extra={'email': request.user.email},
    )

    basket.add(
        product=product,
        quantity=1,
        ref=None,
    )
    basket.extra['is_replenishment'] = True
    basket.update(request)
    zcredit_payment = ZCreditPayment()

    return zcredit_payment.basket_payment(basket, request)


@login_required
def purchase_subscription(request: HttpRequest) -> HttpResponseRedirect:
    subscription_plan_id = request.POST.get('subscription_plan_id')
    subscription_plan = SubscriptionPlan.objects.get(id=int(subscription_plan_id))

    content_type = ContentType.objects.get_for_model(SubscriptionPlan)
    product = content_type.get_object_for_this_type(id=subscription_plan.id)
    basket = get_salesman_model('Basket').objects.create(
        user=request.user,
        extra={'email': request.user.email},
    )

    basket.add(
        product=product,
        quantity=1,
        ref=None,
    )
    basket.extra['is_purchasing_subscription'] = True
    basket.update(request)
    zcredit_payment = ZCreditPayment()

    return zcredit_payment.basket_payment(basket, request)


def download(request: HttpRequest, token: str) -> FileResponse:
    file_list = []
    size = request.GET.get('size', None)

    user = request.user
    guest_email = request.COOKIES.get('email', None)

    if size is not None:
        width, height = size.split(' x ')
        size = int(width), int(height)

    order = get_salesman_model('Order').objects.get(token=token)
    if order.user == user or order.email == guest_email:
        if request.GET.get('item') is not None:
            order_item = get_salesman_model('OrderItem').objects.get(id=request.GET.get('item'))
            order_item_size = order_item.extra.pop('size', None)
            if order_item_size is not None:
                width, height = order_item_size.split(' x ')
                order_item_size = int(width), int(height)
                order_item.save()
            file_list.append((order_item.product.image.path, order_item_size))
        else:
            order = get_salesman_model('Order').objects.get(token=token)
            for order_item in order.items.all():
                order_item_size = order_item.extra.pop('size', None)
                if order_item_size is not None:
                    width, height = order_item_size.split(' x ')
                    order_item_size = int(width), int(height)
                    order_item.save()
                file_list.append((order_item.product.image.path, order_item_size))

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            with zipfile.ZipFile(temp_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path, image_size in file_list:
                    if size is not None:
                        img = Image.open(file_path)
                        changed_file_path = file_path.split('.')[0] + f'_size={size[0]}x{size[1]}.{file_path.split(".")[1]}'

                        img.thumbnail(size)
                        img.save(changed_file_path)
                    elif image_size is not None:
                        img = Image.open(file_path)
                        changed_file_path = file_path.split('.')[0] + f'_size={image_size[0]}x{image_size[1]}.{file_path.split(".")[1]}'

                        img.thumbnail(image_size)
                        img.save(changed_file_path)
                    else:
                        changed_file_path = file_path

                    file_name = os.path.split(changed_file_path)[1]
                    zipf.write(changed_file_path, file_name)

                    if size is not None or image_size:
                        os.remove(changed_file_path)

        response = FileResponse(open(temp_file.name, 'rb'), as_attachment=True, filename='images.zip')
        os.remove(temp_file.name)

        return response

    raise Http404


@login_required
def download_by_subscription(request: HttpRequest, user_subscription_id: int, product_id: int) -> FileResponse:
    user_subscription = UserSubscription.objects.filter(Q(id=user_subscription_id) & Q(user=request.user))

    size = request.GET.get('size', None)
    if size is not None:
        width, height = size.split(' x ')
        size = int(width), int(height)

    if user_subscription.exists():
        user_subscription = user_subscription.first()

        if user_subscription.downloads_remaining > 0 or user_subscription.plan.unlimited:

            product = ImageProduct.objects.get(id=product_id)
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                with zipfile.ZipFile(temp_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    if size is not None:
                        img = Image.open(product.image.path)
                        changed_file_path = product.image.path.split('.')[0] + f'_size={size[0]}x{size[1]}.{product.image.path.split(".")[1]}'

                        img.thumbnail(size)
                        img.save(changed_file_path)
                    else:
                        changed_file_path = product.image.path

                    zipf.write(changed_file_path, os.path.split(changed_file_path)[1])

                    if size is not None:
                        os.remove(changed_file_path)

            if not user_subscription.plan.unlimited:
                user_subscription.downloads_remaining -= 1
                user_subscription.save()

            response = FileResponse(open(temp_file.name, 'rb'), as_attachment=True, filename='images.zip')
            os.remove(temp_file.name)

            return response

    raise Http404


def basket_preview(request: HttpRequest) -> HttpResponse:
    return render(request, 'blocks/basket_preview_block.html', context={'reload_with_remove_from_basket': request.META.get('HTTP_REFERER') == get_url_by_page_name('basket')})


def wishlist_preview(request: HttpRequest) -> HttpResponse:
    return render(request, 'blocks/wishlist_preview_block.html')


def api_wishlist_count(request: HttpRequest) -> JsonResponse:
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.get(user=request.user.id)
        return JsonResponse({'count': wishlist.images.count()})

    decoded_string = urllib.parse.unquote(request.COOKIES.get('wishlist', '%5B%5D'))
    wishlist = json.loads(decoded_string)
    return JsonResponse({'count': len(wishlist)})


def newsletter(request: HttpRequest) -> HttpResponseRedirect:
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        if not Newsletter.objects.filter(email=email).exists():
            Newsletter.objects.create(email=email, name=name).save()
    else:
        email = request.GET.get('email', '')
        if Newsletter.objects.filter(email=email).exists():
            Newsletter.objects.get(email=email).delete()

    return redirect('/')


def load_products_preview(request: HttpRequest) -> HttpResponse:
    blacklist = ['Thumbs.db', 'Desktop.ini', '.DS_Store', '.', '__']

    def looks_like_file(path: str) -> bool:
        return bool(re.match(r'^.*\.[a-zA-Z0-9]+$', path))

    def in_blacklist(filename: str) -> bool:
        for pattern in blacklist:
            if filename.startswith(pattern):
                return True
        if not looks_like_file(filename):
            return True

        return False

    if request.user.is_authenticated and request.user.is_staff:
        if request.method == 'GET':
            return render(request, 'wagtailadmin/load_products_preview.html',
                          context={'is_loading': False,
                                   'orientations': ImageOrientation.objects.filter(available=True),
                                    'categories': ImageCategory.objects.filter(available=True),
                                    },
                )

        if request.method == 'POST':
            images = request.FILES['images']
            default_price = request.POST.get('price', 0.00)
            default_category = request.POST.get('category', '')
            default_selling_option = request.POST.get('selling_option', 'usual')
            path_to_zip = os.path.join(settings.MEDIA_ROOT, str(uuid.uuid4()))
            with open(path_to_zip, 'wb+') as destination:
                for chunk in images.chunks():
                    destination.write(chunk)

            folder = str(uuid.uuid4())
            path_to_images = os.path.join(settings.MEDIA_ROOT, folder)
            with zipfile.ZipFile(path_to_zip, 'r') as zip_ref:
                zip_ref.extractall(path_to_images)
            os.remove(path_to_zip)

            images_info = []
            image_id = 0
            for root, _, files in os.walk(os.path.join(settings.MEDIA_ROOT, folder)):
                for file in files:
                    if not in_blacklist(file):
                        image_id += 1
                        images_info.append({
                            'id': image_id,
                            'name': file,
                            'price': default_price,
                            'orientation': '',
                            'category': default_category,
                            'selling_option': default_selling_option,
                            'tags': '',
                            'description': '',
                            'url': settings.MEDIA_URL + f'{folder}{root.split(folder)[1]}/{file}',
                            'source': os.path.join(root, file),
                        })

            images_info_file = path_to_images + '.json'
            with open(os.path.join(settings.MEDIA_ROOT, images_info_file), 'w', encoding='utf-8') as file:
                file.write(json.dumps(images_info))

            result = request_images_info.delay(images_info_file)

            return redirect(request.build_absolute_uri() + f'table/?images_info={images_info_file}&key={result.id}')

    raise Http404


def load_products_table(request: HttpRequest) -> HttpResponse | None:

    if request.method == 'GET':
        images_info_file = request.GET.get('images_info')
        key = request.GET.get('key')

        if os.path.exists(os.path.join(settings.MEDIA_ROOT, images_info_file)):
            need_reload = True
            if AsyncResult(key).status == 'SUCCESS':
                need_reload = False
            if AsyncResult(key).status == 'PROGRESS' and AsyncResult(key).info['current'] == 1:
                need_reload = False

            with open(os.path.join(settings.MEDIA_ROOT, images_info_file), encoding='utf-8') as file:
                images_info = json.loads(file.read())

            paginator = Paginator(images_info, 20)

            return render(request, 'wagtailadmin/load_products_edit_table.html',
                context={
                    'page': paginator.page(1),
                    'orientations': ImageOrientation.objects.filter(available=True),
                    'categories': ImageCategory.objects.filter(available=True),
                    'key': key,
                    'need_reload': need_reload,
                    },
                )

    if request.method == 'POST':
        images_info_file = request.GET.get('images_info')
        key = request.GET.get('key')

        if os.path.exists(os.path.join(settings.MEDIA_ROOT, images_info_file)):
            current_page = int(request.POST.get('current_page'))
            next_page = int(request.POST.get('next_page')) if request.POST.get('next_page') else int(request.POST.get('current_page'))

            need_reload = True
            if AsyncResult(key).status == 'SUCCESS':
                need_reload = False

            if AsyncResult(key).status == 'PROGRESS' and AsyncResult(key).info['current'] == next_page:
                need_reload = False

            with open(os.path.join(settings.MEDIA_ROOT, images_info_file), encoding='utf-8') as file:
                images_info = json.loads(file.read())

            paginator = Paginator(images_info, 20)
            start_index, page_length = paginator.page(current_page).start_index(), len(paginator.page(current_page).object_list)
            for index in range(start_index, start_index + page_length):
                images_info[index - 1]['name'] = request.POST.get(f'name_{index}')
                images_info[index - 1]['price'] = request.POST.get(f'price_{index}')
                images_info[index - 1]['orientation'] = request.POST.get(f'orientation_{index}')
                images_info[index - 1]['category'] = request.POST.get(f'category_{index}')
                images_info[index - 1]['selling_option'] = request.POST.get(f'selling_option_{index}')
                images_info[index - 1]['tags'] = request.POST.get(f'tags_{index}')
                images_info[index - 1]['description'] = request.POST.get(f'description_{index}')

            with open(os.path.join(settings.MEDIA_ROOT, images_info_file), 'w', encoding='utf-8') as file:
                file.write(json.dumps(images_info))

            if current_page != next_page:
                return render(request, 'wagtailadmin/load_products_edit_table.html',
                        context={
                            'page': paginator.page(next_page),
                            'orientations': ImageOrientation.objects.filter(available=True),
                            'categories': ImageCategory.objects.filter(available=True),
                            'key': key,
                            'need_reload': need_reload,
                            },
                    )
            result = save_images.delay(images_info_file)
            return render(request, 'wagtailadmin/load_products_result.html',
                context={'key': result.id},
                )

    raise Http404


def check_load_products(request: HttpRequest) -> JsonResponse:
    key = request.GET.get('key', '')
    result = AsyncResult(key)
    if result is not None:
        if result.status == 'SUCCESS':
            return JsonResponse({'status': 'success'})

        if result.status in {'PENDING', 'STARTED'}:
            return JsonResponse({'status': 'progress', 'current': 0, 'total': 0})

        if result.status == 'PROGRESS':
            progress = result.info
            return JsonResponse({'status': 'progress', 'current': progress['current'], 'total': progress['total']})

    return JsonResponse({'status': 'error'})


class EarningReportView(ReportView):
    header_icon = 'heroicons-cash-outline'
    template_name = 'reports/earning_report.html'
    title = _('Earning')

    def get_filtered_queryset(self) -> tuple:
        queryset = self.get_queryset()

        form = EarningFilterForm(self.request.GET)
        form.is_valid()
        date_from = form.data.get('date_from', '')
        date_to = form.data.get('date_to', '')
        income_type = form.data.get('income_type', 'all')

        if date_from:
            queryset = queryset.filter(date_created__date__gte=date_from)

        if date_to:
            queryset = queryset.filter(date_created__date__lte=date_to)

        if income_type == 'balance_replenishments':
            queryset = queryset.filter(_extra__has_key='replenishment_amount')
        elif income_type == 'subscriptions':
            queryset = queryset.exclude(_extra__has_key='subscription')
        elif income_type == 'purchases':
            queryset = queryset.exclude(
                Q(_extra__has_key='replenishment_amount') | Q(_extra__has_key='subscription'),
            )

        return form, queryset

    def get_context_data(self, *args, **kwargs) -> dict:
        context = super().get_context_data(*args, **kwargs)
        context['title'] = self.title
        return context

    def get_queryset(self) -> QuerySet:
        return get_salesman_model('Order').objects.filter(total__gt=0).filter(status='COMPLETED').exclude(payments__payment_method='balance-payment')

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        form, self.object_list = self.get_filtered_queryset()
        context = self.get_context_data()

        context['object_list'] = self.decorate_paginated_queryset(
            context['object_list'],
        )
        context['form'] = form
        total_amount = self.object_list.aggregate(total=Sum('total'))['total']
        if total_amount is None:
            total_amount = 0
        context['total_amount'] = total_amount

        return self.render_to_response(context)
