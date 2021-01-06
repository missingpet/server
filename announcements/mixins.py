from rest_framework.pagination import PageNumberPagination

from .serializers import AnnouncementsMapListSerializer
from .serializers import AnnouncementRetrieveSerializer


class AnnouncementPaginationMixin:
    """Пагинация объявлений."""

    pagination_class = PageNumberPagination
    pagination_class.page_size = 5


class AnnouncementsMixin:
    """Список объявлений."""

    serializer_class = AnnouncementRetrieveSerializer
    lookup_url_kwarg = "user_id"


class AnnouncementsMapMixin:
    """Карта объявлений."""

    serializer_class = AnnouncementsMapListSerializer
    pagination_class = None
