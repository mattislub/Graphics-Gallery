import random
from typing import Any

from core.models import (
    EmailSettings,
    ExtPage,
)
from django.conf import settings  # type: ignore
from django.db import models  # type: ignore
from django.http import HttpRequest  # type: ignore
from django.utils.translation import gettext_lazy as _  # type: ignore
from modelcluster.fields import ParentalKey  # type: ignore
from shop.models import (
    ImageCategory,
    ImageProduct,
)
from wagtail import blocks  # type: ignore
from wagtail.admin.panels import (  # type: ignore
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
)
from wagtail.fields import StreamField  # type: ignore
from wagtail.images.blocks import ImageChooserBlock  # type: ignore
from wagtail.models import Orderable  # type: ignore
from wagtail.url_routing import RouteResult  # type: ignore
from wagtailiconchooser.blocks import IconChooserBlock  # type: ignore
from wagtailvideos.blocks import VideoChooserBlock  # type: ignore


class RootPage(ExtPage):
    object_type = 'website'
    schemaorg_type = 'WebSite'

    @property
    def email(self) -> str:
        request = self.get_request()
        email_settings = EmailSettings.load(request_or_site=request)
        return email_settings.login


class AboutUsDetail(Orderable, models.Model):
    title = models.CharField(max_length=255, blank=True, verbose_name=_('Title'))
    text = models.TextField(blank=True, verbose_name=_('Text'))

    page = ParentalKey(
        'pages.AboutUsPage',
        on_delete=models.CASCADE,
        related_name='detail_items',
    )

    def __str__(self) -> str:
        return self.title


class AboutUsPage(RootPage):
    object_type = 'website'
    schemaorg_type = 'AboutPage'
    max_count = 1
    parent_page_types = None

    about_us_description = models.TextField(blank=True, verbose_name=_('Short description'))

    about_us_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    about_us_detail_title = models.CharField(max_length=255, blank=True, verbose_name=_('About us detail title'))

    content_panels = (
        MultiFieldPanel([
            FieldPanel('title'),
            FieldPanel('about_us_image', heading=_('Background image')),
            FieldPanel('about_us_description', heading=_('Short description')),
            FieldPanel('about_us_detail_title', heading=_('About us detail title')),
            InlinePanel('detail_items', label=_('Detail items')),
        ], heading=_('About us page')),
    )


# Changed
class PopularProducts(models.Model):
    title = models.CharField(max_length=255, blank=True, verbose_name=_('Popular products title'))
    filters = models.CharField(max_length=255, blank=True, verbose_name=_('Additional filters'))
    display = models.PositiveIntegerField(verbose_name=_('Number of products in the block'), default=8)

    def __str__(self) -> str:
        return self.title


class SimilarProducts(models.Model):
    title = models.CharField(max_length=255, blank=True, verbose_name=_('Similar products title'))
    filters = models.CharField(max_length=255, blank=True, verbose_name=_('Additional filters'))
    display = models.PositiveIntegerField(verbose_name=_('Number of products in the block'), default=8)

    def __str__(self) -> str:
        return self.title


class LastAddedProducts(models.Model):
    title = models.CharField(max_length=255, blank=True, verbose_name=_('Last added products title'))
    filters = models.CharField(max_length=255, blank=True, verbose_name=_('Additional filters'))
    display = models.PositiveIntegerField(verbose_name=_('Number of products in the block'), default=8)

    def __str__(self) -> str:
        return self.title


class PopularCategories(models.Model):
    title = models.CharField(max_length=255, blank=True, verbose_name=_('Popular categorues title'))
    filters = models.CharField(max_length=255, blank=True, verbose_name=_('Additional filters'))
    display = models.PositiveIntegerField(verbose_name=_('Number of categories in the block'), default=8)

    def __str__(self) -> str:
        return self.title


class PopularQueries(models.Model):
    title = models.CharField(max_length=255, blank=True, verbose_name=_('Popular queries title'))
    query_option = models.CharField(
        max_length=20,
        choices=(('tags', _('Tags')),
                 ('categories', _('Categories')),
                 ('random', _('Random'))),
        verbose_name=_('Option'),
    )
    display = models.PositiveIntegerField(verbose_name=_('Number of items in the block'), default=8)
    new_tab = models.BooleanField(verbose_name=_('Should be opened in a new tab?'), default=True)

    def __str__(self) -> str:
        return self.title + ' ' + self.get_query_option_display()

    @property
    def current_option(self) -> tuple[str, str]:
        if self.query_option == 'tags':
            return 'tags', _('Tags')
        if self.query_option == 'categories':
            return 'categories', _('Categories')

        return random.choice([('tags', _('Tags')), ('categories', _('Categories'))])  # noqa S311


