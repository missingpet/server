from rest_framework import viewsets
from rest_framework import generics

from announcements.models import Announcement
from announcements import permissions, serializers, services


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = serializers.AnnouncementSerializer
    pagination_class = services.AnnouncementPagination
    permission_classes = (permissions.IsAnnouncementAuthorOrAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class BaseAnnouncementUserListAPIView(generics.ListAPIView):
    serializer_class = serializers.AnnouncementSerializer
    pagination_class = services.AnnouncementPagination
    lookup_field = 'user_id'


class UserAnnouncementsListAPIView(BaseAnnouncementUserListAPIView):
    def get_queryset(self):
        return Announcement.objects.filter(
            user_id=self.kwargs.get(self.lookup_field))


class FeedForUserListAPIView(BaseAnnouncementUserListAPIView):
    def get_queryset(self):
        return Announcement.objects.exclude(
            user_id=self.kwargs.get(self.lookup_field))


class BaseAnnouncementsMapListAPIView(generics.ListAPIView):
    serializer_class = serializers.AnnouncementsMapSerializer


class AnnouncementsMapListAPIView(BaseAnnouncementsMapListAPIView):
    queryset = Announcement.objects.all()


class AnnouncementsMapForUserListAPIView(BaseAnnouncementsMapListAPIView):
    lookup_field = "user_id"

    def get_queryset(self):
        return Announcement.objects.exclude(
            user_id=self.kwargs.get(self.lookup_field))
