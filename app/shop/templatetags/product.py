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
    Sum,
)
from django.template.context import RenderContext
from django.utils import timezone
from salesman.core.utils import get_salesman_model
from taggit.models import Tag

from shop.models import (
    BalanceProduct,
    ImageCategory,
    ImageProduct,
    ImageThumbnailSettings,
    PaginatorSettings,
    SubscriptionPlan,
    UserSubscription,
)

register = template.Library()


@register.simple_tag
def get_balance_products() -> QuerySet:
    return BalanceProduct.objects.filter(available=True).order_by('price')


@register.simple_tag
def get_subscription_plans() -> QuerySet:
    return SubscriptionPlan.objects.filter(available=True).order_by('price')


@register.simple_tag(takes_context=True)
def get_possible_image_sizes(context: RenderContext) -> list[str]:
    request = context.get('request')

    image_thumbnail_options = ImageThumbnailSettings.load(request_or_site=request).thumbnail_options

    sizes = []
    for thumbnail_option in image_thumbnail_options.split(','):
        sizes.append(f'{request.product.image.width // int(thumbnail_option)} x {request.product.image.height // int(thumbnail_option)}')

    return sizes


@register.simple_tag(takes_context=True)
def product_in_wishlist(context: RenderContext, product: ImageProduct) -> bool:
    user = context.get('user')

    if user.is_authenticated:
        user_wishlist = Wishlist.objects.get(user=user.id)
        if product in user_wishlist.images.all():
            return True
    else:
        request = context.get('request')
        decoded_string = urllib.parse.unquote(request.COOKIES.get('wishlist', '%5B%5D'))
        wishlist = json.loads(decoded_string)

        if product.code in wishlist:
            return True

    return False


@register.simple_tag(takes_context=True)
def product_is_paid(context: RenderContext, product: ImageProduct) -> bool:
    user = context.get('user')

    if user.is_authenticated:
        orders = get_salesman_model('Order').objects.filter(Q(user=user) & Q(status='COMPLETED') & Q(items__product_id=product.id) & Q(items__product_type='shop.ImageProduct'))
        if orders.exists():
            for order in orders:
                if order.is_paid:
                    return True
    else:
        request = context.get('request')
        guest_email = request.COOKIES.get('email', None)
        if guest_email is not None:
            orders = get_salesman_model('Order').objects.filter(Q(email=guest_email) & Q(status='COMPLETED') & Q(items__product_id=product.id) & Q(items__product_type='shop.ImageProduct'))
            if orders.exists():
                for order in orders:
                    if order.is_paid:
                        return True

    return False


@register.simple_tag(takes_context=True)
def product_is_avaliable_by_subscription(context: RenderContext, product: ImageProduct) -> bool:
    user = context.get('user')
    if user.is_authenticated:
        user_subscriptions = UserSubscription.objects.filter(
            Q(downloads_remaining__gte=0)
            & Q(user=user)
            & Q(end_date__gte=timezone.localtime()),
        )

        if user_subscriptions.exists():
            for user_subscription in user_subscriptions.all():
                if (
                    user_subscription.plan in product.subscription_plans.all()
                    and (user_subscription.downloads_remaining > 0 or user_subscription.plan.unlimited)
                ):
                    return True

    return False


@register.simple_tag(takes_context=True)
def product_in_basket(context: RenderContext, product: ImageProduct) -> bool:

    request = context.get('request')
    basket, _ = get_salesman_model('Basket').objects.get_or_create_from_request(request)

    for basket_item in basket.items.all():
        if basket_item.product.code == product.code:
            return True

    return False


@register.simple_tag(takes_context=True)
def get_popular_products(context: RenderContext, filters: str, display: int, page_number: int = 1) -> Page:
    product = None
    basket, _ = get_salesman_model('Basket').objects.get_or_create_from_request(context['request'])
    basket_products = basket.items.values_list('product_id', flat=True)

    if hasattr(context['request'], 'product'):
        product = context['request'].product

    user = context.get('user')
    user_subscriptions = []
    if user.is_authenticated:
        user_subscriptions = UserSubscription.objects.filter(
            Q(downloads_remaining__gte=0)
            & Q(user=user)
            & Q(end_date__gte=timezone.localtime()),
        )

    filter_kwargs = {}
    if filters:
        filters = [f.split('=') for f in filters.split(',')]
        filter_kwargs = {f[0]: f[1] for f in filters}

    popular_products = ImageProduct.objects.filter(**filter_kwargs).order_by('-downloads')
    popular_products = popular_products.filter(Q(subscription_plans__id__in=[user_subscription.plan.id for user_subscription in user_subscriptions]) | Q(subscription_plans__isnull=True)).order_by('-downloads')
    if product is not None:
        popular_products = popular_products.exclude(id=product.id)

    if basket_products.exists():
        popular_products = popular_products.exclude(id__in=basket_products).order_by('-downloads')

    paginator = Paginator(popular_products.distinct(), display)

    try:
        page = paginator.page(page_number)
        return page.object_list
    except EmptyPage:
        return ()


