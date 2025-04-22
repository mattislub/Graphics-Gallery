from django import template
from django.template.context import RenderContext
from salesman.basket.serializers import BasketSerializer
from salesman.core.utils import get_salesman_model

register = template.Library()


@register.simple_tag(takes_context=True)
def get_basket(context: RenderContext) -> dict:
    basket, _ = get_salesman_model('Basket').objects.get_or_create_from_request(context['request'])
    serializer = BasketSerializer(basket, context={'basket': basket, 'request': context['request']})
    return dict(serializer.data)
