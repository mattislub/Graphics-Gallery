from django import forms
from django.contrib.admin.utils import quote
from django.http import HttpRequest
from django.urls import path, reverse
from django.utils.translation import gettext_lazy as _
from wagtail import hooks
from wagtail.admin.panels import (
    FieldPanel,
    ObjectList,
    TabbedInterface,
)
from wagtail.admin.ui.tables import (
    BulkActionsCheckboxColumn,
    Column,
    TitleColumn,
    UpdatedAtColumn,
)
from wagtail.admin.viewsets.base import ViewSet
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.chooser import (
    ChooseResultsView,
    ChooseView,
    SnippetChooserViewSet,
)
from wagtail.snippets.views.snippets import (
    IndexView,
    SnippetViewSet,
    SnippetViewSetGroup,
)

from shop import models, views


class ImageCategoryViewSet(SnippetViewSet):
    icon = 'heroicons-collection-outline'

    model = models.ImageCategory
    menu_label = _('Categories')
    menu_name = _('Categories')

    url_prefix = 'shop/additionally/categories'


class ImageOrientationViewSet(SnippetViewSet):
    icon = 'heroicons-template-outline'

    model = models.ImageOrientation
    menu_label = _('Image orientations')
    menu_name = _('Image orientations')

    url_prefix = 'shop/additionally/image-orientations'


# ImageProduct
class ImageProductIndexView(IndexView):
    model = models.ImageProduct

    @property
    def image_information_column(self) -> Column:
        return Column(
            'information',
            label=_('Information'),
            accessor='information',
        )

    @property
    def image_column(self) -> Column:
        return Column(
            'image',
            label=_('Image'),
            accessor='admin_preview',
        )

    @property
    def name_column(self) -> TitleColumn:
        return TitleColumn(
            'name',
            label=_('Name'),
            accessor='name',
            get_url=self.get_edit_url,
        )

    @property
    def price_column(self) -> Column:
        return Column(
            'price',
            label=_('Price'),
            accessor='price',
        )

    @property
    def code_column(self) -> Column:
        return Column(
            'code',
            label=_('Code'),
            accessor='code',
        )

    @property
    def category_column(self) -> Column:
        return Column(
            'category',
            label=_('Category'),
            accessor='category',
        )

    @property
    def orientation_column(self) -> Column:
        return Column(
            'orientation',
            label=_('Orientation'),
            accessor='orientation',
        )

    @property
    def columns(self) -> list:
        return [BulkActionsCheckboxColumn('bulk_actions', obj_type='snippet'), self.image_column, self.name_column, self.code_column, self.price_column, self.category_column, self.orientation_column, self.image_information_column, UpdatedAtColumn()]


class ImageProductChooseView(ChooseView):
    model = models.ImageProduct

    @property
    def image_column(self) -> Column:
        return Column(
            'image',
            label=_('Image'),
            accessor='admin_preview',
        )

    @property
    def name_column(self) -> TitleColumn:
        return TitleColumn(
            'name',
            label=_('Name'),
            accessor='name',
            get_url=(
                lambda obj: self.append_preserved_url_parameters(
                    reverse(self.chosen_url_name, args=(quote(obj.pk),)),
                )
            ),
            link_attrs={'data-chooser-modal-choice': True},
        )

    @property
    def price_column(self) -> Column:
        return TitleColumn(
            'price',
            label=_('Price'),
            accessor='price',
            get_url=(
                lambda obj: self.append_preserved_url_parameters(
                    reverse(self.chosen_url_name, args=(quote(obj.pk),)),
                )
            ),
            link_attrs={'data-chooser-modal-choice': True},
        )

    @property
    def code_column(self) -> TitleColumn:
        return TitleColumn(
            'code',
            label=_('Code'),
            accessor='code',
            get_url=(
                lambda obj: self.append_preserved_url_parameters(
                    reverse(self.chosen_url_name, args=(quote(obj.pk),)),
                )
            ),
            link_attrs={'data-chooser-modal-choice': True},
        )

    @property
    def category_column(self) -> TitleColumn:
        return TitleColumn(
            'category',
            label=_('Category'),
            accessor='category',
            get_url=(
                lambda obj: self.append_preserved_url_parameters(
                    reverse(self.chosen_url_name, args=(quote(obj.pk),)),
                )
            ),
            link_attrs={'data-chooser-modal-choice': True},
        )

    @property
    def orientation_column(self) -> TitleColumn:
        return TitleColumn(
            'orientation',
            label=_('Orientation'),
            accessor='orientation',
            get_url=(
                lambda obj: self.append_preserved_url_parameters(
                    reverse(self.chosen_url_name, args=(quote(obj.pk),)),
                )
            ),
            link_attrs={'data-chooser-modal-choice': True},
        )

    @property
    def columns(self) -> list:
        return [self.image_column, self.name_column, self.code_column, self.price_column, self.category_column, self.orientation_column]


