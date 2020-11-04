import re
from .models import User, Announcement
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=60, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email',)
        username = attrs.get('username',)

        if not username.isalnum():
            raise serializers.ValidationError(
                {'error': 'Имя пользователя должно содержать только буквенно-цифровые символы.'}
            )

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
        email = attrs.get('email',)
        password = attrs.get('password',)
        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed(
                {'error': 'Введён неверный адрес электронной почты или пароль. Попробуйте снова.'}
            )

        if not user.is_verified:
            raise AuthenticationFailed({'error': 'Адрес электронной почты не подтверждён.'})

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
        self.token = attrs.get('refresh',)
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('error')


class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=3, max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email',)

        if not User.objects.filter(email=email).exists():
            raise ValidationError({'error': 'Неверный адрес электронной почты.'})

        return attrs


class CompletePasswordResetSerializer(serializers.Serializer):
    uidb64 = serializers.CharField(min_length=1, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    password = serializers.CharField(min_length=6, max_length=60, write_only=True)

    class Meta:
        fields = ['uidb64', 'token', 'password']

    def validate(self, attrs):
        try:
            uidb64 = attrs.get('uidb64',)
            token = attrs.get('token',)
            password = attrs.get('password',)

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed({'error': 'Данная ссылка больше недействительна.'})

            user.set_password(password)
            user.save()

            return user

        except Exception:
            raise AuthenticationFailed({'error': 'Что-то пошло не так.'})


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
    description = serializers.CharField(min_length=1, max_length=500, allow_null=True)
    contact_phone_number = serializers.CharField(min_length=11, max_length=12)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Announcement
        fields = '__all__'

    def validate(self, attrs):

        longitude = attrs.get('longitude',)
        latitude = attrs.get('latitude',)
        place = attrs.get('place',)
        photo = attrs.get('photo',)
        announcement_type = attrs.get('announcement_type',)
        animal_type = attrs.get('animal_type',)
        contact_phone_number = attrs.get('contact_phone_number',)

        if place:
            if longitude < -180.0 or longitude > 180.0:
                raise ValidationError({'error': 'Неверная долгота.'})
            if latitude < -90.0 or latitude > 90.0:
                raise ValidationError({'error': 'Неверная широта.'})
        else:
            attrs['latitude'] = None
            attrs['longitude'] = None

        if contact_phone_number.startswith('8'):
            if len(contact_phone_number) != 11:
                raise ValidationError({'error': 'Неверный формат номера телефона.'})
        elif contact_phone_number.startswith('+7'):
            if len(contact_phone_number) != 12:
                raise ValidationError({'error': 'Неверный формат номера телефона.'})
        else:
            raise ValidationError({'error': 'Неверный формат номера телефона.'})

        if photo:
            if photo.size > 5242880:
                raise ValidationError({'error': 'Размер изображения не должен превышать 5 мегабайт.'})

        if announcement_type not in (1, 2):
            raise ValidationError({'error': 'Неверный тип объявления.'})

        if animal_type not in (1, 2, 3):
            raise ValidationError({'error': 'Неверный тип животного.'})

        return attrs


class AnnouncementMapInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id', 'latitude', 'longitude']

