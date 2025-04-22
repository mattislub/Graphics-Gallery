from django.template.context import RenderContext
from django import template
from pages import models
from urllib.parse import (
    urlunparse,
    urlencode,
    urlparse,
    parse_qs,
)

register = template.Library()


@register.simple_tag
def get_url_by_page_name(name: str):
    try:
        match name:
            case 'about-us':
                return models.AboutUsPage.objects.filter(live=True).first().get_full_url()
            case 'home':
                return models.HomePage.objects.filter(live=True).first().get_full_url()
            case 'basket':
                return models.BasketPage.objects.filter(live=True).first().get_full_url()
            case 'categories':
                return models.CategoriesPage.objects.filter(live=True).first().get_full_url()
            case 'product':
                return models.ProductPage.objects.filter(live=True).first().get_full_url()
            case 'contact-us':
                return models.ContactUsPage.objects.filter(live=True).first().get_full_url()
            case 'payment-methods':
                return models.PaymentMethodsPage.objects.filter(live=True).first().get_full_url()
            case 'privacy-and-security':
                return models.InformationPage.objects.filter(live=True).filter(page_type='privacy_and_security').first().get_full_url()
            case 'accessibility':
                return models.InformationPage.objects.filter(live=True).filter(page_type='accessibility').first().get_full_url()
            case 'faq':
                return models.FAQPage.objects.filter(live=True).first().get_full_url()
            case 'images':
                return models.ImagesPage.objects.filter(live=True).first().get_full_url()
            case 'registration':
                return '/user/registration/'
            case 'login':
                return '/user/login/'
            case 'logout':
                return '/user/logout/'
            case 'profile':
                return '/user/profile/'
            case 'transactions':
                return '/user/transactions/'
            case 'purchases':
                return '/user/purchases/'
            case 'wishlist':
                return '/user/wishlist/'
            case 'to-svg':
                return '/to-svg/'
            case _:
                return '/'

    except AttributeError:
        return '/'


@register.simple_tag(takes_context=True)
def change_page_url(context: RenderContext, page: int):
    request = context.get('request')
    url_parts = urlparse(request.build_absolute_uri())
    query_params = parse_qs(url_parts.query)
    query_params['page'] = [str(page)]
    new_query = urlencode(query_params, doseq=True)
    new_url_parts = url_parts._replace(query=new_query)
    return urlunparse(new_url_parts)


@register.inclusion_tag('elements/popular_products.html', takes_context=True)
def render_popular_products(context: RenderContext, popular_products, reload_with_add_to_basket: bool = False):
    return {'request': context.request, 'user': context.get('user'), 'popular_products': popular_products, 'reload_with_add_to_basket': reload_with_add_to_basket}


@register.inclusion_tag('elements/similar_products.html', takes_context=True)
def render_similar_products(context: RenderContext, similar_products, reload_with_add_to_basket: bool = False):
    return {'request': context.request, 'user': context.get('user'), 'similar_products': similar_products, 'reload_with_add_to_basket': reload_with_add_to_basket}


@register.inclusion_tag('elements/last_added_products.html', takes_context=True)
def render_last_added_products(context: RenderContext, last_added_products, reload_with_add_to_basket: bool = False):
    return {'request': context.request, 'user': context.get('user'), 'last_added_products': last_added_products, 'reload_with_add_to_basket': reload_with_add_to_basket}


@register.inclusion_tag('elements/popular_categories.html', takes_context=True)
def render_popular_categories(context: RenderContext, popular_categories):
    return {'request': context.request, 'user': context.get('user'), 'popular_categories': popular_categories}


@register.inclusion_tag('elements/popular_queries.html', takes_context=True)
def render_popular_queries(context: RenderContext, popular_queries):
    return {'request': context.request, 'user': context.get('user'), 'popular_queries': popular_queries}
