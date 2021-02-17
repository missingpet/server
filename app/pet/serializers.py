import re

from django.conf import settings
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from . import models


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    nickname = serializers.CharField(min_length=3, max_length=64)
    password = serializers.CharField(
        min_length=6,
        max_length=128,
        write_only=True,
    )

    class Meta:
        model = models.User
        fields = ("email", "nickname", "password")

    def validate(self, attrs):
        email = attrs.get("email")
        nickname = attrs.get("nickname")

        if not nickname.isalnum():
            raise serializers.ValidationError(
                "Nickname should contains only alphanumeric characters.")

        if models.User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "User with this email already exists.")

        return attrs

    def create(self, validated_data):
        return models.User.objects.create_user(**validated_data)


class AuthSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(AuthSerializer, self).validate(attrs)
        data.update({
            "id": self.user.id,
            "email": self.user.email,
            "nickname": self.user.nickname,
        })
        return data


class AnnouncementSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = models.Announcement
        fields = "__all__"

    def get_user(self, obj):
        user = models.Announcement.objects.get(id=obj.id).user
        return {"id": user.id, "nickname": user.nickname}

    def validate(self, attrs):
        contact_phone_number = attrs.get("contact_phone_number")
        photo = attrs.get("photo")
        latitude = attrs.get("latitude")
        longitude = attrs.get("longitude")
        announcement_type = attrs.get("announcement_type")
        animal_type = attrs.get("animal_type")

        if not re.match(r"\+7\d{10}$", contact_phone_number):
            raise serializers.ValidationError(
                "Contact phone number should starts with +7 and contains 12 characters total."
            )

        if photo.size > settings.MAX_PHOTO_UPLOAD_SIZE:
            raise serializers.ValidationError(
                f"Image size should be less than {settings.MAX_PHOTO_UPLOAD_SIZE} bytes."
            )

        if latitude < -90.0 or latitude > 90.0:
            raise serializers.ValidationError(
                "Latitude should take value between -90,0 and 90,0.")
        if longitude < -180.0 or longitude > 180.0:
            raise serializers.ValidationError(
                "Longitude should take value between -180,0 and 180,0.")

        if announcement_type not in {1, 2}:
            raise serializers.ValidationError(
                "Announcement type should be 1 (if you lost an animal) or 2 (if you found one)."
            )

        if animal_type not in {1, 2, 3}:
            raise serializers.ValidationError(
                "Animal type should be 1 (for dogs), 2 (for cats) or 3 (for other animals)."
            )

        return attrs


class AnnouncementsMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Announcement
        fields = ("id", "latitude", "longitude")
