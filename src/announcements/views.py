from rest_framework import generics, viewsets

from .models import Announcement
from . import permissions, serializers, services


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = serializers.AnnouncementSerializer
    pagination_class = services.AnnouncementPagination
    permission_classes = (permissions.IsAnnouncementAuthorOrAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class UserAnnouncementsListAPIView(generics.ListAPIView):
    serializer_class = serializers.AnnouncementSerializer
    pagination_class = services.AnnouncementPagination
    lookup_field = "user_id"

    def get_queryset(self):
        return Announcement.objects.filter(
            user_id=self.kwargs.get(self.lookup_field))


class FeedForUserListAPIView(generics.ListAPIView):
    serializer_class = serializers.AnnouncementSerializer
    pagination_class = services.AnnouncementPagination
    lookup_field = "user_id"

    def get_queryset(self):
        return Announcement.objects.exclude(
            user_id=self.kwargs.get(self.lookup_field))


class AnnouncementsMapListAPIView(generics.ListAPIView):
    queryset = Announcement.objects.all()
    serializer_class = serializers.AnnouncementsMapSerializer


class AnnouncementsMapForUserListAPIView(generics.ListAPIView):
    serializer_class = serializers.AnnouncementsMapSerializer
    lookup_field = "user_id"

    def get_queryset(self):
        return Announcement.objects.exclude(
            user_id=self.kwargs.get(self.lookup_field))
