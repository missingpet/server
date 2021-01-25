from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from .models import Announcement
from .permissions import IsAnnouncementAuthorOrAuthenticatedOrReadOnly
from .serializers import AnnouncementSerializer
from .serializers import AnnouncementsMapSerializer
from .services import AnnouncementPagination


class AnnouncementViewSet(ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    pagination_class = AnnouncementPagination
    permission_classes = (IsAnnouncementAuthorOrAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class UserAnnouncementsListAPIView(ListAPIView):
    """Объявления пользователя с указанным user_id."""

    serializer_class = AnnouncementSerializer
    pagination_class = AnnouncementPagination
    lookup_field = "user_id"

    def get_queryset(self):
        return Announcement.objects.filter(
            user_id=self.kwargs[self.lookup_field])


class FeedForUserListAPIView(ListAPIView):
    """Лента объявлений для пользователя с указанным user_id."""

    serializer_class = AnnouncementSerializer
    pagination_class = AnnouncementPagination
    lookup_field = "user_id"

    def get_queryset(self):
        return Announcement.objects.exclude(
            user_id=self.kwargs[self.lookup_field])


class AnnouncementsMapListAPIView(ListAPIView):
    """Карта всех объявлений."""

    queryset = Announcement.objects.all()
    serializer_class = AnnouncementsMapSerializer


class AnnouncementsMapForUserListAPIView(ListAPIView):
    """
    Карта объявлений \
    без объявлений, созданных пользователем с указанным user_id.
    """

    serializer_class = AnnouncementsMapSerializer
    lookup_field = "user_id"

    def get_queryset(self):
        return Announcement.objects.exclude(
            user_id=self.kwargs[self.lookup_field])
