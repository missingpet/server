from .serializers import AnnouncementsMapListSerializer
from .serializers import AnnouncementRetrieveSerializer


class AnnouncementsMixin:
    serializer_class = AnnouncementRetrieveSerializer
    lookup_url_kwarg = "user_id"


class AnnouncementsMapMixin:
    serializer_class = AnnouncementsMapListSerializer
    pagination_class = None