class ImageProductChooseResultsView(ChooseResultsView):
    model = models.ImageProduct

    @property
    def image_column(self) -> Column:
        return Column(
            'image',
            label=_('Image'),
            accessor='admin_preview',
        )

    @property
    def name_column(self) -> TitleColumn:
        return TitleColumn(
            'name',
            label=_('Name'),
            accessor='name',
            get_url=(
                lambda obj: self.append_preserved_url_parameters(
                    reverse(self.chosen_url_name, args=(quote(obj.pk),)),
                )
            ),
            link_attrs={'data-chooser-modal-choice': True},
        )

    @property
    def price_column(self) -> TitleColumn:
        return TitleColumn(
            'price',
            label=_('Price'),
            accessor='price',
            get_url=(
                lambda obj: self.append_preserved_url_parameters(
                    reverse(self.chosen_url_name, args=(quote(obj.pk),)),
                )
            ),
            link_attrs={'data-chooser-modal-choice': True},
        )

    @property
    def code_column(self) -> TitleColumn:
        return TitleColumn(
            'code',
            label=_('Code'),
            accessor='code',
            get_url=(
                lambda obj: self.append_preserved_url_parameters(
                    reverse(self.chosen_url_name, args=(quote(obj.pk),)),
                )
            ),
            link_attrs={'data-chooser-modal-choice': True},
        )

    @property
    def category_column(self) -> TitleColumn:
        return TitleColumn(
            'category',
            label=_('Category'),
            accessor='category',
            get_url=(
                lambda obj: self.append_preserved_url_parameters(
                    reverse(self.chosen_url_name, args=(quote(obj.pk),)),
                )
            ),
            link_attrs={'data-chooser-modal-choice': True},
        )

    @property
    def orientation_column(self) -> TitleColumn:
        return TitleColumn(
            'orientation',
            label=_('Orientation'),
            accessor='orientation',
            get_url=(
                lambda obj: self.append_preserved_url_parameters(
                    reverse(self.chosen_url_name, args=(quote(obj.pk),)),
                )
            ),
            link_attrs={'data-chooser-modal-choice': True},
        )

    @property
    def columns(self) -> list:
        return [self.image_column, self.name_column, self.code_column, self.price_column, self.category_column, self.orientation_column]


class ImageProductChooserViewSet(SnippetChooserViewSet):
    model = models.ImageProduct

    choose_view_class = ImageProductChooseView
    choose_results_view_class = ImageProductChooseResultsView


