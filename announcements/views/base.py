from rest_framework.permissions import IsAuthenticated

from rest_framework.generics import ListAPIView

from announcements.serializers import AnnouncementRetrieveSerializer


class AnnouncementBaseListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = AnnouncementRetrieveSerializer
