from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Announcement
from .permissions import IsAnnouncementAuthor
from .serializers import (AnnouncementCreateSerializer,
                          AnnouncementRetrieveSerializer, MapInfoSerializer)


class AllAnnouncementListAPIView(ListAPIView):
    """Лента всех объявлений."""

    permission_classes = (AllowAny,)
    serializer_class = AnnouncementRetrieveSerializer
    queryset = Announcement.objects.all()


class FeedAnnouncementListAPIView(ListAPIView):
    """Лента объявлений без объявлений пользователя."""

    permission_classes = (IsAuthenticated,)
    serializer_class = AnnouncementRetrieveSerializer

    def get_queryset(self):
        return Announcement.objects.exclude(user=self.request.user)


class MyAnnouncementListAPIView(ListAPIView):
    """Объявления пользователя."""

    permission_classes = (IsAuthenticated,)
    serializer_class = AnnouncementRetrieveSerializer
    pagination_class = None

    def get_queryset(self):
        return Announcement.objects.filter(user=self.request.user)


class AnnouncementCreateAPIView(CreateAPIView):
    """Создание нового объявления."""

    permission_classes = (IsAuthenticated,)
    serializer_class = AnnouncementCreateSerializer
    queryset = Announcement.objects.all()

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class AnnouncementDestroyAPIView(DestroyAPIView):
    """Удаление объявления."""

    permission_classes = (IsAnnouncementAuthor,)
    queryset = Announcement.objects.all()


class AnnouncementRetrieveAPIView(RetrieveAPIView):
    """Получение конкретного объявления по id."""

    permission_classes = (AllowAny,)
    serializer_class = AnnouncementRetrieveSerializer
    queryset = Announcement.objects.all()


class AllMapInfoListAPIView(ListAPIView):
    """
    Список всех объектов вида "id, широта, долгота"
    из ленты всех объявлений.
    """

    permission_classes = (AllowAny,)
    serializer_class = MapInfoSerializer
    pagination_class = None
    queryset = Announcement.objects.all()


class FeedMapInfoListAPIView(ListAPIView):
    """
    Список всех объектов вида "id, широта, долгота"
    из ленты объявлений без объявлений пользователя.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = MapInfoSerializer
    pagination_class = None

    def get_queryset(self):
        return Announcement.objects.exclude(user=self.request.user)
