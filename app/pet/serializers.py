"""
Serializers module.
"""
import imghdr
import re
import time

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSlidingSerializer

from . import models


def validate_nickname(nickname: str) -> str:
    if not nickname.isalnum():
        raise serializers.ValidationError(
            "Имя пользователя должно содержать только буквенно-цифровые символы"
        )
    return nickname


class UserNicknameChangeSerializer(serializers.Serializer):
    nickname = serializers.CharField(min_length=3, max_length=64)

    def validate(self, attrs):
        nickname = attrs.get("nickname")
        validate_nickname(nickname)
        return attrs


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

        validate_nickname(nickname)

        try:
            models.User.objects.get(email=email)
        except ObjectDoesNotExist:
            pass
        else:
            raise serializers.ValidationError(
                "Пользователь с таким адресом электронной почты уже зарегистирован"
            )

        return attrs

    def create(self, validated_data):
        return models.User.objects.create_user(**validated_data)


class AuthSerializer(TokenObtainSlidingSerializer):

    default_error_messages = {
        "no_active_account": "Аккаунт с предоставленными учетными данными не найден"
    }

    def validate(self, attrs):
        data = super(AuthSerializer, self).validate(attrs)
        data.update(
            {
                "id": self.user.id,
                "email": self.user.email,
                "nickname": self.user.nickname,
            }
        )
        return data


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        min_length=6,
        max_length=128,
    )
    email = serializers.EmailField()
    code = serializers.IntegerField()

    def validate(self, attrs):
        code = attrs.get("code")
        email = attrs.get("email")

        try:
            user = models.User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                "Пользователь с таким адресом электронной почты не найден"
            )
        else:
            try:
                password_reset_confirmation_code = (
                    models.PasswordResetConfirmationCode.objects.get(
                        user=user,
                        code=code,
                    )
                )
            except ObjectDoesNotExist:
                raise serializers.ValidationError("Неправильный код сброса пароля")
            else:
                if round(time.time()) > password_reset_confirmation_code.expired_in:
                    raise serializers.ValidationError(
                        "Код подтверждения больше недействителен"
                    )

        return attrs


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get("email")

        try:
            models.User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                "Пользователь с таким адресом электронной почты не найден"
            )

        return attrs


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Settings
        fields = (
            "id",
            "settings_name",
            "actual_app_version_ios",
            "min_app_version_ios",
        )


class AnnouncementSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = models.Announcement
        fields = "__all__"

    def get_user(self, obj):
        user = obj.user
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
                "Номер телефона обязан начинаться с +7 и должен содержать ровно 12 символов"
            )

        if imghdr.what(photo) not in settings.ALLOWED_UPLOAD_IMAGE_EXTENSIONS:
            raise serializers.ValidationError("Неправильное расширение изображения")
        if photo.size > settings.MAX_PHOTO_UPLOAD_SIZE:
            raise serializers.ValidationError(
                "Размер изображения не должен превышать {} байт".format(
                    settings.MAX_PHOTO_UPLOAD_SIZE
                )
            )

        if not (-90.0 <= latitude <= 90.0):
            raise serializers.ValidationError("Неправильное значение широты")
        if not (-180.0 <= longitude <= 180.0):
            raise serializers.ValidationError("Неправильное значение долготы")

        if announcement_type not in models.AnnouncementType.values:
            raise serializers.ValidationError("Неправильный тип объявления")

        if animal_type not in models.AnimalType.values:
            raise serializers.ValidationError("Неправильный тип животного")

        return attrs


class AnnouncementsMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Announcement
        fields = ("id", "latitude", "longitude")
