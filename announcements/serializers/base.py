from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import CharField

from ..models import Announcement


class AnnouncementBaseSerializer(ModelSerializer):
    user = CharField(
        source='user.username',
        read_only=True
    )

    class Meta:
        model = Announcement
        fields = '__all__'
