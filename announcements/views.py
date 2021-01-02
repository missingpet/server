from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveDestroyAPIView)
from rest_framework.permissions import IsAuthenticated

from .models import Announcement
from .permissions import IsAnnouncementAuthorOrReadOnly
from .serializers import (AnnouncementCreateSerializer, AnnouncementSerializer,
                          MapInfoSerializer)


class AllAnnouncementsListAPIView(ListAPIView):
    """Все объявления."""

    serializer_class = AnnouncementSerializer
    queryset = Announcement.objects.all()


class UserAnnouncementsListAPIView(ListAPIView):
    """Объявления пользователя."""

    serializer_class = AnnouncementSerializer
    lookup_url_kwarg = "user_id"

    def get_queryset(self):
        return Announcement.objects.filter(
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


class AnnouncementCreateAPIView(CreateAPIView):
    """Создание объявления."""

    permission_classes = (IsAuthenticated,)
    serializer_class = AnnouncementCreateSerializer
    queryset = Announcement.objects.all()

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
    Список объектов ленты вида "id, широта, долгота" для заданного пользователя.
    Это нужно для маркеров на карте объявлений.
    """

    serializer_class = MapInfoSerializer
    lookup_url_kwarg = "user_id"
    pagination_class = None

    def get_queryset(self):
        return Announcement.objects.exclude(
            user_id=self.kwargs.get(self.lookup_url_kwarg)
        )
