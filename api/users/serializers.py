from django.contrib import auth
from rest_framework import exceptions
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import User


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    username = serializers.CharField(min_length=3, max_length=64)
    password = serializers.CharField(min_length=6, max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password')

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')

        if not username.isalnum():
            raise serializers.ValidationError('Username should contains only alphanumeric characters.')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with this email already exists.')

        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class SignInSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6, max_length=128, write_only=True)
    username = serializers.CharField(min_length=3, max_length=64, read_only=True)
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "email", "password", "username", "tokens")

    def get_tokens(self, obj):
        tokens = User.objects.get(id=obj["id"]).tokens()
        return {"refresh": tokens["refresh"], "access": tokens["access"]}

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        user = auth.authenticate(email=email, password=password)

        if not user:
            raise exceptions.AuthenticationFailed("Invalid email and/or password.")

        return {
            'id': user.id,
            "email": user.email,
            "username": user.username,
            "tokens": user.tokens(),
        }


class SignOutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {"token_error": "Invalid token."}

    def save(self):
        try:
            RefreshToken(self.validated_data['refresh']).blacklist()
        except TokenError:
            self.fail("token_error")
