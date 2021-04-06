import re
import imghdr
import time

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSlidingSerializer

from . import models


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        min_length=6,
        max_length=128,
    )
    email = serializers.EmailField()
    code = serializers.IntegerField()

    def validate(self, attrs):
        code = attrs.get('code')
        email = attrs.get('email')

        try:
            user = models.User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                'Пользователь с таким адресом электронной почты не найден')
        else:
            try:
                password_reset_confirmation_code = models.PasswordResetConfirmationCode.objects.get(
                    user=user,
                    code=code,
                )
            except ObjectDoesNotExist:
                raise serializers.ValidationError(
                    'Неправильный код сброса пароля')
            else:
                if round(time.time()) > password_reset_confirmation_code.expired_in:
                    raise serializers.ValidationError(
                        'Код подтверждения больше недействителен')

        return attrs

    def save(self):
        email = self.validated_data['email']
        code = self.validated_data['code']

        code_object = models.PasswordResetConfirmationCode.objects.get(
            user=models.User.objects.get(email=email),
            code=code,
        )
        code_object.delete()


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')

        try:
            models.User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                'Пользователь с таким адресом электронной почты не найден')

        return attrs


class SettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Settings
        fields = (
            'id',
            'settings_name',
            'actual_app_version_ios',
            'min_app_version_ios',
        )


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
                "Имя пользователя должно содержать только буквенно-цифровые символы"
            )

        try:
            models.User.objects.get(email=email)
        except ObjectDoesNotExist:
            pass
        else:
            raise serializers.ValidationError(
                'Пользователь с таким адресом электронной почты уже зарегистирован')

        return attrs

    def create(self, validated_data):
        return models.User.objects.create_user(**validated_data)


class AuthSerializer(TokenObtainSlidingSerializer):

    default_error_messages = {
        "no_active_account":
        "Аккаунт с предоставленными учетными данными не найден"
    }

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
                'Номер телефона обязан начинаться с +7 и должен содержать ровно 12 символов'
            )

        if imghdr.what(photo) not in settings.ALLOWED_UPLOAD_IMAGE_EXTENSIONS:
            raise serializers.ValidationError(
                'Неправильное расширение изображения')

        if photo.size > settings.MAX_PHOTO_UPLOAD_SIZE:
            raise serializers.ValidationError(
                f"Размер изображения не должен превышать {settings.MAX_PHOTO_UPLOAD_SIZE} байт"
            )

        if latitude < -90.0 or latitude > 90.0:
            raise serializers.ValidationError("Неверное значение широты")
        if longitude < -180.0 or longitude > 180.0:
            raise serializers.ValidationError("Неверное значение долготы")

        if announcement_type not in (1, 2):
            raise serializers.ValidationError('Неверный тип объявления')

        if animal_type not in (1, 2, 3):
            raise serializers.ValidationError("Неверный тип животного")

        return attrs


class AnnouncementsMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Announcement
        fields = ("id", "latitude", "longitude")
