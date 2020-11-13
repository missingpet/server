from .models import User

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import TokenError

from django.core.validators import validate_email
from django.contrib import auth


def validate_username(username):
    if not username.isalnum():
        raise serializers.ValidationError(
            'Username should contain only alphanumeric characters.'
        )
    return username


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=6,
        max_length=60,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password')

    def validate(self, attrs):
        email = attrs.get('email')
        username = attrs.get('username')
        validate_username(username)
        validate_email(email)
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class SignInSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        min_length=3,
        max_length=255
    )
    password = serializers.CharField(
        min_length=6,
        max_length=60,
        write_only=True
    )
    username = serializers.CharField(
        min_length=3,
        max_length=32,
        read_only=True
    )
    tokens = serializers.SerializerMethodField()

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
                'Invalid email address.'
            )

        return {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens()
        }


class SignOutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {'error': 'Invalid token.'}

    def validate(self, attrs):
        self.token = attrs.get('refresh')
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('error')
