from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from . import serializers


class SignUpAPIView(generics.CreateAPIView):
    serializer_class = serializers.SignUpSerializer


class SignInAPIView(generics.GenericAPIView):
    serializer_class = serializers.SignInSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SignOutAPIView(generics.CreateAPIView):
    serializer_class = serializers.SignOutSerializer

    def post(self, request, *args, **kwargs):
        super(SignOutAPIView, self).post(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)
