from .serializers import SignInSerializer
from .serializers import SignUpSerializer
from .serializers import SignOutSerializer

from rest_framework.generics import GenericAPIView

from rest_framework.status import HTTP_201_CREATED
from rest_framework.status import HTTP_200_OK
from rest_framework.status import HTTP_204_NO_CONTENT

from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny


class SignUpAPIView(GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)


class SignInAPIView(GenericAPIView):
    serializer_class = SignInSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=HTTP_200_OK)


class SignOutAPIView(GenericAPIView):
    serializer_class = SignOutSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_204_NO_CONTENT)
