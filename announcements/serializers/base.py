from announcements.models import Announcement

from rest_framework.serializers import ModelSerializer, CharField


class AnnouncementBaseSerializer(ModelSerializer):
    user = CharField(
        source='user.username',
        read_only=True
    )

    class Meta:
        model = Announcement
        fields = '__all__'


class MapInfoBaseSerializer(ModelSerializer):

    class Meta:
        model = Announcement
        fields = ('id', 'latitude', 'longitude')
