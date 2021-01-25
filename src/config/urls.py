from django.conf import settings
from django.conf.urls.static import static
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.sites import site
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include
from django.urls import path
from drf_yasg.openapi import Info
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    Info(title="MissingPet API", default_version=""),
    public=True,
)

api_urls = [
    path("", include("announcements.urls")),
    path("", include("users.urls")),
    path("", include("rest_framework.urls", namespace="rest_framework")),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]

urlpatterns = [path("", site.urls), path("api/", include(api_urls))]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += staticfiles_urlpatterns()

AdminSite.site_title = "Администрирование"
AdminSite.site_header = "Администрирование"