class FAQPage(RootPage):
    object_type = 'article'
    schemaorg_type = 'FAQPage'
    max_count = 1
    parent_page_types = None

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('Image'),
    )
    sub_title = models.CharField(max_length=255, blank=True, verbose_name=_('Sub title'))

    body = StreamField(
        [
            ('block', blocks.StructBlock(
                [
                    ('question', blocks.CharBlock()),
                    ('answer', blocks.TextBlock(required=False)),
                    ('link', blocks.StructBlock([('link_text', blocks.CharBlock(required=False)), ('url', blocks.URLBlock(required=False))])),
                ])),
            ('html', blocks.RawHTMLBlock(required=False)),
        ],
        use_json_field=True,
        verbose_name=_('Page body'))

    content_panels = (
        MultiFieldPanel([
            FieldPanel('title'),
            FieldPanel('sub_title'),
            FieldPanel('image'),
            FieldPanel('body'),
        ], heading=_('FAQ page')),
    )


class InformationPage(RootPage):
    object_type = 'website'
    schemaorg_type = 'AboutPage'
    max_count = 2
    parent_page_types = None

    page_type = models.CharField(
        max_length=20,
        choices=(('privacy_and_security', _('Privacy and Security')),
                 ('accessibility', _('Accessibility'))),
        verbose_name=_('Page type'),
    )

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('Image'),
    )

    body = StreamField(
        [
            (
                'text', blocks.RichTextBlock(
                    features=['h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'bold', 'italic', 'link'],
                ),
            ),
        ],
        use_json_field=True,
        verbose_name=_('Page body'),
    )

    content_panels = (
        MultiFieldPanel([
            FieldPanel('title'),
            FieldPanel('page_type'),
            FieldPanel('image'),
            FieldPanel('body'),
        ], heading=_('Information page')),
    )


class ContactUsPage(RootPage):
    object_type = 'contact'
    schemaorg_type = 'ContactPage'
    max_count = 1
    parent_page_types = None

    sub_title = models.CharField(blank=True, verbose_name=_('Sub title'))

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('Image'),
    )

    content_panels = (
        MultiFieldPanel([
            FieldPanel('title'),
            FieldPanel('sub_title'),
            FieldPanel('image'),
        ], heading=_('Contact us page')),
    )


