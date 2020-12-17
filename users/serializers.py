import re

from django.contrib import auth

from django.utils.translation import gettext_lazy as _

from rest_framework.serializers import SerializerMethodField
from rest_framework.serializers import ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import Serializer
from rest_framework.serializers import CharField

from rest_framework.exceptions import AuthenticationFailed

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import TokenError

from .models import User


class SignUpSerializer(ModelSerializer):
    password = CharField(
        min_length=6,
        max_length=128,
        write_only=True
    )

    class Meta:
        model = User
        fields = ("email", 'username', 'password')

    def validate(self, attrs):
        """Проверяет корректность значений полей при регистрации нового пользователя."""
        email = attrs.get('email')
        username = attrs.get('username')

        username_len = len(username)
        if username_len < 3 or username_len > 64:
            raise ValidationError(
                _('Username should contain 3 to 64 characters.')
            )

        if not username.isalnum():
            raise ValidationError(
                _('Username should contain only alphanumeric characters.')
            )

        email_len = len(email)
        if email_len < 3 or email_len > 255:
            raise ValidationError(
                _('Email address should contain 3 to 255 characters.')
            )

        if not re.match(r'[a-z0-9]+@[a-z0-9]+\.[a-z0-9]+$', email):
            raise ValidationError(
                _('Invalid email address format.')
            )

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class SignInSerializer(ModelSerializer):
    email = CharField(
        min_length=3,
        max_length=255
    )
    password = CharField(
        min_length=6,
        max_length=128,
        write_only=True
    )
    username = CharField(
        min_length=3,
        max_length=64,
        read_only=True
    )
    tokens = SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'tokens')

    def get_tokens(self, current_user_instance):
        tokens = User.objects.get(email=current_user_instance['email']).tokens()
        return {
            'refresh': tokens['refresh'],
            'access': tokens['access']
        }

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed(
                _('Invalid email address or password.')
            )

        return {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens()
        }


class SignOutSerializer(Serializer):
    refresh = CharField()

    default_error_messages = {
        'error': _('Invalid token.')
    }

    def validate(self, attrs):
        self.token = attrs.get('refresh')
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('error')