@register.simple_tag(takes_context=True)
def get_similar_products(context: RenderContext, filters: str, display: int, page_number: int = 1) -> Page:
    product = None
    basket, _ = get_salesman_model('Basket').objects.get_or_create_from_request(context['request'])
    basket_products = basket.items.values_list('product_id', flat=True)

    if hasattr(context['request'], 'product'):
        product = context['request'].product

    user = context.get('user')
    user_subscriptions = []
    if user.is_authenticated:
        user_subscriptions = UserSubscription.objects.filter(
            Q(downloads_remaining__gte=0)
            & Q(user=user)
            & Q(end_date__gte=timezone.localtime()),
        )

    filter_kwargs = {}
    if filters:
        filters = [f.split('=') for f in filters.split(',')]
        filter_kwargs = {f[0]: f[1] for f in filters}

    similar_products = ImageProduct.objects.filter(Q(subscription_plans__id__in=[user_subscription.plan.id for user_subscription in user_subscriptions]) | Q(subscription_plans__isnull=True)).order_by('-downloads')

    if product is not None:
        similar_products.filter(
            Q(tags__in=product.tags.all()) | Q(category=product.category),
        ).exclude(id=product.id)

    if basket_products.exists():
        basket_products_objs = ImageProduct.objects.filter(id__in=basket_products)
        tags = [tag for product in basket_products_objs for tag in product.tags.all()]
        categories = basket_products_objs.values_list('category', flat=True).distinct()

        similar_products = similar_products.filter(
            Q(tags__in=tags) | Q(category__in=categories),
        )

        similar_products = similar_products.exclude(id__in=basket_products)

    similar_products = similar_products.filter(**filter_kwargs).order_by('-downloads')
    paginator = Paginator(similar_products.distinct(), display)

    try:
        page = paginator.page(page_number)
        return page.object_list

    except EmptyPage:
        return ()


@register.simple_tag(takes_context=True)
def get_last_added_products(context: RenderContext, filters: str, display: int, page_number: int = 1) -> Page:
    product = None
    basket, _ = get_salesman_model('Basket').objects.get_or_create_from_request(context['request'])
    basket_products = basket.items.values_list('product_id', flat=True)

    if hasattr(context['request'], 'product'):
        product = context['request'].product

    user = context.get('user')
    user_subscriptions = []
    if user.is_authenticated:
        user_subscriptions = UserSubscription.objects.filter(
            Q(downloads_remaining__gte=0)
            & Q(user=user)
            & Q(end_date__gte=timezone.localtime()),
        )

    filter_kwargs = {}
    if filters:
        filters = [f.split('=') for f in filters.split(',')]
        filter_kwargs = {f[0]: f[1] for f in filters}

    last_added_products = ImageProduct.objects.filter(**filter_kwargs).order_by('-publish_date')
    last_added_products = last_added_products.objects.filter(Q(subscription_plans__id__in=[user_subscription.plan.id for user_subscription in user_subscriptions]) | Q(subscription_plans__isnull=True)).order_by('-publish_date')

    if product is not None:
        last_added_products = last_added_products.exclude(id=product.id)

    if basket_products.exists():
        last_added_products = last_added_products.exclude(id__in=basket_products)

    paginator = Paginator(last_added_products.distinct(), display)

    try:
        page = paginator.page(page_number)
        return page.object_list
    except EmptyPage:
        return ()


@register.simple_tag(takes_context=True)
def get_popular_categories(context: RenderContext, filters: str, display: int, page_number: int = 1) -> Page:
    filter_kwargs = {}
    if filters:
        filters = [f.split('=') for f in filters.split(',')]
        filter_kwargs = {f[0]: f[1] for f in filters}

    popular_categories = ImageCategory.objects.annotate(
        total_downloads=Sum('imageproduct__downloads'),
    ).order_by('-total_downloads')
    popular_categories = popular_categories.filter(available=True).filter(**filter_kwargs)

    paginator = Paginator(popular_categories.distinct(), display)

    try:
        page = paginator.page(page_number)
        return page.object_list
    except EmptyPage:
        return ()


