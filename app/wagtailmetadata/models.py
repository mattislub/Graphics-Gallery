from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _
from wagtail.images import get_image_model_string
from django.contrib.auth import get_user_model
from wagtail.admin.panels import FieldPanel
from meta import settings as meta_settings
from django.http import HttpRequest
from meta.models import ModelMeta
from django.conf import settings
from wagtail.models import Site
from django.db import models
from meta import utils
import datetime
from typing import (
    ClassVar,
    Any,
)


class MetadataMixin(ModelMeta):
    class Author:
        fb_url = meta_settings.META_FB_AUTHOR_URL
        twitter_profile = meta_settings.META_TWITTER_AUTHOR
        schemaorg_profile = None

        def get_full_name(self) -> str | None:
            return None

    context_meta_name = "meta"

    object_type: str | None = None
    schemaorg_type: str | None = None
    custom_namespace: str | None = None

    _metadata_default: ClassVar[dict] = {
        "use_og": "use_og",
        "use_twitter": "use_twitter",
        "use_schemaorg": "use_schemaorg",
        "use_title_tag": "use_title_tag",
        "title": "get_meta_title",
        "description": "get_meta_description",
        "keywords": "get_meta_keywords",
        "url": "get_meta_url",
        "image": "get_meta_image",
        "object_type": "get_meta_object_type",
        "site_name": "get_meta_site_name",
        "twitter_site": "get_meta_twitter_site",
        "twitter_creator": "get_meta_twitter_creator",
        "twitter_card": "get_meta_twitter_card",
        "og_author": "get_author_url",
        "og_publisher": meta_settings.META_FB_PUBLISHER,
        "facebook_app_id": meta_settings.META_FB_APPID,
        "fb_pages": meta_settings.META_FB_PAGES,
        "locale": "get_meta_locale",
        "schemaorg_type": "get_meta_schemaorg_type",
        "custom_namespace": "get_meta_custom_namespace",
        "get_domain": "get_domain",
    }

    @property
    def use_og(self) -> bool:
        return meta_settings.USE_OG_PROPERTIES

    @property
    def use_twitter(self) -> bool:
        return meta_settings.USE_TWITTER_PROPERTIES

    @property
    def use_schemaorg(self) -> bool:
        return meta_settings.USE_SCHEMAORG_PROPERTIES

    @property
    def use_title_tag(self) -> str | None:
        return None

    def get_meta_title(self) -> str | None:
        return None

    def get_meta_description(self) -> str | None:
        return None

    def get_meta_keywords(self) -> list[str]:
        return []

    def get_meta_url(self) -> str | None:
        return None

    def get_meta_image(self) -> str | None:
        if bool(meta_settings.DEFAULT_IMAGE) is True:
            return self.build_absolute_uri(meta_settings.DEFAULT_IMAGE)
        return None

    def get_meta_object_type(self) -> str:
        return self.object_type or meta_settings.SITE_TYPE

    def get_meta_schemaorg_type(self) -> str:
        return self.schemaorg_type or meta_settings.SCHEMAORG_TYPE

    def get_meta_site_name(self) -> str:
        request = utils.get_request()
        site = getattr(request, "site", None)
        if request and isinstance(site, Site):
            if bool(request.site.site_name) is True:
                return request.site.site_name

        site = self.get_site()
        if isinstance(site, Site):
            if bool(site.site_name) is True:
                return site.site_name

        if request:
            site = Site.find_for_request(request)
            if isinstance(site, Site):
                return site.site_name

        return settings.WAGTAIL_SITE_NAME

    def get_meta_twitter_site(self) -> str:
        return meta_settings.TWITTER_SITE

    def get_meta_twitter_creator(self) -> Any:
        return self.get_author_twitter()

    def get_meta_twitter_card(self) -> str:
        if self.get_meta_image() is not None:
            return "summary_large_image"
        return "summary"

    def get_meta_locale(self) -> str:
        return getattr(settings, "LANGUAGE_CODE", "en_US")

    def get_meta_custom_namespace(self) -> str:
        return self.custom_namespace or meta_settings.OG_NAMESPACES

    def get_domain(self) -> str:
        request = utils.get_request()
        if request and getattr(request, "site", None):
            return request.site.hostname

        site = self.get_site()
        if site is not None:
            if bool(site.hostname) is True:
                return site.hostname

        if not meta_settings.SITE_DOMAIN:
            raise ImproperlyConfigured("META_SITE_DOMAIN is not set")

        return meta_settings.SITE_DOMAIN

    def get_author(self) -> Author:
        return MetadataMixin.Author()

    def build_absolute_uri(self, url: str) -> str:
        request = utils.get_request()
        if request is not None:
            return request.build_absolute_uri(url)

        if url.startswith("http"):
            return url

        site = self.get_site()
        if site is not None:
            return "{}{}".format(site.root_url, url if url.startswith("/") else "/" + url)

        raise NotImplementedError

    def get_context(self, request: HttpRequest) -> dict:
        context = super().get_context(request)
        context[self.context_meta_name] = self.as_meta(request)

        return context


class MetadataPageMixin(MetadataMixin, models.Model):

    search_image = models.ForeignKey(
        get_image_model_string(),
        verbose_name=_("Search image"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    promote_panels: ClassVar[list] = [FieldPanel("search_image")]

    _metadata: ClassVar[dict] = {
        "published_time": "published_time",
        "modified_time": "latest_revision_created_at",
        "expiration_time": "expire_at",
    }

    class Meta:
        abstract = True

    @property
    def published_time(self) -> datetime.datetime:
        return self.go_live_at or self.first_published_at

    def get_meta_title(self) -> str:
        return self.seo_title or self.title

    def get_meta_description(self) -> str:
        return self.search_description

    def get_meta_keywords(self) -> list[str]:
        return []

    def get_meta_url(self) -> str:
        return self.build_absolute_uri(self.url)

    def get_meta_image(self) -> str | None:
        if self.search_image is not None:
            return self.build_absolute_uri(
                self.search_image.get_rendition(getattr(settings, "META_SEARCH_IMAGE_RENDITION", "fill-800x450")).url,
            )
        return super().get_meta_image()

    def get_author(self) -> MetadataMixin.Author:
        author = super().get_author()
        if hasattr(self, "owner") and isinstance(self.owner, get_user_model()):
            author.get_full_name = self.owner.get_full_name  # type: ignore
        return author
