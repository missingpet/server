from rest_framework.views import APIView
from rest_framework import viewsets, generics
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework.renderers import TemplateHTMLRenderer

from . import models
from . import serializers
from .pagination_service import AnnouncementPagination
from .permissions import AnnouncementPermission


class AuthView(TokenObtainPairView):
    """Use to authenticate users."""

    serializer_class = serializers.AuthSerializer
    permission_classes = (AllowAny, )


class UserCreateView(generics.CreateAPIView):
    """Use to create a new user."""

    queryset = models.User
    serializer_class = serializers.UserCreateSerializer
    permission_classes = (AllowAny, )


class AnnouncementViewSet(viewsets.ModelViewSet):
    """Use to create a new announcement,
    retrieve/delete an announcement with given id or to get the whole announcements list."""

    queryset = models.Announcement.objects.all()
    serializer_class = serializers.AnnouncementSerializer
    permission_classes = (AnnouncementPermission,)
    pagination_class = AnnouncementPagination

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class BaseAnnouncementUserListView(generics.ListAPIView):
    """Base announcement user view to extend in subclasses."""

    serializer_class = serializers.AnnouncementSerializer
    permission_classes = (AllowAny, )
    pagination_class = AnnouncementPagination
    lookup_field = 'user_id'


class UserAnnouncementsListView(BaseAnnouncementUserListView):
    """Use to get announcements that belong to user with given user id."""

    def get_queryset(self):
        return models.Announcement.objects.get_announcements_of_user(self.kwargs.get(self.lookup_field))


class FeedForUserListView(BaseAnnouncementUserListView):
    """Use to get feed for user with given user id
    (Announcements that belong to this user are excluded)."""

    def get_queryset(self):
        return models.Announcement.objects.get_feed_for_user(self.kwargs.get(self.lookup_field))


class BaseAnnouncementsMapListView(generics.ListAPIView):
    """Base announcements map view to extend in subclasses."""

    serializer_class = serializers.AnnouncementsMapSerializer
    permission_classes = (AllowAny, )


class AnnouncementsMapListView(BaseAnnouncementsMapListView):
    """Use to get the whole announcements map."""

    queryset = models.Announcement.objects.all()


class AnnouncementsMapForUserListView(BaseAnnouncementsMapListView):
    """Use to get announcements map without announcements
    that belong to user with given user id."""

    lookup_field = "user_id"

    def get_queryset(self):
        return models.Announcement.objects.get_feed_for_user(self.kwargs.get(self.lookup_field))


class SetNewPasswordView(APIView):
    """Use to set new password for user.
    Not implemented yet."""

    serializer_class = serializers.SetNewPasswordSerializer
    renderer_classes = (TemplateHTMLRenderer, )
    template_name = 'set_new_password.html'

    def post(self, request):
        pass
