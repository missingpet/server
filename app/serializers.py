import re

from .models import User, Announcement

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from django.core.validators import validate_email
from django.contrib import auth


def validate_contact_phone_number(contact_phone_number):
    if not re.match(r'\+7\d{10}$', contact_phone_number):
        raise serializers.ValidationError('Неверный формат номера телефона.')
    return contact_phone_number


def validate_username(username):
    if not username.isalnum():
        raise serializers.ValidationError('Имя пользователя должно содержать только буквенно-цифровые символы.')
    return username


def validate_photo(photo):
    if photo:
        if photo.size > 5242880:
            raise serializers.ValidationError('Размер изображения не должен превышать 5 мегабайт.')
    return photo


def validate_place_and_coordinates(place, latitude, longitude):
    if place:
        if longitude < -180.0 or longitude > 180.0:
            raise serializers.ValidationError('Неверная долгота.')
        if latitude < -90.0 or latitude > 90.0:
            raise serializers.ValidationError('Неверная широта.')
    else:
        latitude = None
        longitude = None
    return place, latitude, longitude


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=60, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email')
        username = attrs.get('username')
        validate_username(username)
        validate_email(email)
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class SignInSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(min_length=3, max_length=255)
    password = serializers.CharField(min_length=6, max_length=60, write_only=True)
    username = serializers.CharField(min_length=3, max_length=32, read_only=True)
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

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
            raise AuthenticationFailed('Введён неверный адрес электронной почты или пароль. Попробуйте снова.')

        if not user.is_verified:
            raise AuthenticationFailed('Аккаунт не подтверждён.')

        return {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens()
        }


class SignOutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {'error': 'Токен недействителен.'}

    def validate(self, attrs):
        self.token = attrs.get('refresh')
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('TokenError')


class AnnouncementRetrieveSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Announcement
        fields = '__all__'


class AnnouncementCreateSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    photo = serializers.ImageField(allow_null=True)
    announcement_type = serializers.IntegerField()
    animal_type = serializers.IntegerField()
    place = serializers.CharField(min_length=1, max_length=500, allow_null=True)
    latitude = serializers.FloatField(allow_null=True)
    longitude = serializers.FloatField(allow_null=True)
    description = serializers.CharField(min_length=1, max_length=1000, allow_null=True)
    contact_phone_number = serializers.CharField(min_length=12, max_length=12)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Announcement
        fields = '__all__'

    def validate(self, attrs):

        longitude = attrs.get('longitude')
        latitude = attrs.get('latitude')
        place = attrs.get('place')
        photo = attrs.get('photo')
        announcement_type = attrs.get('announcement_type')
        animal_type = attrs.get('animal_type')
        contact_phone_number = attrs.get('contact_phone_number')

        _, lat, long = validate_place_and_coordinates(place, latitude, longitude)
        attrs['latitude'] = lat
        attrs['longitude'] = long
        validate_contact_phone_number(contact_phone_number)
        validate_photo(photo)

        if announcement_type not in (1, 2):
            raise serializers.ValidationError('Неверный тип объявления.')

        if animal_type not in (1, 2, 3):
            raise serializers.ValidationError('Неверный тип животного.')

        return attrs
