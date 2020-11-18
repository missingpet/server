from rest_framework.generics import ListAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import RetrieveAPIView

from rest_framework.permissions import IsAuthenticated

from ..permissions import IsAnnouncementAuthor

from ..models import Announcement

from ..serializers import *

from .base import AnnouncementBaseListAPIView


class FeedAnnouncementListAPIView(AnnouncementBaseListAPIView):
    """
    Лента объявлений.
    """
    def get_queryset(self):
        return Announcement.objects.exclude(user=self.request.user)


class MyAnnouncementListAPIView(AnnouncementBaseListAPIView):
    """
    Объявления пользователя.
    """
    pagination_class = None

    def get_queryset(self):
        return Announcement.objects.filter(user=self.request.user)


class AnnouncementCreateAPIView(CreateAPIView):
    """
    Создание нового объявления.
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = AnnouncementCreateSerializer
    queryset = Announcement.objects.all()

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class AnnouncementDestroyAPIView(DestroyAPIView):
    """
    Удаление объявления.
    """
    permission_classes = (IsAnnouncementAuthor, )
    queryset = Announcement.objects.all()


class AnnouncementRetrieveAPIView(RetrieveAPIView):
    """
    Получение конкретного объявления по id.
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = AnnouncementRetrieveSerializer
    queryset = Announcement.objects.all()


class FeedMapInfoListAPIView(ListAPIView):
    """
    Список всех объектов вида "id, широта, долгота" из ленты объявлений.
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = MapInfoSerializer
    pagination_class = None

    def get_queryset(self):
        return Announcement.objects.exclude(user=self.request.user).exclude(address__isnull=True)
