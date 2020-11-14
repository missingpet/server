from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.urls import path, include

from drf_yasg.openapi import Info
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
    Info(
        title='MissingPet API',
        default_version=''
    ),
    public=True,
)

urlpatterns = [
    path('', admin.site.urls),
    path(
        'api/',
        include('announcements.urls')
    ),
    path(
        'api/auth/',
        include('users.urls')
    ),
    path(
        'api/',
        include('rest_framework.urls', namespace='rest_framework')
    ),
    path(
        'api/swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += staticfiles_urlpatterns()
