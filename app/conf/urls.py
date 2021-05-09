"""
URL configuration module.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.admin import sites
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include
from django.urls import path
from django.urls import re_path
from drf_yasg.openapi import Info
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    Info('MissingPet API', 'v1'),
    permission_classes=(AllowAny, ),
    public=True,
)

api_versioned_urls = [
    path("", include("pet.urls")),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0)),
]

api_urls = [
    re_path("(?P<version>(v1))/", include(api_versioned_urls)),
    path("", include("rest_framework.urls", namespace="rest_framework")),
]

urlpatterns = [path("", sites.site.urls), path("api/", include(api_urls))]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += staticfiles_urlpatterns()
