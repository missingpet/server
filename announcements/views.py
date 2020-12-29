from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated

from .models import Announcement
from .permissions import IsAnnouncementAuthorOrReadOnly
from .serializers import AnnouncementCreateSerializer
from .serializers import AnnouncementSerializer
from .serializers import MapInfoSerializer


class AllAnnouncementsListAPIView(ListAPIView):
    """Все объявления."""

    permission_classes = (AllowAny, )
    serializer_class = AnnouncementSerializer
    queryset = Announcement.objects.all()


class UserAnnouncementsListAPIView(ListAPIView):
    """Объявления пользователя."""

    permission_classes = (AllowAny, )
    serializer_class = AnnouncementSerializer
    lookup_url_kwarg = "user_id"

    def get_queryset(self):
        user_id = self.kwargs.get(self.lookup_url_kwarg)
        return Announcement.objects.filter(user_id=user_id)


class FeedAnnouncementsListAPIView(ListAPIView):
    """Лента объявлений для данного пользователя."""

    permission_classes = (AllowAny, )
    serializer_class = AnnouncementSerializer
    lookup_url_kwarg = "user_id"

    def get_queryset(self):
        user_id = self.kwargs.get(self.lookup_url_kwarg)
        return Announcement.objects.exclude(user_id=user_id)


class AnnouncementCreateAPIView(CreateAPIView):
    """Создание объявления."""

    permission_classes = (IsAuthenticated, )
    serializer_class = AnnouncementCreateSerializer
    queryset = Announcement.objects.all()

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class AnnouncementRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    serializer_class = AnnouncementSerializer
    permission_classes = (IsAnnouncementAuthorOrReadOnly, )
    queryset = Announcement.objects.all()

    def get(self, request, *args, **kwargs):
        """Получение объявления по идентификатору."""
        return super(AnnouncementRetrieveDestroyAPIView,
                     self).get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Удаление объявления."""
        return super(AnnouncementRetrieveDestroyAPIView,
                     self).delete(request, *args, **kwargs)


class AllMapInfoListAPIView(ListAPIView):
    """Список ВСЕХ объектов вида "id, широта, долгота"."""

    permission_classes = (AllowAny, )
    serializer_class = MapInfoSerializer
    pagination_class = None
    queryset = Announcement.objects.all()


class FeedMapInfoListAPIView(ListAPIView):
    """Список объектов ЛЕНТЫ вида "id, широта, долгота" для данного пользователя."""

    permission_classes = (AllowAny, )
    serializer_class = MapInfoSerializer
    pagination_class = None
    lookup_url_kwarg = "user_id"

    def get_queryset(self):
        user_id = self.kwargs.get(self.lookup_url_kwarg)
        return Announcement.objects.exclude(user_id=user_id)
