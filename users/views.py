from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.status import HTTP_204_NO_CONTENT

from .serializers import SignInSerializer
from .serializers import SignOutSerializer
from .serializers import SignUpSerializer


class SignUpAPIView(CreateAPIView):
    """Регистрация нового пользователя."""

    serializer_class = SignUpSerializer


class SignInAPIView(GenericAPIView):
    """Вход в профиль."""

    serializer_class = SignInSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=HTTP_200_OK)


class SignOutAPIView(CreateAPIView):
    """Выход из профиля."""

    serializer_class = SignOutSerializer

    def create(self, request, *args, **kwargs):
        super(SignOutAPIView, self).create(request, *args, *kwargs)
        return Response(status=HTTP_204_NO_CONTENT)
