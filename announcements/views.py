from rest_framework.generics import ListAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Announcement
from .permissions import IsAnnouncementAuthorOrReadOnly
from .serializers import AnnouncementCreateSerializer
from .serializers import AnnouncementSerializer
from .serializers import MapInfoSerializer


class UserAnnouncementsListAPIView(ListAPIView):
    """Объявления пользователя."""

    serializer_class = AnnouncementSerializer
    lookup_url_kwarg = "user_id"

    def get_queryset(self):
        return Announcement.objects.filter(
            user_id=self.kwargs.get(self.lookup_url_kwarg)
        )


class AnnouncementListCreateAPIView(ListCreateAPIView):
    """Получение списка всех объявлений/Создание объявления."""

    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Announcement.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return AnnouncementSerializer
        return AnnouncementCreateSerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class AnnouncementRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    """Получение/удаление объявления."""

    serializer_class = AnnouncementSerializer
    permission_classes = (IsAnnouncementAuthorOrReadOnly,)
    queryset = Announcement.objects.all()


class AllMapInfoListAPIView(ListAPIView):
    """
    Список всех объектов вида "id, широта, долгота".
    Это нужно для маркеров на карте объявлений.
    """

    serializer_class = MapInfoSerializer
    queryset = Announcement.objects.all()
    pagination_class = None


class FeedMapInfoListAPIView(ListAPIView):
    """
    Список объектов вида "id, широта, долгота" из ленты для заданного пользователя.
    Это нужно для маркеров на карте объявлений.
    """

    serializer_class = MapInfoSerializer
    lookup_url_kwarg = "user_id"
    pagination_class = None

    def get_queryset(self):
        return Announcement.objects.exclude(
            user_id=self.kwargs.get(self.lookup_url_kwarg)
        )


class FeedAnnouncementsListAPIView(ListAPIView):
    """Лента объявлений для заданного пользователя."""

    serializer_class = AnnouncementSerializer
    lookup_url_kwarg = "user_id"

    def get_queryset(self):
        return Announcement.objects.exclude(
            user_id=self.kwargs.get(self.lookup_url_kwarg)
        )
