import imghdr
import re

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from . import models


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    nickname = serializers.CharField(min_length=3, max_length=64)
    password = serializers.CharField(min_length=6, max_length=128, write_only=True)

    class Meta:
        model = models.User
        fields = ('email', 'nickname', 'password')

    def validate(self, data):
        email = data.get('email')
        nickname = data.get('nickname')

        if not nickname.isalnum():
            raise serializers.ValidationError('Nickname should contains only alphanumeric characters.')

        if models.User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with this email already exists.')

        return data

    def create(self, validated_data):
        return models.User.objects.create_user(**validated_data)


class TokenObtainPairCustomSerializer(TokenObtainPairSerializer):

    default_error_messages = {
        'no_active_account': 'Incorrect authentication information.'
    }


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'email', 'nickname')


class AnnouncementSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = models.Announcement
        fields = '__all__'

    def get_user(self, obj):
        user = models.Announcement.objects.get(id=obj.id).user
        return {"id": user.id, "username": user.nickname}

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

        if imghdr.what(photo) not in {'jpeg', 'png'}:
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
        model = models.Announcement
        fields = ('id', 'latitude', 'longitude')
