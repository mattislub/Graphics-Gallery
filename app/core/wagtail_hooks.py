from django.utils.translation import gettext_lazy as _  # type: ignore
from wagtail.snippets.models import register_snippet  # type: ignore
from wagtail.snippets.views.snippets import SnippetViewSet  # type: ignore

from core import models


class NewsletterViewSet(SnippetViewSet):
    model = models.Newsletter
    menu_label = _("Newsletter")
    menu_name = _("Newsletter")
    add_to_admin_menu = True
    icon = 'heroicons-newspaper-outline'


register_snippet(NewsletterViewSet)
