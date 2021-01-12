from django.conf import settings
from django.conf.urls.static import static
from django.contrib.admin.sites import AdminSite, site
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from drf_yasg.openapi import Info
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    Info(title="MissingPet API", default_version=""),
    public=True,
)

urlpatterns = [
    path("", site.urls),
    path("api/", include("announcements.urls")),
    path("api/", include("users.urls")),
    path("api/", include("rest_framework.urls", namespace="rest_framework")),
    path(
        "api/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += staticfiles_urlpatterns()

AdminSite.site_title = "MissingPet CMS"
AdminSite.site_header = "MissingPet CMS"
