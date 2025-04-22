import json
import uuid

import requests  # type: ignore
from django.http import (  # type: ignore
    HttpRequest,
    HttpResponseRedirect,
)
from django.shortcuts import redirect  # type: ignore
from django.urls import (  # type: ignore
    path,
    reverse,
)
from django.utils.translation import gettext_lazy as _  # type: ignore
from pages.templatetags.pages import get_url_by_page_name  # type: ignore
from salesman.checkout.payment import (  # type: ignore
    PaymentError,
    PaymentMethod,
)
from salesman.core.utils import get_salesman_model  # type: ignore

from shop.email_notifications import (
    send_purchase_confirmation,
    send_replenishment_confirmation,
    send_subscription_confirmation,
)
from shop.models import (
    Basket,
    ImageProduct,
    Order,
    UserSubscription,
    ZCreditSettings,
)
from shop.tasks import checkout_ZCreditPayment


def validate_address(value: str, context: dict) -> str:
    return value


def increase_product_downloads(order: Order) -> None:
    for order_item in order.items.all():
        if order_item.product.code[0] == 'I':
            product = ImageProduct.objects.get(id=order_item.product_id)
            product.downloads += 1
            product.save()


def get_detail_order_note_message(order: Order) -> str:
    message = ''
    for order_item in order.items.all():
        if order_item.product.code[0] == 'I':
            message += f'{order_item.name}[{order_item.code}]\n'
        if order_item.product.code[0] == 'B':
            message += f'{_("Replenishment balance")} {order_item.product.replenishment}\n'
        if order_item.product.code[0] == 'S':
            message += f'{_("Purchasing a subscription")} {order_item.product.download_limit if not order_item.product.unlimited else "∞"}/{order_item.product.duration_days}\n'

    return message[:-1]


class BalancePayment(PaymentMethod):
    identifier = 'balance-payment'
    label = 'Pay from balance'

    def basket_payment(self, basket: Basket, request: HttpRequest) -> HttpResponseRedirect:
        user = request.user
        if user.balance >= basket.total:
            order = get_salesman_model('Order').objects.create_from_basket(basket, request, status='COMPLETED')

            if order.email != user.email:
                order.email = user.email
                order.save()

            order.pay(
                amount=order.amount_outstanding,
                transaction_id=uuid.uuid4(),
                payment_method=self.identifier,
            )
            order.save()

            detail_note = get_salesman_model('OrderNote').objects.create(
                order=order,
                message=get_detail_order_note_message(order),
                public=True,
            )
            detail_note.save()

            user.balance -= basket.total
            user.save()

            basket.delete()

            increase_product_downloads(order)
            send_purchase_confirmation(request, order)

            return redirect(f'/download/{order.token}/')

        raise PaymentError(_('Insufficient funds on balance'))

    def refund_payment(self, payment: str) -> bool:
        print(payment, type(payment))
        return False