class PaymentMethodsPage(RootPage):
    object_type = 'website'
    schemaorg_type = 'AboutPage'
    max_count = 1
    parent_page_types = None

    sub_title = models.CharField(blank=True, verbose_name=_('Sub title'))

    body = StreamField(
        [
            ('cardpayment',
             blocks.StructBlock(
                 [
                     ('title', blocks.CharBlock()),
                     ('text', blocks.RichTextBlock(features=['h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'bold', 'italic', 'link'])),
                 ])),
            ('balancepayment',
             blocks.StructBlock(
                 [
                     ('title', blocks.CharBlock()),
                     ('text', blocks.RichTextBlock(features=['h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'bold', 'italic', 'link'])),
                 ])),
            ('subscriptions',
             blocks.StructBlock(
                 [
                     ('title', blocks.CharBlock()),
                     ('text', blocks.RichTextBlock(features=['h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'bold', 'italic', 'link'])),
                 ])),
        ],
        block_counts={'cardpayment': {'max_num': 1}, 'balancepayment': {'max_num': 1}, 'subscriptions': {'max_num': 1}},
        use_json_field=True,
        verbose_name=_('Body'),
    )

    content_panels = (
        MultiFieldPanel([
            FieldPanel('title'),
            FieldPanel('sub_title'),
            FieldPanel('body'),
        ], heading=_('Payment methods page')),
    )


class BasketPage(RootPage):
    object_type = 'product.item-list'
    schemaorg_type = 'Offer'
    max_count = 1
    parent_page_types = None

    private_page_options = ('login', )

    similar_products = models.ForeignKey(
        'SimilarProducts',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    content_panels = (
        MultiFieldPanel([
            FieldPanel('title'),
        ], heading=_('Basket page')),
        MultiFieldPanel([
            FieldPanel('similar_products', heading=_('Similar products')),
        ], heading=_('Similar products block')),
    )


class ProductPage(RootPage):
    object_type = 'product'
    schemaorg_type = 'Product'
    max_count = 1
    parent_page_types = None

    popular_products = models.ForeignKey(
        'PopularProducts',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    similar_products = models.ForeignKey(
        'SimilarProducts',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    content_panels = (
        MultiFieldPanel([
            FieldPanel('title'),
        ], heading=_('Product page')),
        MultiFieldPanel([
            FieldPanel('popular_products', heading=_('Popular products')),
        ], heading=_('Popular products block')),
        MultiFieldPanel([
            FieldPanel('similar_products', heading=_('Similar products')),
        ], heading=_('Similar products block')),
    )

    def get_meta_image(self) -> str | None:
        request = self.get_request()
        if hasattr(request, 'product'):
            return request.product.display_image_url

        if self.search_image is not None:
            return self.build_absolute_uri(
                self.search_image.get_rendition(getattr(settings, "META_SEARCH_IMAGE_RENDITION", "fill-800x450")).url,
            )
        return super().get_meta_image()

    def get_meta_url(self) -> str:
        return self.get_request().build_absolute_uri()

    def get_meta_title(self) -> str:
        additional_title = ''
        request = self.get_request()
        if hasattr(request, 'product'):
            additional_title += ':' + request.product.name

        return (self.seo_title or self.title) + additional_title

    def get_meta_keywords(self) -> list[str]:
        keywords = []
        request = self.get_request()

        if len(self.keywords):
            keywords.extend([key.strip() for key in self.keywords.split(',')])

        if hasattr(request, 'product'):
            keywords.extend([tags.name for tags in request.product.tags.all()])

        return keywords

    def get_meta_description(self) -> str:
        additional_description = ''
        request = self.get_request()
        if hasattr(request, 'product'):
            additional_description += ' ' + request.product.description

        return self.search_description + additional_description

    def route(self, request: HttpRequest, path_components: list) -> Any:
        if len(path_components) == 1:
            product_code = path_components[0]

            if product_code.startswith('I') and product_code[1:].isdigit():
                request.product = ImageProduct.objects.get(id=int(product_code[1:]))

        return RouteResult(self)


class HomePage(RootPage):
    object_type = 'website'
    schemaorg_type = 'WebSite'
    max_count = 1
    parent_page_types = None

    sub_title = models.CharField(max_length=255, blank=True, verbose_name=_('Sub title'))

    popular_products = models.ForeignKey(
        'PopularProducts',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    popular_categories = models.ForeignKey(
        'PopularCategories',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    popular_queries = models.ForeignKey(
        'PopularQueries',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    advertising_blocks = StreamField(
        [
            ('singleimageblock',
             blocks.StructBlock(
                 [
                     ('title', blocks.CharBlock()),
                     ('text', blocks.RichTextBlock(features=['h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'bold', 'italic', 'link'])),
                     ('icon', blocks.StructBlock([('icon', IconChooserBlock()), ('icon_color', blocks.CharBlock())])),
                     ('image', ImageChooserBlock()),
                     ('image_position', blocks.ChoiceBlock(choices=[('left', _('Left')), ('right', _('Right'))])),
                 ], template='blocks/singleimageblock.html')),
            ('multiimagesblock',
             blocks.StructBlock(
                 [
                     ('title', blocks.CharBlock()),
                     ('text', blocks.RichTextBlock(features=['h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'bold', 'italic', 'link'])),
                     ('icon', blocks.StructBlock([('icon', IconChooserBlock()), ('icon_color', blocks.CharBlock())])),
                     ('images', blocks.ListBlock(ImageChooserBlock())),
                 ], template='blocks/multiimagesblock.html')),
            ('videoblock',
             blocks.StructBlock(
                 [
                     ('title', blocks.CharBlock()),
                     ('text', blocks.RichTextBlock(features=['h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'bold', 'italic', 'link'])),
                     ('icon', blocks.StructBlock([('icon', IconChooserBlock()), ('icon_color', blocks.CharBlock())])),
                     ('video', VideoChooserBlock()),
                     ('video_position', blocks.ChoiceBlock(choices=[('left', _('Left')), ('right', _('Right'))])),
                 ], template='blocks/videoblock.html')),
            ('comparingblock',
             blocks.StructBlock(
                 [
                     ('title', blocks.CharBlock()),
                     ('text', blocks.RichTextBlock(features=['h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'bold', 'italic', 'link'])),
                     ('icon', blocks.StructBlock([('icon', IconChooserBlock()), ('icon_color', blocks.CharBlock())])),
                     ('image_1', ImageChooserBlock()),
                     ('image_2', ImageChooserBlock()),
                 ], template='blocks/comparingblock.html')),
        ],
        use_json_field=True,
        verbose_name=_('Advertising block'),
    )

    last_added_products = models.ForeignKey(
        'LastAddedProducts',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    content_panels = (
        MultiFieldPanel([
            FieldPanel('title'),
            FieldPanel('sub_title'),
        ], heading=_('Home page')),
        MultiFieldPanel([
            FieldPanel('popular_products', heading=_('Popular products')),
        ], heading=_('Popular products block')),
        MultiFieldPanel([
            FieldPanel('popular_categories', heading=_('Popular categories')),
        ], heading=_('Popular categories block')),
        MultiFieldPanel([
            FieldPanel('advertising_blocks', heading=_('Advertising')),
        ], heading=_('Advertising blocks')),
        MultiFieldPanel([
            FieldPanel('last_added_products', heading=_('Last added products')),
        ], heading=_('Last added products block')),
        MultiFieldPanel([
            FieldPanel('popular_queries', heading=_('Popular queries')),
        ], heading=_('Popular queries block')),
    )


class CategoriesPage(RootPage):
    object_type = 'product.group'
    schemaorg_type = 'ItemList'
    max_count = 1
    parent_page_types = None

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('Image'),
    )

    content_panels = (
        MultiFieldPanel([
            FieldPanel('title'),
            FieldPanel('image'),
        ], heading=_('Categories page')),
    )

    def route(self, request: HttpRequest, path_components: list) -> Any:
        categories = ImageCategory.objects.filter(available=True).filter(parent_category=None)
        request.categories = categories
        return super().route(request, path_components)


class ImagesPage(RootPage):
    object_type = 'product.group'
    schemaorg_type = 'ItemList'
    max_count = 1
    parent_page_types = None

    content_panels = (
        MultiFieldPanel([
            FieldPanel('title'),
        ], heading=_('Images page')),
    )
