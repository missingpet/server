from rest_framework.generics import ListAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Announcement
from .permissions import IsAnnouncementAuthorOrReadOnly
from .serializers import AnnouncementCreateSerializer
from .serializers import AnnouncementRetrieveSerializer
from .serializers import ObjectsForAnnouncementsMapRetrieveSerializer


class UserAnnouncementsListAPIView(ListAPIView):
    """Объявления пользователя."""

    serializer_class = AnnouncementRetrieveSerializer
    lookup_url_kwarg = "user_id"

    def get_queryset(self):
        return Announcement.objects.filter(
            user_id=self.kwargs.get(self.lookup_url_kwarg))


class AnnouncementListCreateAPIView(ListCreateAPIView):
    """Получение списка всех объявлений/Создание объявления."""

    serializer_class = AnnouncementCreateSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = Announcement.objects.all()

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class AnnouncementRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    """Получение/удаление объявления."""

    serializer_class = AnnouncementRetrieveSerializer
    permission_classes = (IsAnnouncementAuthorOrReadOnly, )
    queryset = Announcement.objects.all()


class AllObjectsForAnnouncementsMapListAPIView(ListAPIView):
    """
    Список всех объектов вида "id, широта, долгота".
    Это нужно для маркеров на карте объявлений.
    """

    serializer_class = ObjectsForAnnouncementsMapRetrieveSerializer
    queryset = Announcement.objects.all()
    pagination_class = None


class ObjectsForAnnouncementsMapForUserFeedListAPIView(ListAPIView):
    """
    Список объектов вида "id, широта, долгота" из ленты для заданного пользователя.
    Это нужно для маркеров на карте объявлений.
    """

    serializer_class = ObjectsForAnnouncementsMapRetrieveSerializer
    lookup_url_kwarg = "user_id"
    pagination_class = None

    def get_queryset(self):
        return Announcement.objects.exclude(
            user_id=self.kwargs.get(self.lookup_url_kwarg))


class FeedAnnouncementsListAPIView(ListAPIView):
    """Лента объявлений для заданного пользователя."""

    serializer_class = AnnouncementRetrieveSerializer
    lookup_url_kwarg = "user_id"

    def get_queryset(self):
        return Announcement.objects.exclude(
            user_id=self.kwargs.get(self.lookup_url_kwarg))
