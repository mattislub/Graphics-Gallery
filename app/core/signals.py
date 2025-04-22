from typing import Type

from django.conf import settings  # type: ignore
from django.contrib.auth.signals import user_logged_in  # type: ignore
from django.db.models import Q  # type: ignore
from django.db.models.signals import post_save  # type: ignore
from django.dispatch import receiver  # type: ignore
from django.http import HttpRequest  # type: ignore
from salesman.core.utils import get_salesman_model  # type: ignore
from shop.models import Order

from core.models import (
    LoginSettings,
    SessionWithUser,
    User,
    Wishlist,
)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_wishlist(sender: Type[User], instance: User, created: bool, **kwargs) -> None:  # noqa FBT001
    if created:
        Wishlist.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def check_user_purchases(sender: Type[User], instance: Order, created: bool, **kwargs) -> None:  # noqa FBT001
    orders = get_salesman_model('Order').objects.filter(Q(email=instance.email) & Q(user=None))
    if orders.exists():
        for order in orders:
            order.user = instance
            order.save()


@receiver(user_logged_in)
def enforce_login_restrictions(sender: Type[User], request: HttpRequest, user: User, **kwargs) -> None:
    if request.user.is_authenticated:
        user_sessions = SessionWithUser.objects.filter(user_id=request.user.id).order_by('date_created')
        login_settings = LoginSettings.load(request_or_site=request)

        if user_sessions.count() + 1 > login_settings.max_simultaneous_logins:
            sessions_to_delete = user_sessions[:(user_sessions.count() + 1) - login_settings.max_simultaneous_logins]
            for session in sessions_to_delete:
                session.delete()
