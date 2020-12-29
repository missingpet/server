import imghdr
import re

from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField

from .models import Announcement


class AnnouncementSerializer(ModelSerializer):
    user = SerializerMethodField()

    class Meta:
        model = Announcement
        fields = "__all__"

    def get_user(self, current_announcement_instance):
        user = Announcement.objects.get(
            id=current_announcement_instance.id).user
        return {"id": user.id, "username": user.username}


class AnnouncementCreateSerializer(AnnouncementSerializer):
    def validate(self, attrs):
        """Проверяет корректность значений всех полей объявления."""
        contact_phone_number = attrs.get("contact_phone_number")
        photo = attrs.get("photo")
        latitude = attrs.get("latitude")
        longitude = attrs.get("longitude")
        announcement_type = attrs.get("announcement_type")
        animal_type = attrs.get("animal_type")

        if not re.match(r"\+7\d{10}$", contact_phone_number):
            raise ValidationError(
                _("Contact phone number should starts with +7 and contains 12 characters total."
                  ))

        if imghdr.what(photo) not in ("jpeg", "png"):
            raise ValidationError(_("Image extension should be jpeg or png."))
        if photo.size > 5242880:
            raise ValidationError(
                _("Image size should be less than 5 megabytes."))

        if latitude < -90.0 or latitude > 90.0:
            raise ValidationError(
                _("Latitude should take value between -90,0 and 90,0."))
        if longitude < -180.0 or longitude > 180.0:
            raise ValidationError(
                _("Longitude should take value between -180,0 and 180,0."))

        if announcement_type not in (1, 2):
            raise ValidationError(
                _("Announcement type should be 1 (if you lost an animal) or 2 (if you found one)."
                  ))

        if animal_type not in (1, 2, 3):
            raise ValidationError(
                _("Animal type should be 1 (for dogs), 2 (for cats) or 3 (for other animals)."
                  ))

        return attrs


class MapInfoSerializer(ModelSerializer):
    class Meta:
        model = Announcement
        fields = ("id", "latitude", "longitude")
