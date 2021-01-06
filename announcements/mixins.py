from rest_framework.pagination import PageNumberPagination

from .serializers import AnnouncementsMapListSerializer
from .serializers import AnnouncementRetrieveSerializer


class AnnouncementPaginationMixin:
    pagination_class = PageNumberPagination
    pagination_class.page_size = 5


class AnnouncementsMixin:
    serializer_class = AnnouncementRetrieveSerializer
    lookup_url_kwarg = "user_id"


class AnnouncementsMapMixin:
    serializer_class = AnnouncementsMapListSerializer
    pagination_class = None
