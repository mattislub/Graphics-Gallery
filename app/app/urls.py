from django.conf import settings  # type: ignore
from django.contrib import admin  # type: ignore
from django.urls import include, path  # type: ignore
from wagtail import urls as wagtail_urls  # type: ignore
from wagtail.admin import urls as wagtailadmin_urls  # type: ignore
from wagtail.documents import urls as wagtaildocs_urls  # type: ignore
from wagtailautocomplete.urls.admin import (  # type: ignore
    urlpatterns as autocomplete_admin_urls,  # type: ignore
)

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path("admin/autocomplete/", include(autocomplete_admin_urls)),

    path('__reload__/', include('django_browser_reload.urls')),

    path('', include('shop.urls')),
    path('', include('pages.urls')),
    path('', include('social_django.urls', namespace='social')),
    path('api/', include('salesman.urls')),
]


if settings.DEBUG:
    from django.conf.urls.static import static  # type: ignore
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns  # type: ignore

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('', include(wagtail_urls)),
]
