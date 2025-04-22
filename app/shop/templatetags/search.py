from django import template
from django.db.models import QuerySet
from django.template.context import RenderContext
from django.utils.translation import gettext_lazy as _

from shop.models import (
    ImageCategory,
    ImageOrientation,
)

register = template.Library()


# Search

@register.simple_tag
def get_image_orientations() -> QuerySet:
    return ImageOrientation.objects.filter(available=True)


@register.simple_tag
def get_image_categories() -> list:
    def get_image_category_tree(parent: ImageCategory | None = None) -> list:
        image_categories = ImageCategory.objects.filter(parent_category=parent, available=True).order_by('slug')

        image_category_list = []
        for image_category in image_categories:
            image_category_list.append(image_category)
            image_category_list.extend(get_image_category_tree(parent=image_category))

        return image_category_list

    return get_image_category_tree()


@register.simple_tag
def get_sorting_options() -> list[dict]:
    return [
        {'slug': 'popular', 'name': _('Popular')},
        {'slug': 'date_to_old', 'name': _('Date &darr;')},
        {'slug': 'date_to_new', 'name': _('Date &uarr;')},
        {'slug': 'price_to_high', 'name': _('Price &uarr;')},
        {'slug': 'price_to_low', 'name': _('Price &darr;')},
    ]


@register.simple_tag(takes_context=True)
def get_selected_image_category(context: RenderContext) -> bool:
    request = context.get('request')
    image_category_slug = request.GET.get('image-category', None)

    if image_category_slug is not None:
        return ImageCategory.objects.get(slug=image_category_slug)

    return False


@register.simple_tag(takes_context=True)
def get_search_text(context: RenderContext) -> bool:
    request = context.get('request')
    return request.GET.get('search', '')


@register.simple_tag(takes_context=True)
def has_children_image_categories(context: RenderContext) -> bool:
    request = context.get('request')

    parent_category = request.GET.get('image-category', None)

    if parent_category is not None:
        return ImageCategory.objects.filter(parent_category__slug=parent_category).filter(available=True).exists()

    return False


@register.simple_tag(takes_context=True)
def get_children_image_categories(context: RenderContext) -> list:
    request = context.get('request')

    parent_category = request.GET.get('image-category', None)
    children_image_categories = []

    if parent_category is not None:
        children_image_categories = ImageCategory.objects.filter(parent_category__slug=parent_category).filter(available=True)

    return children_image_categories