class ImageProductViewSet(SnippetViewSet):

    icon = 'heroicons-document-outline'
    model = models.ImageProduct
    menu_label = _('Image products')
    menu_name = _('Image products')

    url_prefix = 'shop/image-products'
    list_filter = ('category', 'orientation', 'premium', 'subscription_plans')

    index_view_class = ImageProductIndexView
    chooser_viewset_class = ImageProductChooserViewSet

    edit_handler = TabbedInterface([
        ObjectList([FieldPanel('name'), FieldPanel('description'), FieldPanel('image'), FieldPanel('price'), FieldPanel('downloads', read_only=True)], heading=_('Info')),
        ObjectList([FieldPanel('category'), FieldPanel('orientation')], heading=_('Details')),
        ObjectList([FieldPanel('tags')], heading=_('Tags')),
        ObjectList([FieldPanel('premium'), FieldPanel('subscription_plans', widget=forms.CheckboxSelectMultiple)], heading=_('Advanced')),
    ])


class BalanceProductViewSet(SnippetViewSet):
    icon = 'heroicons-currency-dollar-outline'
    model = models.BalanceProduct
    menu_label = _('Balance product')
    menu_name = _('Balance product')

    url_prefix = 'shop/balance-products'
    list_filter = ('price', 'replenishment', 'available')

    panels = (
        FieldPanel('main_text'),
        FieldPanel('help_text'),
        FieldPanel('badge_text'),
        FieldPanel('price'),
        FieldPanel('replenishment'),
        FieldPanel('available'),
    )


class LoadProductsViewSet(ViewSet):
    icon = 'upload'

    name = 'load_products'
    menu_label = _('Load products')
    menu_name = _('Load products')

    url_prefix = 'shop/load-products'

    def get_urlpatterns(self) -> list:
        return [
            path('', views.load_products_preview, name='load-products'),
            path('table/', views.load_products_table, name='load-products-table'),
        ]


class EarningViewSet(ViewSet):
    icon = 'heroicons-cash-outline'

    name = 'earning'
    menu_label = _('Earning')
    menu_name = _('Earning')

    url_prefix = 'earning'

    add_to_admin_menu = True
    menu_order = 3

    def get_urlpatterns(self) -> list:
        return [
            path('', views.EarningReportView.as_view(), name='earning'),
        ]


class SubscriptionPlanViewSet(SnippetViewSet):
    icon = 'heroicons-shopping-bag-outline'

    model = models.SubscriptionPlan
    menu_label = _('Subscription plan')
    menu_name = _('Subscription plan')

    url_prefix = 'shop/additionally/subscription-plan'


class UserSubscriptionViewSet(SnippetViewSet):
    menu_order = 601
    icon = 'heroicons-user-add-outline'

    # exclude_form_fields = ['start_date', 'end_date', 'downloads_remaining']
    model = models.UserSubscription
    menu_label = _('User subscription')
    menu_name = _('User subscription')
    add_to_settings_menu = True

    url_prefix = 'user/user-subscription'


class AdditionallyShopViewSetGroup(SnippetViewSetGroup):
    items = (ImageCategoryViewSet, ImageOrientationViewSet)
    menu_icon = 'heroicons-adjustments-outline'
    menu_label = _('Additionally')
    menu_name = _('Additionally')
    add_to_admin_menu = False


class ShopViewSetGroup(SnippetViewSetGroup):
    menu_order = 1
    items = (LoadProductsViewSet, ImageProductViewSet, BalanceProductViewSet, SubscriptionPlanViewSet, AdditionallyShopViewSetGroup)
    menu_icon = 'heroicons-clipboard-list-solid'
    menu_label = _('Shop')
    menu_name = _('Shop')


register_snippet(UserSubscriptionViewSet)
register_snippet(ShopViewSetGroup)
register_snippet(EarningViewSet)


@hooks.register('construct_main_menu')
def hide_menu_items(request: HttpRequest, menu_items: list) -> None:
    menu_items[:] = [menu_item for menu_item in menu_items if menu_item.name not in {'reports', 'help'}]


@hooks.register('construct_settings_menu')
def hide_settings_menu_items(request: HttpRequest, menu_items: list) -> None:
    menu_items[:] = [menu_item for menu_item in menu_items if menu_item.name not in {'redirects', 'workflows', 'workflow-tasks', 'groups'}]
