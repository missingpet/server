from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT)

from users.serializers import (SignInSerializer, SignOutSerializer,
                               SignUpSerializer)


class SignUpAPIView(GenericAPIView):
    """Регистрация нового пользователя."""

    serializer_class = SignUpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)


class SignInAPIView(GenericAPIView):
    """Вход в профиль."""

    serializer_class = SignInSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=HTTP_200_OK)


class SignOutAPIView(GenericAPIView):
    """Выход из профиля."""

    serializer_class = SignOutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_204_NO_CONTENT)
