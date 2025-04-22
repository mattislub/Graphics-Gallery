from core.models import (
    EmailSettings,
    Newsletter,
)
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import (
    EmailMessage,
    get_connection,
)
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import RequestFactory
from django.utils.translation import gettext_lazy as _
from salesman.basket.serializers import BasketSerializer
from wagtail.models import Site

from shop.models import (
    Basket,
    ImageProduct,
    Order,
)


def send_user_verification_code(request: HttpRequest) -> None:
    try:
        user_id = request.session.get('user_id', None)
        if user_id is not None and get_user_model().objects.filter(id=user_id).exists():
            email_settings = EmailSettings.load(request_or_site=request)
            site = Site.find_for_request(request)
            user = get_user_model().objects.get(id=user_id)
            message_body = render_to_string('email/email_verification.html',
                                            request=request,
                                            context={'verification_code': user.verification_code})

            email_backend = get_connection(
                host=email_settings.host,
                port=int(email_settings.port),
                username=email_settings.login,
                password=email_settings.password,
                use_tls=email_settings.use_tls,
                use_ssl=True,
                fail_silently=False,
            )

            email = EmailMessage(
                subject=_('Verification code'),
                body=message_body,
                from_email=f'{site.site_name} <{email_settings.login}>',
                to=[user.email],
                connection=email_backend,
            )
            email.content_subtype = 'html'
            email.send()
        else:
            messages.error(request, _('Your account was not found.'))
    except Exception:
        messages.error(request, _('Something went wrong. Please try later.'))


def send_purchase_confirmation(request: HttpRequest, order: Order, **kwargs) -> None:

    try:
        if order.status == order.Status.COMPLETED:
            if order.user is not None and order.user.purchase_notification is False:
                return

            email_settings = EmailSettings.load(request_or_site=request)
            site = Site.find_for_request(request)

            message_body = render_to_string('email/purchase_confirmation.html',
                                            request=request,
                                            context={'order': order})

            email_backend = get_connection(
                host=email_settings.host,
                port=int(email_settings.port),
                username=email_settings.login,
                password=email_settings.password,
                use_tls=email_settings.use_tls,
                use_ssl=True,
                fail_silently=False,
            )

            email = EmailMessage(
                subject=_('You have made a successful purchase'),
                body=message_body,
                from_email=f'{site.site_name} <{email_settings.login}>',
                to=[order.email],
                connection=email_backend,
            )
            email.content_subtype = 'html'
            email.send()

    except Exception:
        pass


def send_subscription_confirmation(request: HttpRequest, order: Order, **kwargs) -> None:
    try:
        if order.status == order.Status.COMPLETED:
            if order.user is not None and order.user.purchase_notification is False:
                return

            email_settings = EmailSettings.load(request_or_site=request)
            site = Site.find_for_request(request)

            message_body = render_to_string('email/subscription_confirmation.html', request=request, context={'order': order})

            email_backend = get_connection(
                host=email_settings.host,
                port=int(email_settings.port),
                username=email_settings.login,
                password=email_settings.password,
                use_tls=email_settings.use_tls,
                use_ssl=True,
                fail_silently=False,
            )

            email = EmailMessage(
                subject=_('You have made a successful subscription purchase'),
                body=message_body,
                from_email=f'{site.site_name} <{email_settings.login}>',
                to=[order.email],
                connection=email_backend,
            )
            email.content_subtype = 'html'
            email.send()

    except Exception:
        pass


def send_replenishment_confirmation(request: HttpRequest, order: Order, **kwargs) -> None:
    try:
        if order.status == order.Status.COMPLETED:
            if order.user is not None and order.user.balance_replenishment_notification is False:
                return

            email_settings = EmailSettings.load(request_or_site=request)
            site = Site.find_for_request(request)

            message_body = render_to_string('email/replenishment_confirmation.html', request=request, context={'order': order})

            email_backend = get_connection(
                host=email_settings.host,
                port=int(email_settings.port),
                username=email_settings.login,
                password=email_settings.password,
                use_tls=email_settings.use_tls,
                use_ssl=True,
                fail_silently=False,
            )

            email = EmailMessage(
                subject=_('You have made a successful replenishment'),
                body=message_body,
                from_email=f'{site.site_name} <{email_settings.login}>',
                to=[order.email],
                connection=email_backend,
            )
            email.content_subtype = 'html'
            email.send()

    except Exception:
        pass


def send_basket_notification(basket: Basket, **kwargs) -> None:
    try:
        if basket.user is not None and basket.user.filled_cart_notification is False:
            return

        request = RequestFactory().get('/')
        email_settings = EmailSettings.load(request_or_site=request)
        site = Site.find_for_request(request)

        serializer = BasketSerializer(basket, context={'basket': basket, 'request': request})

        message_body = render_to_string('email/unpaid_basket_notification.html',
                                        request=request,
                                        context={'basket': dict(serializer.data), 'user': f'{basket.user.first_name} {basket.user.last_name}'})

        email_backend = get_connection(
            host=email_settings.host,
            port=int(email_settings.port),
            username=email_settings.login,
            password=email_settings.password,
            use_tls=email_settings.use_tls,
            use_ssl=True,
            fail_silently=False,
        )

        email = EmailMessage(
            subject=_('You have unpaid basket'),
            body=message_body,
            from_email=f'{site.site_name} <{email_settings.login}>',
            to=[basket.user.email],
            connection=email_backend,
        )
        email.content_subtype = 'html'
        email.send()

    except Exception:
        pass


def send_new_images_notification(images: list[int]) -> None:
    try:
        chunk_size = 4
        request = RequestFactory().get('/')
        email_settings = EmailSettings.load(request_or_site=request)
        site = Site.find_for_request(request)

        images = ImageProduct.objects.filter(id__in=images)

        new_images = [images[i:i + chunk_size] for i in range(0, len(images), chunk_size)]

        for user in Newsletter.objects.all():
            message_body = render_to_string('email/new_images_notification.html',
                                            request=request,
                                            context={'new_images': new_images, 'user': f'{user.name}', 'email': user.email})

            email_backend = get_connection(
                host=email_settings.host,
                port=int(email_settings.port),
                username=email_settings.login,
                password=email_settings.password,
                use_tls=email_settings.use_tls,
                use_ssl=True,
                fail_silently=False,
            )

            email = EmailMessage(
                subject=_('We have new images'),
                body=message_body,
                from_email=f'{site.site_name} <{email_settings.login}>',
                to=[user.email],
                connection=email_backend,
            )
            email.content_subtype = 'html'
            email.send()

    except Exception:
        pass
