from django.contrib import auth
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.serializers import (CharField, EmailField, IntegerField,
                                        ModelSerializer, Serializer,
                                        SerializerMethodField, ValidationError)
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import User


class SignUpSerializer(ModelSerializer):
    """Регистрация нового пользователя."""

    email = EmailField()
    username = CharField(min_length=3, max_length=64)
    password = CharField(min_length=6, max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ("email", "username", "password")

    def validate(self, attrs):
        email = attrs.get("email")
        username = attrs.get("username")

        if not username.isalnum():
            raise ValidationError(
                _("Username should contains only alphanumeric characters.")
            )

        if User.objects.filter(email=email).first():
            raise ValidationError(_("User with this email already exists."))

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class SignInSerializer(ModelSerializer):
    """Вход в профиль."""

    id = IntegerField(read_only=True)
    email = EmailField()
    password = CharField(min_length=6, max_length=128, write_only=True)
    username = CharField(min_length=3, max_length=64, read_only=True)
    tokens = SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "email", "password", "username", "tokens")

    def get_tokens(self, current_user_instance):
        tokens = User.objects.get(id=current_user_instance["id"]).tokens()
        return {"refresh": tokens["refresh"], "access": tokens["access"]}

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed(_("Invalid email address or password."))

        return {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "tokens": user.tokens(),
        }


class SignOutSerializer(Serializer):
    """Выход из профиля."""

    refresh = CharField()

    default_error_messages = {"error": _("Invalid token.")}

    def save(self, **kwargs):
        try:
            RefreshToken(self.validated_data.get("refresh")).blacklist()
        except TokenError:
            self.fail("error")
