import json
import urllib.parse

from core.models import Wishlist
from django import template
from django.core.paginator import (
    EmptyPage,
    Page,
    Paginator,
)
from django.db.models import (
    Q,
    QuerySet,
)
from django.template.context import RenderContext
from django.utils import timezone
from salesman.core.utils import get_salesman_model

from shop.models import (
    ImageCategory,
    ImageProduct,
    PaginatorSettings,
    UserSubscription,
)

register = template.Library()


@register.simple_tag(takes_context=True)
def get_user_orders(context: RenderContext) -> Page:
    request = context.get('request')
    user = context.get('user')

    page = int(request.GET.get('page', 1))

    orders = get_salesman_model('Order').objects.filter(Q(user=user) & Q(status='COMPLETED')).order_by('-date_created').distinct()
    paginator = Paginator(orders, 20)

    if page > paginator.num_pages:
        page = 0

    try:
        return paginator.page(page)
    except EmptyPage:
        return ()


@register.simple_tag(takes_context=True)
def get_user_wishlist_images(context: RenderContext) -> QuerySet | dict:
    user = context.get('user')
    if user.is_authenticated:
        user_subscriptions = UserSubscription.objects.filter(
            Q(downloads_remaining__gte=0)
            & Q(user=user)
            & Q(end_date__gte=timezone.localtime()),
        )
        wishlist_image_products = Wishlist.objects.get(user=user.id).images.filter(Q(subscription_plans__id__in=[user_subscription.plan.id for user_subscription in user_subscriptions]) | Q(subscription_plans__isnull=True))
    else:
        request = context.get('request')
        decoded_string = urllib.parse.unquote(request.COOKIES.get('wishlist', '%5B%5D'))
        wishlist_codes = [int(code[1:]) for code in json.loads(decoded_string)]
        wishlist_image_products = ImageProduct.objects.filter(id__in=wishlist_codes)

    return wishlist_image_products


@register.simple_tag(takes_context=True)
def get_filtered_user_wishlist(context: RenderContext) -> Page:

    request = context.get('request')
    user = context.get('user')

    page = int(request.GET.get('page', 1))
    search = request.GET.get('search', None)
    tag = request.GET.get('tag', None)
    category = request.GET.get('image-category', None)
    orientation = request.GET.get('image-orientation', None)
    premium = request.GET.get('premium', None)
    usual = request.GET.get('usual', None)

    sort_by = request.GET.get('sort-by', 'popular')

    user_subscriptions = []
    if user.is_authenticated:
        user_subscriptions = UserSubscription.objects.filter(
            Q(downloads_remaining__gte=0)
            & Q(user=user)
            & Q(end_date__gte=timezone.localtime()),
        )

    image_products = Wishlist.objects.get(user=user.id).images.all()

    if premium is not None:
        image_products = image_products.filter(premium=True)

    if usual is not None:
        image_products = image_products.filter(Q(premium=False) & Q(subscription_plans__isnull=True))

    if orientation is not None:
        image_products = image_products.filter(orientation__slug=orientation)

    if category is not None:
        category = ImageCategory.objects.get(slug=category)
        subcategories = category.get_all_subcategories()
        all_categories = [category, *subcategories]
        category_ids = [cat.id for cat in all_categories]

        image_products = image_products.filter(category__id__in=category_ids)

    if tag is not None:
        image_products = image_products.filter(tags__slug=tag)

    if search:
        search = search.split(',')
        for phrase in search:
            image_products &= image_products.filter(tags__name__icontains=phrase.strip()) | image_products.filter(name__icontains=phrase.strip()) | image_products.filter(description__icontains=phrase.strip())

    image_products = image_products.filter(Q(subscription_plans__id__in=[user_subscription.plan.id for user_subscription in user_subscriptions]) | Q(subscription_plans__isnull=True))

    if sort_by == 'popular':
        image_products = image_products.distinct().order_by('-downloads')
    elif sort_by == 'date_to_old':
        image_products = image_products.distinct().order_by('-publish_date')
    elif sort_by == 'date_to_new':
        image_products = image_products.distinct().order_by('publish_date')
    elif sort_by == 'price_to_high':
        image_products = image_products.distinct().order_by('price')
    elif sort_by == 'price_to_low':
        image_products = image_products.distinct().order_by('-price')

    paginator_settings = PaginatorSettings.load(request_or_site=request)
    paginator = Paginator(image_products, paginator_settings.products_per_page)

    if page > paginator.num_pages:
        page = 0

    try:
        return paginator.page(page)
    except EmptyPage:
        return ()


@register.simple_tag(takes_context=True)
def get_filtered_user_purchased_products(context: RenderContext) -> Page:

    request = context.get('request')
    user = context.get('user')

    page = int(request.GET.get('page', 1))
    search = request.GET.get('search', None)
    tag = request.GET.get('tag', None)
    category = request.GET.get('image-category', None)
    orientation = request.GET.get('image-orientation', None)
    premium = request.GET.get('premium', None)

    sort_by = request.GET.get('sort-by', 'popular')

    order_items = get_salesman_model('OrderItem').objects.filter(Q(order__user=user) & Q(order__status='COMPLETED') & Q(product_type='shop.ImageProduct')).order_by('-order__date_created').distinct()
    paid_product_ids = order_items.values_list('product_id', flat=True)

    image_products = ImageProduct.objects.filter(id__in=paid_product_ids)

    if premium in {'true', 'false'}:
        image_products = image_products.filter(premium=(premium == 'true'))

    if orientation is not None:
        image_products = image_products.filter(orientation__slug=orientation)

    if category is not None:
        category = ImageCategory.objects.get(slug=category)
        subcategories = category.get_all_subcategories()
        all_categories = [category, *subcategories]
        category_ids = [cat.id for cat in all_categories]

        image_products = image_products.filter(category__id__in=category_ids)

    if tag is not None:
        image_products = image_products.filter(tags__slug=tag)

    if search:
        search = search.split(',')
        for phrase in search:
            image_products &= image_products.filter(tags__name__icontains=phrase.strip()) | image_products.filter(name__icontains=phrase.strip()) | image_products.filter(description__icontains=phrase.strip())

    if sort_by == 'popular':
        image_products = image_products.distinct().order_by('-downloads')
    elif sort_by == 'date_to_old':
        image_products = image_products.distinct().order_by('-publish_date')
    elif sort_by == 'date_to_new':
        image_products = image_products.distinct().order_by('publish_date')
    elif sort_by == 'price_to_high':
        image_products = image_products.distinct().order_by('price')
    elif sort_by == 'price_to_low':
        image_products = image_products.distinct().order_by('-price')

    paginator_settings = PaginatorSettings.load(request_or_site=request)
    paginator = Paginator(image_products, paginator_settings.products_per_page)

    if page > paginator.num_pages:
        page = 0

    try:
        return paginator.page(page)
    except EmptyPage:
        return ()


@register.simple_tag(takes_context=True)
def get_user_subscriptions(context: RenderContext) -> QuerySet:
    user = context.get('user')

    return UserSubscription.objects.filter(Q(user=user) & Q(end_date__gte=timezone.localtime()))
