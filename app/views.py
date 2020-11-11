from .serializers import *

from .permissions import IsAnnouncementAuthor

from .models import Announcement

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class SignUpAPIView(generics.GenericAPIView):
    serializer_class = SignUpSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)


class SignInAPIView(generics.GenericAPIView):
    serializer_class = SignInSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SignOutAPIView(generics.GenericAPIView):
    serializer_class = SignOutSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success': 'Выход из профиля произведён успешно.'}, status=status.HTTP_204_NO_CONTENT)


class FeedAnnouncementListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = AnnouncementRetrieveSerializer

    def get_queryset(self):
        user = self.request.user
        return Announcement.objects.exclude(user=user)


class MyAnnouncementListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = AnnouncementRetrieveSerializer
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        return Announcement.objects.filter(user=user)


class AnnouncementCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = AnnouncementCreateSerializer
    queryset = Announcement.objects.all()

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class AnnouncementDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, IsAnnouncementAuthor)
    queryset = Announcement.objects.all()


class AnnouncementRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = AnnouncementRetrieveSerializer
    queryset = Announcement.objects.all()


class FeedMapInfoListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = MapInfoSerializer

    def get_queryset(self):
        return Announcement.objects.exclude(user=self.request.user)

