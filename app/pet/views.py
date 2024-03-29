"""
Module which contains controllers implementation.
"""
from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainSlidingView

from . import models
from . import serializers
from .pagination import AnnouncementPagination
from .permissions import AnnouncementPermission


class ValidateAPIView(generics.GenericAPIView):
    def validate(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data


class UserNicknameChangeView(ValidateAPIView):
    """Изменение имени пользователя"""

    serializer_class = serializers.UserNicknameChangeSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        data = self.validate(request)

        request.user.nickname = data["nickname"]
        request.user.save()

        return Response()


class AuthView(TokenObtainSlidingView):
    """Авторизация пользователя"""

    serializer_class = serializers.AuthSerializer
    permission_classes = (AllowAny, )


class UserCreateView(generics.CreateAPIView):
    """Регистрация пользователя"""

    queryset = models.User
    serializer_class = serializers.UserCreateSerializer
    permission_classes = (AllowAny, )


class AnnouncementViewSet(viewsets.ModelViewSet):
    """
    create:
    Создание объявления

    retrieve:
    Получение объявления по идентификатору

    destroy:
    Удаление объявления

    list:
    Получение списка всех объявлений
    """

    queryset = models.Announcement.objects.all()
    serializer_class = serializers.AnnouncementSerializer
    permission_classes = (AnnouncementPermission, )
    pagination_class = AnnouncementPagination

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class BaseAnnouncementUserListView(generics.ListAPIView):
    serializer_class = serializers.AnnouncementSerializer
    permission_classes = (AllowAny, )
    pagination_class = AnnouncementPagination
    lookup_field = "user_id"


class UserAnnouncementsListView(BaseAnnouncementUserListView):
    """Получение списка объявлений принадлежащих пользователю с указанным user_id"""
    def get_queryset(self):
        queryset = models.Announcement.objects.filter(
            user_id=self.kwargs.get(self.lookup_field))
        return queryset


class FeedForUserListView(BaseAnnouncementUserListView):
    """Получение ленты объявлений для пользователя с указанным user_id"""
    def get_queryset(self):
        queryset = models.Announcement.objects.exclude(
            user_id=self.kwargs.get(self.lookup_field))
        return queryset


class BaseMapListView(generics.ListAPIView):
    serializer_class = serializers.AnnouncementsMapSerializer
    permission_classes = (AllowAny, )


class MapListView(BaseMapListView):
    """Получение всей карты объявлений"""

    queryset = models.Announcement.objects.all()


class MapForUserListView(BaseMapListView):
    """Получение карты объявлений из ленты для пользователя с указанным user_id"""

    lookup_field = "user_id"

    def get_queryset(self):
        queryset = models.Announcement.objects.exclude(
            user_id=self.kwargs.get(self.lookup_field))
        return queryset
