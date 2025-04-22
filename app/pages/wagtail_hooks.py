from django.utils.translation import gettext_lazy as _  # type: ignore
from wagtail.snippets.models import register_snippet  # type: ignore
from wagtail.snippets.views.snippets import (  # type: ignore
    SnippetViewSet,
    SnippetViewSetGroup,
)

from pages import models


class PopularProductsViewSet(SnippetViewSet):
    model = models.PopularProducts
    menu_label = _('Popular product')
    menu_name = _('Popular product')


class PopularCategoriesViewSet(SnippetViewSet):
    model = models.PopularCategories
    menu_label = _('Popular category')
    menu_name = _('Popular category')


class SimilarProductsViewSet(SnippetViewSet):
    model = models.SimilarProducts
    menu_label = _('Similar product')
    menu_name = _('Similar product')


class LastAddedProductsViewSet(SnippetViewSet):
    model = models.LastAddedProducts
    menu_label = _('Last added product')
    menu_name = _('Last added product')


class PopularQueriesViewSet(SnippetViewSet):
    model = models.PopularQueries
    menu_label = _('Popular query')
    menu_name = _('Popular query')


class PagesSnippetsViewSetGroup(SnippetViewSetGroup):
    items = (PopularProductsViewSet, PopularCategoriesViewSet, SimilarProductsViewSet, LastAddedProductsViewSet, PopularQueriesViewSet)
    menu_icon = 'heroicons-puzzle-outline'
    menu_label = _('Page snippet')
    menu_name = _('Page snippet')


register_snippet(PagesSnippetsViewSetGroup)