class ZCreditPayment(PaymentMethod):
    identifier = 'zcredit-payment'
    label = 'Pay from card'

    api_server = 'https://pci.zcredit.co.il/ZCreditWS/api/'

    dev_create_session = 'https://private-anon-1fe1cb4956-zcreditwc.apiary-mock.com/webcheckout/api/WebCheckout/CreateSession'
    dev_session_status = 'https://private-anon-1fe1cb4956-zcreditwc.apiary-mock.com/webcheckout/api/WebCheckout/GetSessionStatus'

    create_session = 'https://pci.zcredit.co.il/webcheckout/api/WebCheckout/CreateSession'
    session_status = 'https://pci.zcredit.co.il/webcheckout/api/WebCheckout/GetSessionStatus'

    headers: dict = {  # noqa
        'User-agent': 'Mozilla/5.0',
        'Content-Type': 'application/json; charset=utf-8',
    }

    def get_urls(self) -> list[str]:
        return [
            path('success/', self.success_payment, name='zcredit-payment-success'),
        ]

    def get_formated_basket_items(self, basket: Basket, request: HttpRequest) -> list[dict]:
        basket_items = []
        for basket_item in basket.items.all():
            basket_item.update(request)
            basket_items.append({
                'Name': basket_item.product.name,
                'Amount': f'{float(basket_item.total)}',
                'Currency': 'ILS',
                'Quantity': 1,
                'IsTaxFree': 'false',
                'AdjustAmount': 'false',
            })

        return basket_items

    def session_create_data(self, basket_items: list[dict], order: Order, request: HttpRequest) -> dict:
        settings = ZCreditSettings.load(request_or_site=request)

        return {
            'Key': settings.key,
            'Local': 'He',
            'UniqueId': order.ref,
            'SuccessUrl': request.build_absolute_uri(reverse('zcredit-payment-success') + f'?ref={order.ref}'),
            'PaymentType': 'regular',
            'CreateInvoice': 'false',
            'AdditionalText': settings.additional_text,
            'ShowCart': settings.show_cart,
            'ForceCaptcha': settings.force_captcha,
            'Customer': {
                'Email': order.email,
                'Name': f'{request.user.first_name} {request.user.last_name}' if request.user.is_authenticated else 'Guest',
            },
            'CartItems': basket_items,
        }

    def basket_payment(self, basket: Basket, request: HttpRequest) -> HttpResponseRedirect:
        order = get_salesman_model('Order').objects.create_from_basket(basket, request, status='NEW')
        order.extra['basket_id'] = basket.id
        order.save()

        basket_items = self.get_formated_basket_items(basket, request)
        values = self.session_create_data(basket_items, order, request)
        create_session_request = requests.post(
            self.create_session,
            data=json.dumps(values, indent=4),
            headers=self.headers,
            timeout=10,
        )

        if create_session_request.status_code == 200:  # noqa PLR2004
            create_session_request = create_session_request.json()

            if create_session_request['HasError'] is False:
                order.extra['reference_number'] = create_session_request['Data']['ReferenceNumber']
                order.extra['session_id'] = create_session_request['Data']['SessionId']
                order.extra['unique_id'] = create_session_request['Data']['UniqueID']
                order.extra['token'] = create_session_request['Data']['Token']
                order.save(update_fields=['extra'])

                checkout_ZCreditPayment.apply_async((request.build_absolute_uri(reverse('zcredit-payment-success') + f'?ref={order.ref}'), ), countdown=7200)  # 2 hours
                return redirect(create_session_request['Data']['SessionUrl'])

        order.status = 'FAILED'
        order.save()

        raise PaymentError('Payment failed')

    def process_order(self, request: HttpRequest, order: Order) -> HttpResponseRedirect:
        user = request.user

        for order_item in order.items.all():
            if order_item.product_type == 'shop.BalanceProduct':
                order.extra['replenishment_amount'] = float(order_item.product.replenishment)
                order.save(update_fields=['extra'])
                user.balance += float(order_item.product.replenishment)
                user.save()

                send_replenishment_confirmation(request, order)
                return redirect(get_url_by_page_name('user-transactions'))

            if order_item.product_type == 'shop.SubscriptionPlan':
                order.extra['subscription'] = order_item.main_text
                order.extra['subscription_duration_days'] = order_item.duration_days
                order.extra['subscription_downloads_remaining'] = '∞' if order_item.unlimited else order_item.download_limit
                order.save(update_fields=['extra'])

                user_subscription = UserSubscription(
                    user=user,
                    plan=order_item.product_id,
                )
                user_subscription.save()

                send_subscription_confirmation(request, order)
                return redirect(get_url_by_page_name('user-transactions'))

        increase_product_downloads(order)
        send_purchase_confirmation(request, order)
        return redirect(f'/download/{order.token}/')

    def refund_payment(self, payment: str) -> bool:
        return False

    def success_payment(self, request: HttpRequest) -> HttpResponseRedirect:
        try:
            ref = request.GET['ref']
        except KeyError as error:
            raise PaymentError('Invalid request') from error

        try:
            order = get_salesman_model('Order').objects.get(ref=ref)
            if order.status != 'COMPLETED':
                settings = ZCreditSettings.load(request_or_site=request)

                session_id = order.extra['session_id']
                session_status_request = requests.post(
                    self.session_status,
                    data=json.dumps({'SessionId': session_id, 'Key': settings.key}, indent=4),
                    headers=self.headers,
                    timeout=10,
                )

                if session_status_request.status_code == 200:  # noqa PLR2004
                    session_status_request = session_status_request.json()
                    if session_status_request['TransactionSuccess']:

                        transaction_id = session_status_request['TransactionID']
                        basket_id = order.extra.pop('basket_id', None)

                        if basket_id is not None:
                            basket = get_salesman_model('Basket').objects.get(id=basket_id)
                            basket.delete()

                            order.status = 'COMPLETED'
                            order.pay(
                                amount=order.amount_outstanding,
                                transaction_id=transaction_id,
                                payment_method=self.identifier,
                            )
                            order.save()

                            detail_note = get_salesman_model('OrderNote').objects.create(
                                order=order,
                                message=get_detail_order_note_message(order),
                                public=True,
                            )
                            detail_note.save()
                            self.process_order(request, order)

                order.status = 'FAILED'
                order.save()
                raise PaymentError('Payment failed')

            for order_item in order.items.all():
                if order_item.product_type == 'shop.BalanceProduct':
                    return redirect(get_url_by_page_name('user-transactions'))

                if order_item.product_type == 'shop.SubscriptionPlan':
                    return redirect(get_url_by_page_name('user-transactions'))

            return redirect(f'/download/{order.token}/')

        except (get_salesman_model('Order').DoesNotExist, get_salesman_model('Basket').DoesNotExist) as error:
            raise PaymentError('Payment failed') from error
