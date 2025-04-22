import datetime
import secrets
from typing import ClassVar

from django.contrib.auth.models import (  # type: ignore
    AbstractBaseUser,
    BaseUserManager,
    Group,
    Permission,
    PermissionsMixin,
)
from django.contrib.sessions.backends.db import SessionStore as DBStore  # type: ignore
from django.contrib.sessions.base_session import AbstractBaseSession  # type: ignore
from django.db import models  # type: ignore
from django.utils.translation import gettext_lazy as _  # type: ignore
from wagtail.admin.panels import (  # type: ignore
    FieldPanel,
    MultiFieldPanel,
)
from wagtail.contrib.settings.models import (  # type: ignore
    BaseGenericSetting,
    register_setting,
)
from wagtail.models import Page  # type: ignore
from wagtail.search import index  # type: ignore
from wagtailmetadata.models import MetadataPageMixin  # type: ignore


class UserManager(BaseUserManager):
    """Manager for users."""
    def create_user(self, email: str, password: str | None = None, **kw) -> AbstractBaseUser:
        """Create, save and return new user."""
        if not email or not email.split("@")[0]:
            raise ValueError("User must have email.")
        user = self.model(email=self.normalize_email(email), **kw)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email: str, password: str | None = None, **kw) -> AbstractBaseUser:
        """Create and return new Superuser."""
        return self.create_user(email,
                                password,
                                is_staff=True,
                                is_superuser=True,
                                is_active=True,
                                **kw,
                                )

    @staticmethod
    def normalize_email(email: str) -> str:
        name, domain = email.split("@")
        return f"{name.replace(' ', '')}@{domain.replace(' ', '').lower()}"


class User(AbstractBaseUser, PermissionsMixin):
    """User."""

    def create_verification_code() -> str:  # type: ignore
        return ''.join(str(secrets.randbelow(10)) for i in range(6))

    username = models.CharField(verbose_name=_('Username'), max_length=255, unique=True, blank=False, null=False)
    email = models.EmailField(verbose_name=_('Email'), max_length=255, unique=True, blank=False, null=False)
    first_name = models.CharField(verbose_name=_('First name'), max_length=255, blank=False, null=False)
    last_name = models.CharField(verbose_name=_('Last name'), max_length=255, blank=False, null=False)

    balance = models.DecimalField(verbose_name=_('Balance'), max_digits=18, decimal_places=2, default=50)

    verification_code = models.CharField(verbose_name=_('Verification code'), default=create_verification_code, max_length=6, blank=True)
    registration_date = models.DateTimeField(verbose_name=_('Registration date'), auto_now_add=True)

    is_active = models.BooleanField(verbose_name=_('User is active'), default=False)
    is_staff = models.BooleanField(verbose_name=_('User is staff'), default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'

    groups = models.ManyToManyField(Group, blank=True, related_name='core_user_groups')
    user_permissions = models.ManyToManyField(
        Permission, blank=True, related_name='core_user_permissions',
    )

    balance_replenishment_notification = models.BooleanField(verbose_name=_('Balance replenishment notification'), default=True)
    purchase_notification = models.BooleanField(verbose_name=_('Purchase notification'), default=True)
    filled_cart_notification = models.BooleanField(verbose_name=_('Filled cart notification'), default=True)


class WishlistImage(models.Model):
    wishlist = models.ForeignKey('Wishlist', on_delete=models.CASCADE)
    image = models.ForeignKey('shop.ImageProduct', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return ''


class Wishlist(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='wishlist')
    images = models.ManyToManyField('shop.ImageProduct', through='WishlistImage', blank=True)

    def __str__(self) -> str:
        return f'Wishlist: {self.user.email}'


class ExtPage(MetadataPageMixin, Page):
    keywords = models.CharField(max_length=255, verbose_name=_('Meta keywords'), blank=True)

    search_fields: ClassVar = [*Page.search_fields, index.AutocompleteField('keywords', partial_match=True, boost=2)]
    promote_panels = (  # type: ignore
        MultiFieldPanel([
            FieldPanel('slug'),
            FieldPanel('seo_title', heading=_('Title tag')),
            FieldPanel('search_description'),
            FieldPanel('keywords'),
            FieldPanel('search_image'),
        ], heading=_('For search engines')),
    )

    class Meta:
        abstract = True

    def get_meta_keywords(self) -> list[str]:
        if len(self.keywords):
            return [key.strip() for key in self.keywords.split(',')]

        return []


@register_setting(icon='heroicons-at-symbol-outline')
class EmailSettings(BaseGenericSetting):
    host = models.CharField(blank=True, verbose_name=_('Email host'))
    port = models.CharField(blank=True, verbose_name=_('Email port'))
    login = models.EmailField(blank=True, verbose_name=_('Email login'))
    password = models.CharField(blank=True, verbose_name=_('Email Password'))
    use_tls = models.BooleanField(default=False, verbose_name=_('Use TLS'))


@register_setting(icon='heroicons-user-group-outline')
class LoginSettings(BaseGenericSetting):
    max_simultaneous_logins = models.PositiveIntegerField(
        default=5,
        verbose_name=_('Maximum Simultaneous Logins'),
        help_text=_('The maximum number of devices a user can be logged in simultaneously.'),
    )


@register_setting(icon='heroicons-photograph-outline')
class SVGLifetimeSettings(BaseGenericSetting):
    lifetime = models.PositiveIntegerField(
        default=120,
        verbose_name=_('SVG Lifetime'),
        help_text=_('The time in minutes during which the svg image will be available after conversion.'),
    )


class Newsletter(models.Model):
    email = models.EmailField(verbose_name=_('Email'), unique=True)
    name = models.TextField(verbose_name=_('Name'))

    def __str__(self) -> str:
        return f'{self.email} {self.name}'


class SessionWithUser(AbstractBaseSession):
    user_id = models.IntegerField(null=True, db_index=True)
    date_created = models.DateTimeField(null=True)

    @classmethod
    def get_session_store_class(cls) -> DBStore:
        return SessionStore


class SessionStore(DBStore):
    @classmethod
    def get_model_class(cls) -> AbstractBaseSession:

        return SessionWithUser

    def create_model_instance(self, data: dict) -> AbstractBaseSession:
        obj = super().create_model_instance(data)

        try:
            user_id = int(data.get('_auth_user_id'))  # type: ignore
        except (ValueError, TypeError):
            user_id = None

        obj.user_id = user_id
        obj.date_created = datetime.datetime.isoformat(datetime.datetime.now(tz=datetime.timezone.utc))
        return obj
