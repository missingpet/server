from rest_framework import viewsets, generics

from .models import Announcement
from . import permissions, serializers, services


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = serializers.AnnouncementSerializer
    pagination_class = services.AnnouncementPagination
    permission_classes = (permissions.AnnouncementPermission, )

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class BaseAnnouncementUserListAPIView(generics.ListAPIView):
    serializer_class = serializers.AnnouncementSerializer
    pagination_class = services.AnnouncementPagination
    lookup_field = 'user_id'


class UserAnnouncementsListAPIView(BaseAnnouncementUserListAPIView):
    def get_queryset(self):
        return Announcement.objects.get_announcements_of_user(
            user_id=self.kwargs.get(self.lookup_field))


class FeedForUserListAPIView(BaseAnnouncementUserListAPIView):
    def get_queryset(self):
        return Announcement.objects.get_feed_for_user(
            user_id=self.kwargs.get(self.lookup_field))


class BaseAnnouncementsMapListAPIView(generics.ListAPIView):
    serializer_class = serializers.AnnouncementsMapSerializer


class AnnouncementsMapListAPIView(BaseAnnouncementsMapListAPIView):
    queryset = Announcement.objects.all()


class AnnouncementsMapForUserListAPIView(BaseAnnouncementsMapListAPIView):
    lookup_field = "user_id"

    def get_queryset(self):
        return Announcement.objects.get_feed_for_user(
            user_id=self.kwargs.get(self.lookup_field))
