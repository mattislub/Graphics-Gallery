import datetime
import os
import uuid
from typing import (
    Any,
    Self,
)

from django.conf import settings  # type: ignore
from django.contrib.contenttypes.fields import GenericRelation  # type: ignore
from django.db import models  # type: ignore
from django.http import HttpRequest  # type: ignore
from django.utils.html import format_html  # type: ignore
from django.utils.translation import gettext_lazy as _  # type: ignore
from modelcluster.models import ClusterableModel  # type: ignore
from salesman.basket.models import (  # type: ignore
    BaseBasket,
    BaseBasketItem,
)
from salesman.orders.models import (  # type: ignore
    BaseOrder,
    BaseOrderItem,
    BaseOrderNote,
    BaseOrderPayment,
)
from salesman.orders.status import BaseOrderStatus  # type: ignore
from slugify import slugify  # type: ignore
from taggit.managers import TaggableManager  # type: ignore
from taggit.models import TaggedItem  # type: ignore
from wagtail.contrib.settings.models import (  # type: ignore
    BaseGenericSetting,
    register_setting,
)
from wagtail.models import PreviewableMixin  # type: ignore
from wagtail.search import index  # type: ignore


# SALESMAN
class OrderStatus(BaseOrderStatus):

    NEW = 'NEW', _('New')

    CREATED = 'CREATED', _('Created')
    HOLD = 'HOLD', _('Hold')
    FAILED = 'FAILED', _('Failed')

    COMPLETED = 'COMPLETED', _('Completed')
    REFUNDED = 'REFUNDED', _('Refunded')

    @classmethod
    def get_payable(cls) -> list:
        return [cls.CREATED, cls.HOLD, cls.FAILED]

    @classmethod
    def get_transitions(cls) -> dict[str, list]:
        return {
            'NEW': [cls.CREATED],

            'CREATED': [cls.HOLD, cls.FAILED, cls.COMPLETED, cls.REFUNDED],
            'HOLD': [cls.FAILED, cls.COMPLETED, cls.REFUNDED],
            'FAILED': [cls.COMPLETED, cls.REFUNDED],

            'COMPLETED': [cls.REFUNDED],
            'REFUNDED': [],
        }


class Basket(BaseBasket):
    pass


class BasketItem(BaseBasketItem):
    pass


class Order(BaseOrder):
    @property
    def is_paid(self) -> bool:
        return self.amount_paid >= self.total and self.total > 0


class OrderItem(BaseOrderItem):
    pass


class OrderPayment(BaseOrderPayment):
    pass


class OrderNote(BaseOrderNote):
    pass


class ImageOrientation(index.Indexed, models.Model):
    '''Image orientation.'''
    name = models.CharField(verbose_name=_('Image orientation'), max_length=20, blank=False)
    slug = models.SlugField(verbose_name=_('Slug'), unique=True, blank=True, allow_unicode=settings.WAGTAIL_ALLOW_UNICODE_SLUGS, max_length=100)
    available = models.BooleanField(verbose_name=_('Available for viewing'), default=True)

    search_auto_update = True
    search_fields = (
        index.AutocompleteField('name'),
    )

    class Meta:
        verbose_name = _('Image orientation')
        verbose_name_plural = _('Image orientations')

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> Any:
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=settings.WAGTAIL_ALLOW_UNICODE_SLUGS)
        return super().save(*args, **kwargs)


class ImageCategory(index.Indexed, models.Model):
    '''Image category.'''
    name = models.CharField(verbose_name=_('Category'), max_length=255, blank=False)
    slug = models.SlugField(verbose_name=_('Slug'), blank=True, unique=True, allow_unicode=settings.WAGTAIL_ALLOW_UNICODE_SLUGS, max_length=100)
    available = models.BooleanField(verbose_name=_('Available for viewing'), default=True)
    parent_category = models.ForeignKey('ImageCategory', verbose_name=_('Parent category'), blank=True, null=True, on_delete=models.SET_NULL)
    preview_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('Preview image'),
    )

    small_preview_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('Small preview image'),
    )

    display_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('Display image'),
    )

    search_fields = (
        index.AutocompleteField('__str__'),
        index.AutocompleteField('name'),
    )

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self) -> str:
        return ('' if self.parent_category is None else str(self.parent_category) + ' > ') + self.name

    def save(self, *args, **kwargs) -> Any:
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=settings.WAGTAIL_ALLOW_UNICODE_SLUGS)
        return super().save(*args, **kwargs)

    def get_all_subcategories(self) -> list[Self]:
        subcategories = list(self.imagecategory_set.all())
        for subcategory in self.imagecategory_set.all():
            subcategories.extend(subcategory.get_all_subcategories())
        return subcategories


