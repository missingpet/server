from .serializers import *

from .permissions import IsAnnouncementAuthor

from .models import Announcement

from rest_framework.generics import ListAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import RetrieveAPIView

from rest_framework.permissions import IsAuthenticated


class FeedAnnouncementListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = AnnouncementRetrieveSerializer

    def get_queryset(self):
        return Announcement.objects.exclude(user=self.request.user)


class MyAnnouncementListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = AnnouncementRetrieveSerializer
    pagination_class = None

    def get_queryset(self):
        return Announcement.objects.filter(user=self.request.user)


class AnnouncementCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = AnnouncementCreateSerializer
    queryset = Announcement.objects.all()

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class AnnouncementDeleteAPIView(DestroyAPIView):
    permission_classes = (IsAnnouncementAuthor, )
    queryset = Announcement.objects.all()


class AnnouncementRetrieveAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = AnnouncementRetrieveSerializer
    queryset = Announcement.objects.all()


class FeedMapInfoListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = FeedMapInfoSerializer
    pagination_class = None

    def get_queryset(self):
        return Announcement.objects.exclude(user=self.request.user).exclude(address__isnull=True)