@register.simple_tag(takes_context=True)
def get_popular_queries(context: RenderContext, query_option: str, display: int, page_number: int = 1) -> Page:
    if query_option == 'tags':
        popular_queries = (Tag.objects.filter(taggit_taggeditem_items__image_products__isnull=False)
                           .annotate(total_downloads=Sum('taggit_taggeditem_items__image_products__downloads'))
                           .order_by('-total_downloads'))
    else:
        popular_queries = ImageCategory.objects.annotate(
            total_downloads=Sum('imageproduct__downloads'),
        ).filter(available=True).order_by('-total_downloads')

    paginator = Paginator(popular_queries.distinct(), display)

    try:
        page = paginator.page(page_number)
        return page.object_list
    except EmptyPage:
        return ()


@register.simple_tag()
def get_products_tags(products_list: list) -> QuerySet:
    tags_qs = Tag.objects.none()

    for product in products_list:
        product_tags = product.tags.all()
        tags_qs |= product_tags

    return tags_qs.distinct()


@register.simple_tag(takes_context=True)
def get_download_link(context: RenderContext, product: ImageProduct) -> str | None:

    user = context.get('user')
    if user.is_authenticated:
        user_subscriptions = UserSubscription.objects.filter(
            Q(downloads_remaining__gte=0)
            & Q(user=user)
            & Q(end_date__gte=timezone.localtime()),
        )

        orders = get_salesman_model('Order').objects.filter(
            (Q(user=user) & Q(status='COMPLETED'))
            & Q(items__product_id=product.id)
            & Q(items__product_type='shop.ImageProduct'))

        if orders.exists():
            for order in orders:
                if order.is_paid:
                    for item in order.items.all():
                        if item.product_id == product.id:
                            return f'/download/{order.token}/?item={item.id}'

        elif user_subscriptions.exists():
            for user_subscription in user_subscriptions.all():
                if (
                    user_subscription.plan in product.subscription_plans.all()
                    and (user_subscription.downloads_remaining > 0 or user_subscription.plan.unlimited)
                ):
                    return f'/download-by-subscription/{user_subscription.id}/{product.id}/'
    else:
        request = context.get('request')
        guest_email = request.COOKIES.get('email', None)
        if guest_email is not None:
            orders = get_salesman_model('Order').objects.filter(Q(email=guest_email) & Q(status='COMPLETED') & Q(items__product_id=product.id) & Q(items__product_type='shop.ImageProduct'))
            if orders.exists():
                for order in orders:
                    if order.is_paid:
                        for item in order.items.all():
                            if item.product_id == product.id:
                                return f'/download/{order.token}/?item={item.id}'
    return None


@register.simple_tag(takes_context=True)
def get_filtered_products(context: RenderContext) -> Page:

    request = context.get('request')
    user = context.get('user')
    user_subscriptions = []
    if user.is_authenticated:
        user_subscriptions = UserSubscription.objects.filter(
            Q(downloads_remaining__gte=0)
            & Q(user=user)
            & Q(end_date__gte=timezone.localtime()),
        )

    page = int(request.GET.get('page', 1))
    search = request.GET.get('search', None)
    tag = request.GET.get('tag', None)
    category = request.GET.get('image-category', None)
    orientation = request.GET.get('image-orientation', None)
    premium = request.GET.get('premium', None)
    usual = request.GET.get('usual', None)
    free = request.GET.get('free', None)

    sort_by = request.GET.get('sort-by', 'popular')

    image_products = ImageProduct.objects.all()

    if premium is not None:
        image_products = image_products.filter(premium=True)

    if usual is not None:
        image_products = image_products.filter(Q(premium=False) & Q(subscription_plans__isnull=True))

    if free is not None:
        image_products = image_products.filter(subscription_plans__isnull=False)

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


@register.inclusion_tag('products/balance_product.html', takes_context=True)
def render_balance_product(context: RenderContext, balance_product: BalanceProduct) -> dict:
    return {'balance_product': balance_product, 'request': context.request}


@register.inclusion_tag('products/subscription_plan.html', takes_context=True)
def render_subscription_plan(context: RenderContext, subscription_plan: SubscriptionPlan) -> dict:
    return {'subscription_plan': subscription_plan, 'request': context.request}


@register.inclusion_tag('products/image_product.html', takes_context=True)
def render_image_product(context: RenderContext, image_product: ImageProduct, reload_with_add_to_basket: bool = False) -> dict:
    return {'user': context.get('user'),
            'product': image_product,
            'request': context.request,
            'reload_with_add_to_basket': reload_with_add_to_basket,
            }


@register.inclusion_tag('elements/category.html', takes_context=True)
def render_category(context: RenderContext, category: ImageCategory) -> dict:
    return {'user': context.get('user'),
            'category': category,
            'request': context.request,
            }


@register.inclusion_tag('elements/category_preview.html')
def render_category_preview(category: ImageCategory) -> dict:
    return {'category': category}
