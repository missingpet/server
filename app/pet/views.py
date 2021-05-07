from django.conf import settings
from django.utils.decorators import method_decorator
from ratelimit.decorators import ratelimit
from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainSlidingView

from . import const, models, serializers
from .email_logic import send_message
from .exceptions import (
    catch_smtp_exception_for_view,
    catch_rate_limit_exceeded_exception_for_view,
)
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
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = self.validate(request)

        request.user.nickname = data["nickname"]
        request.user.save()

        return Response()


class AuthView(TokenObtainSlidingView):
    """Авторизация пользователя"""

    serializer_class = serializers.AuthSerializer
    permission_classes = (AllowAny,)


class UserCreateView(generics.CreateAPIView):
    """Регистрация пользователя"""

    queryset = models.User
    serializer_class = serializers.UserCreateSerializer
    permission_classes = (AllowAny,)


class PasswordResetRequestView(ValidateAPIView):
    """Запрос на сброс пароля"""

    serializer_class = serializers.PasswordResetRequestSerializer
    permission_classes = (AllowAny,)

    @catch_smtp_exception_for_view
    @catch_rate_limit_exceeded_exception_for_view
    @method_decorator(
        ratelimit(key="ip", rate=settings.SEND_EMAIL_RATE_LIMIT, block=True)
    )
    def post(self, request, *args, **kwargs):
        data = self.validate(request)

        user = models.User.objects.get(email=data["email"])

        code = models.PasswordResetConfirmationCode.objects.create(user=user)

        send_message(
            const.PASSWORD_RESET_REQUEST_SUBJECT,
            const.PASSWORD_RESET_REQUEST_BODY.format(user.nickname, code.code),
            user.email,
        )

        return Response(
            data={
                "success": const.PASSWORD_RESET_CONFIRM_SUCCESS_MESSAGE.format(
                    user.email
                )
            },
            status=status.HTTP_201_CREATED,
        )


class PasswordResetConfirmView(ValidateAPIView):
    """Подтверждение сброса пароля"""

    serializer_class = serializers.PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        data = self.validate(request)

        user = models.User.objects.get(email=data["email"])

        models.PasswordResetConfirmationCode.objects.get(
            user=user,
            code=data["code"],
        ).delete()

        user.set_password(data["new_password"])
        user.save()

        return Response(
            data={"success": "Пароль успешно сброшен"},
            status=status.HTTP_204_NO_CONTENT,
        )


class SettingsView(generics.GenericAPIView):
    """Получение актуальных настроек мобильного приложения"""

    permission_classes = (AllowAny,)
    serializer_class = serializers.SettingsSerializer

    def get(self, request, *args, **kwargs):
        actual_settings = models.Settings.objects.get_actual()
        if not actual_settings:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"settings_not_set_error": "Настройки не установлены"},
            )
        serializer = self.serializer_class(actual_settings)

        return Response(serializer.data)


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
    permission_classes = (AnnouncementPermission,)
    pagination_class = AnnouncementPagination

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class BaseAnnouncementUserListView(generics.ListAPIView):
    serializer_class = serializers.AnnouncementSerializer
    permission_classes = (AllowAny,)
    pagination_class = AnnouncementPagination
    lookup_field = "user_id"


class UserAnnouncementsListView(BaseAnnouncementUserListView):
    """Получение списка объявлений принадлежащих пользователю с указанным user_id"""

    def get_queryset(self):
        queryset = models.Announcement.objects.filter(
            user_id=self.kwargs.get(self.lookup_field)
        )
        return queryset


class FeedForUserListView(BaseAnnouncementUserListView):
    """Получение ленты объявлений для пользователя с указанным user_id"""

    def get_queryset(self):
        queryset = models.Announcement.objects.exclude(
            user_id=self.kwargs.get(self.lookup_field)
        )
        return queryset


class BaseMapListView(generics.ListAPIView):
    serializer_class = serializers.AnnouncementsMapSerializer
    permission_classes = (AllowAny,)


class MapListView(BaseMapListView):
    """Получение всей карты объявлений"""

    queryset = models.Announcement.objects.all()


class MapForUserListView(BaseMapListView):
    """Получение карты объявлений из ленты для пользователя с указанным user_id"""

    lookup_field = "user_id"

    def get_queryset(self):
        queryset = models.Announcement.objects.exclude(
            user_id=self.kwargs.get(self.lookup_field)
        )
        return queryset
