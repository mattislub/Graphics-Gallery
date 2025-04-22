from django.http import HttpRequest  # type: ignore
from salesman.basket.modifiers import BasketModifier  # type: ignore

from shop.models import (
    Basket,
    BasketItem,
)


class LimitBasketModifier(BasketModifier):
    identifier = 'limit'

    def setup_item(self, item: BasketItem, request: HttpRequest) -> None:
        if item.quantity > 1:
            item.quantity = 1
            item.save()


class FilterBasketModifier(BasketModifier):
    identifier = 'filter'

    def process_basket(self, basket: Basket, request: HttpRequest) -> None:
        is_replenishment = basket.extra.pop('is_replenishment', False)
        is_purchasing_subscription = basket.extra.pop('is_purchasing_subscription', False)

        for basket_item in basket.items.all():

            if is_replenishment and basket_item.code[0] != 'B':
                basket_item.delete()

            elif is_purchasing_subscription and basket_item.code[0] != 'S':
                basket_item.delete()

            elif basket_item.code[0] in {'B', 'S'}:
                basket_item.delete()

        basket.save()
