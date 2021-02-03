from django.conf import settings
from django.conf.urls.static import static
from django.contrib.admin import sites
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

from .yasg import get_schema_view

api_urls = [
    path('', include('announcements.urls')),
    path('', include('users.urls')),
    path('swagger/',
         get_schema_view().with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns = [path('', sites.site.urls), path('api/', include(api_urls))]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += staticfiles_urlpatterns()

sites.AdminSite.site_title = 'Администрирование'
sites.AdminSite.site_header = 'Администрирование'
