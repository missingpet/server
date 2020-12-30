from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT)
from rest_framework_simplejwt.views import TokenRefreshView

from .serializers import SignInSerializer, SignOutSerializer, SignUpSerializer


class SignUpAPIView(GenericAPIView):
    """Регистрация нового пользователя."""

    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_summary="Регистрирация пользователя.",
        operation_description="Регистрирует нового пользователя.",
        responses={
            "201": SignUpSerializer,
            "400": """
                Пользователь с таким именем или адресом электронной почты уже существует.
                
                Неверный формат имени и/или адреса электронной почты.
                
                Слишком короткий пароль, имя пользователя или адрес электронной почты.
                """,
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)


class SignInAPIView(GenericAPIView):
    """Вход в профиль."""

    serializer_class = SignInSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_summary="Авторизация пользователя.",
        operation_description="Регистрирует нового пользователя.",
        responses={
            "200": SignInSerializer,
            "403": "Неверный адрес электронной почты или пароль.",
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=HTTP_200_OK)


class SignOutAPIView(GenericAPIView):
    """Выход из профиля."""

    serializer_class = SignOutSerializer
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_summary="Выход из профиля пользователя.",
        operation_description="Производит выход из профиля.",
        responses={
            "204": "Это успех, refresh токен сброшен.",
            "400": "Недопустимый токен.",
            "403": "Учетные данные не были предоставлены.",
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_204_NO_CONTENT)


class TokenRefreshAPIView(TokenRefreshView):
    """Обновление access токена по refresh токену."""

    @swagger_auto_schema(
        operation_summary="Обновление токена доступа.",
        operation_description="Обновляет access токен по заданному refresh токену.",
        responses={"200": "Это успех.", "401": "Токен недействителен или просрочен."},
    )
    def post(self, request, *args, **kwargs):
        return super(TokenRefreshAPIView, self).post(request, *args, **kwargs)
