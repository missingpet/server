import imghdr
import re

from rest_framework import serializers

from .models import Announcement


class AnnouncementSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Announcement
        fields = '__all__'

    def get_user(self, obj):
        user = Announcement.objects.get(id=obj.id).user
        return {"id": user.id, "username": user.username}

    def validate(self, data):
        contact_phone_number = data.get("contact_phone_number")
        photo = data.get("photo")
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        announcement_type = data.get("announcement_type")
        animal_type = data.get("animal_type")

        if not re.match(r"\+7\d{10}$", contact_phone_number):
            raise serializers.ValidationError(
                "Contact phone number should starts with +7 and contains 12 characters total.")

        if imghdr.what(photo) not in {"jpeg", "png"}:
            raise serializers.ValidationError("Image extension should be jpeg or png.")
        if photo.size > 5242880:
            raise serializers.ValidationError(
                "Image size should be less than 5 megabytes.")

        if latitude < -90.0 or latitude > 90.0:
            raise serializers.ValidationError(
                "Latitude should take value between -90,0 and 90,0.")
        if longitude < -180.0 or longitude > 180.0:
            raise serializers.ValidationError(
                "Longitude should take value between -180,0 and 180,0.")

        if announcement_type not in {1, 2}:
            raise serializers.ValidationError(
                "Announcement type should be 1 (if you lost an animal) or 2 (if you found one).")

        if animal_type not in {1, 2, 3}:
            raise serializers.ValidationError(
                "Animal type should be 1 (for dogs), 2 (for cats) or 3 (for other animals).")

        return data


class AnnouncementsMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ("id", "latitude", "longitude")
