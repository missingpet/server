from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainSlidingView

from . import const, models, serializers
from .email_logic import send_email_message
from .exceptions import catch_smtp_exception_for_view
from .pagination import AnnouncementPagination
from .permissions import AnnouncementPermission


class AuthView(TokenObtainSlidingView):
    """Авторизация пользователя"""

    serializer_class = serializers.AuthSerializer
    permission_classes = (AllowAny,)


class UserCreateView(generics.CreateAPIView):
    """Регистрация пользователя"""

    queryset = models.User
    serializer_class = serializers.UserCreateSerializer
    permission_classes = (AllowAny,)


class PasswordResetRequestView(generics.GenericAPIView):
    """Запрос на сброс пароля"""

    serializer_class = serializers.PasswordResetRequestSerializer
    permission_classes = (AllowAny,)

    @catch_smtp_exception_for_view
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = models.User.objects.get(
            email=serializer.validated_data["email"],
        )

        models.PasswordResetConfirmationCode.objects.filter(
            user=user,
        ).delete()

        code = models.PasswordResetConfirmationCode.objects.create(
            user=user,
        )

        email_message_data = {
            "subject": const.PASSWORD_RESET_REQUEST_SUBJECT,
            "body": const.PASSWORD_RESET_REQUEST_BODY.format(
                user.nickname,
                code.code,
            ),
            "recipient": user.email,
        }
        send_email_message(**email_message_data)

        return Response(
            data={
                "success": const.PASSWORD_RESET_CONFIRM_SUCCESS_MESSAGE.format(
                    user.email
                )
            },
            status=status.HTTP_201_CREATED,
        )


class PasswordResetConfirmView(generics.GenericAPIView):
    """Подтверждение сброса пароля"""

    serializer_class = serializers.PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        validated_data = serializer.validated_data

        user = models.User.objects.get(email=validated_data["email"])
        user.set_password(validated_data["new_password"])
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
