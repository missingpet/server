from drf_yasg.openapi import Info
from drf_yasg.views import get_schema_view as _
from rest_framework.permissions import AllowAny


API_NAME = 'MissingPet API'


def get_schema_view(default_api_version=''):
    return _(Info(API_NAME, default_api_version), permission_classes=(AllowAny,), public=True)
