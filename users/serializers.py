from .models import User

from rest_framework.serializers import SerializerMethodField
from rest_framework.serializers import ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import EmailField
from rest_framework.serializers import Serializer
from rest_framework.serializers import CharField

from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import TokenError

from django.contrib import auth


class SignUpSerializer(ModelSerializer):
    password = CharField(
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

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class SignInSerializer(ModelSerializer):
    email = EmailField(
        min_length=3,
        max_length=255
    )
    password = CharField(
        min_length=6,
        max_length=60,
        write_only=True
    )
    username = CharField(
        min_length=3,
        max_length=32,
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
                'Invalid email address.'
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
        'error': 'Invalid token.'
    }

    def validate(self, attrs):
        self.token = attrs.get('refresh')
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('error')
