from .serializers import *

from .permissions import IsAnnouncementAuthor

from .models import Announcement

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


class FeedAnnouncementListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = AnnouncementRetrieveSerializer

    def get_queryset(self):
        return Announcement.objects.exclude(user=self.request.user)


class MyAnnouncementListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = AnnouncementRetrieveSerializer
    pagination_class = None

    def get_queryset(self):
        return Announcement.objects.filter(user=self.request.user)


class AnnouncementCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = AnnouncementCreateSerializer
    queryset = Announcement.objects.all()

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class AnnouncementDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, IsAnnouncementAuthor)
    queryset = Announcement.objects.all()


class AnnouncementRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = AnnouncementRetrieveSerializer
    queryset = Announcement.objects.all()


class FeedMapInfoListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = FeedMapInfoSerializer
    pagination_class = None

    def get_queryset(self):
        return Announcement.objects.exclude(user=self.request.user).exclude(address__isnull=True)