class ImageProduct(PreviewableMixin, index.Indexed, ClusterableModel):
    '''Product: Image.'''

    def save_image_to(_, filename: str) -> str:  # noqa N805
        return f'products/{uuid.uuid4()}{os.path.splitext(filename)[1]}'

    name = models.CharField(verbose_name=_('Product name'), max_length=255, blank=True)
    description = models.TextField(verbose_name=_('Product description'), blank=True)
    price = models.DecimalField(verbose_name=_('Price'), max_digits=18, decimal_places=2, default=0)
    image = models.ImageField(upload_to=save_image_to, verbose_name=_('Product image'))

    orientation = models.ForeignKey('ImageOrientation', verbose_name=_('Orientation'), on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey('ImageCategory', verbose_name=_('Category'), on_delete=models.SET_NULL, null=True)

    tags = TaggableManager(blank=True, verbose_name=_('Tags'))
    related_tags = GenericRelation(TaggedItem, related_query_name='image_products')

    premium = models.BooleanField(verbose_name=_('Premium'), default=False)
    subscription_plans = models.ManyToManyField('SubscriptionPlan', verbose_name=_('Available on subscription plans'), blank=True)

    # Internal data
    downloads = models.PositiveBigIntegerField(default=0)
    publish_date = models.DateField(auto_now_add=True)

    search_auto_update = True
    search_fields = (
        index.AutocompleteField('name'),
        index.AutocompleteField('code'),
        index.RelatedFields('category', [index.AutocompleteField('__str__'), index.AutocompleteField('name')]),
        index.RelatedFields('orientation', [index.AutocompleteField('name')]),
        index.RelatedFields('tags', [index.AutocompleteField('name')]),
    )

    def __str__(self) -> str:
        return format_html(f'<img src="{self.image.url}" width=60/> {self.name} {self.code} [ {self.price} ]')

    def save(self, *args, **kwargs) -> Any:
        if not self.name:
            self.name = str(uuid.uuid4())
        return super().save(*args, **kwargs)

    @property
    def code(self) -> str:
        return 'I' + str(self.id).zfill(10)

    @property
    def information(self) -> str:
        return _('Premium') if self.premium else (_('Subscription') if len(self.subscription_plans.all()) else _('Usual'))

    @property
    def admin_preview(self) -> str:
        return format_html(f'<img src="{self.image.url}" width=60/>')

    @property
    def display_image_name(self) -> str:
        return f'{str(self.id).zfill(10)}_display.avif'

    @property
    def display_image_url(self) -> str:
        return f'{settings.MEDIA_URL}previews/{str(self.id).zfill(10)}_display.avif'

    @property
    def preview_image_name(self) -> str:
        return f'{str(self.id).zfill(10)}_preview.avif'

    @property
    def preview_image_url(self) -> str:
        return f'{settings.MEDIA_URL}previews/{str(self.id).zfill(10)}_preview.avif'

    @property
    def size(self) -> str:
        return f'{self.image.width} x {self.image.height}'

    @property
    def dpi(self) -> str:
        return '300'  # TODO add real dpi

    def get_price(self, request: HttpRequest) -> float:
        return self.price

    def get_preview_template(self, request: HttpRequest, mode_name: str) -> str:
        request.product = self
        return 'pages/product_page.html'


class BalanceProduct(index.Indexed, models.Model):
    main_text = models.CharField(verbose_name=_('Main text'), max_length=255, blank=True)
    help_text = models.CharField(verbose_name=_('Help text'), max_length=255, blank=True)
    badge_text = models.CharField(verbose_name=_('Badge text'), max_length=255, blank=True)

    price = models.DecimalField(verbose_name=_('Price'), max_digits=18, decimal_places=2, default=0, unique=True)
    replenishment = models.DecimalField(verbose_name=_('Replenishment'), max_digits=18, decimal_places=2, default=0)
    available = models.BooleanField(verbose_name=_('Available for viewing'), default=True)

    search_auto_update = True
    search_fields = (
        index.AutocompleteField('main_text'),
        index.AutocompleteField('help_text'),
        index.AutocompleteField('price'),
        index.AutocompleteField('replenishment'),
    )

    def __str__(self) -> str:
        return self.name

    @property
    def name(self) -> str:
        return f'{self.price} -> {self.replenishment}'

    def get_price(self, request: HttpRequest) -> float:
        return self.price

    @property
    def code(self) -> str:
        return 'B' + str(self.id).zfill(4)


class SubscriptionPlan(index.Indexed, models.Model):
    main_text = models.CharField(verbose_name=_('Main text'), max_length=255, blank=True)
    help_text = models.CharField(verbose_name=_('Help text'), max_length=255, blank=True)
    badge_text = models.CharField(verbose_name=_('Badge text'), max_length=255, blank=True)

    price = models.DecimalField(verbose_name=_('Price'), max_digits=18, decimal_places=2, default=0, unique=True)
    download_limit = models.PositiveIntegerField(verbose_name=_('Download limit'), default=0)
    unlimited = models.BooleanField(default=False, verbose_name=_('Unlimited downloads'))
    duration_days = models.PositiveIntegerField(verbose_name=_('Duration'), default=30)
    available = models.BooleanField(verbose_name=_('Available for viewing'), default=True)

    search_auto_update = True
    search_fields = (
        index.AutocompleteField('main_text'),
        index.AutocompleteField('help_text'),
        index.AutocompleteField('price'),
        index.AutocompleteField('download_limit'),
    )

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> Any:
        if self.unlimited:
            self.download_limit = 0
        return super().save(*args, **kwargs)

    @property
    def name(self) -> str:
        return f'{_("Subscription plan")}: {self.download_limit if not self.unlimited else "∞"}/{self.duration_days}'

    @property
    def code(self) -> str:
        return 'S' + str(self.id).zfill(4)

    def get_price(self, request: HttpRequest) -> float:
        return self.price


class UserSubscription(index.Indexed, models.Model):
    user = models.ForeignKey('core.User', on_delete=models.CASCADE, verbose_name=_('User'))
    plan = models.ForeignKey('SubscriptionPlan', on_delete=models.SET_NULL, null=True, verbose_name=_('Subscription plan'))
    start_date = models.DateField(verbose_name=_('Start date'))
    end_date = models.DateField(verbose_name=_('End date'))
    downloads_remaining = models.IntegerField(verbose_name=_('Downloads remaining'))
    renew = models.BooleanField(default=True, verbose_name=_('Refresh when finished'))

    search_auto_update = True
    search_fields = (
        index.RelatedFields('user', [index.AutocompleteField('username'), index.AutocompleteField('email'), index.AutocompleteField('first_name'), index.AutocompleteField('last_name')]),
        index.RelatedFields('plan', [index.AutocompleteField('main_text'), index.AutocompleteField('help_text'), index.AutocompleteField('price'), index.AutocompleteField('download_limit')]),
    )

    def __str__(self) -> str:
        return f'{self.user.email} - {self.plan.name} [{self.downloads_remaining}]'

    def save(self, *args, **kwargs) -> Any:
        if not self.id:
            self.start_date = datetime.datetime.now(tz=datetime.timezone.utc).date()
            self.end_date = self.start_date + datetime.timedelta(days=self.plan.duration_days)
            self.downloads_remaining = self.plan.download_limit
        super().save(*args, **kwargs)


# SETTINGS
@register_setting(icon='heroicons-adjustments-outline')
class PaginatorSettings(BaseGenericSetting):
    products_per_page = models.PositiveIntegerField(default=40, verbose_name=_('Products per page'))


@register_setting(icon='heroicons-photograph-outline')
class ImageThumbnailSettings(BaseGenericSetting):
    thumbnail_options = models.CharField(default='1, 2, 3', verbose_name=_('Image thumbnail options'), help_text=_('Integers separated by commas indicating how much to reduce the image size'))


@register_setting(icon='upload')
class OpenAISettings(BaseGenericSetting):
    openai_api_key = models.CharField(max_length=255, verbose_name=_('OpenAI API key'))


@register_setting(icon='heroicons-credit-card-outline')
class ZCreditSettings(BaseGenericSetting):
    key = models.CharField(
        max_length=255,
        verbose_name=_('Z-Credit key'),
    )
    additional_text = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('Additional text'),
        help_text=_('Text to be logged with the transaction data. You can view it in your backoffice account online.'),
    )
    show_cart = models.BooleanField(
        default=True,
        verbose_name=_('Show Cart'),
        help_text=_('Allows to hide the cart list of items, to get a minimal UI for credit card data only.'),
    )

    force_captcha = models.BooleanField(
        default=False,
        verbose_name=_('Force Captcha'),
        help_text=_('When set to true, the payment page will show a "RecaptchaV2" inside the payment page.'),
    )
