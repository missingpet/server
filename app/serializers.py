import re
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import User, Announcement
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


# -------------------------------------------------------- Auth --------------------------------------------------------
class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=60, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'photo', 'password']

    def validate(self, attrs):
        email = attrs['email']
        username = attrs['username']
        photo = attrs['photo']

        if photo:
            if photo.size > 5242880:
                raise serializers.ValidationError({'error': 'Размер изображения не должен превышать 5 мегабайт.'})

        if not username.isalnum():
            raise serializers.ValidationError(
                {'error': 'Имя пользователя должно содержать только буквенно-цифровые символы.'}
            )

        email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if not re.match(email_regex, email):
            raise serializers.ValidationError({'error': 'Некорректный формат адреса электронной почты.'})

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(min_length=3, max_length=255)
    password = serializers.CharField(min_length=6, max_length=60, write_only=True)
    username = serializers.CharField(min_length=3, max_length=32, read_only=True)
    photo = serializers.ImageField(read_only=True)
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'photo', 'tokens']

    def get_tokens(self, current_user_instance):
        tokens = User.objects.get(email=current_user_instance['email']).tokens()
        return {
            'refresh': tokens['refresh'],
            'access': tokens['access']
        }

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
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
            'photo': user.photo,
            'tokens': user.tokens()
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {'error': 'Токен недействителен.'}

    def validate(self, attrs):
        self.token = attrs['refresh']
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
        email = attrs['email']

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
            uidb64 = attrs['uidb64']
            token = attrs['token']
            password = attrs['password']

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed({'error': 'Данная ссылка больше недействительна.'})

            user.set_password(password)
            user.save()

            return user

        except Exception:
            raise AuthenticationFailed({'error': 'Что-то пошло не так.'})


# ---------------------------------------------------- Announcement ----------------------------------------------------
class AnnouncementSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Announcement
        fields = '__all__'


class AnnouncementCreateSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    title = serializers.CharField(min_length=1, max_length=50)
    photo = serializers.ImageField(allow_null=True)
    announcement_type = serializers.IntegerField()
    breed = serializers.CharField(min_length=1, max_length=50, allow_null=True)
    age = serializers.IntegerField(allow_null=True)
    place = serializers.CharField(min_length=1, max_length=500, allow_null=True)
    latitude = serializers.FloatField(allow_null=True)
    longitude = serializers.FloatField(allow_null=True)
    description = serializers.CharField(min_length=1, max_length=500, allow_null=True)
    contact_phone_number = serializers.CharField(min_length=11, max_length=12, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    at_home = serializers.BooleanField()

    class Meta:
        model = Announcement
        fields = '__all__'

    def validate(self, attrs):

        longitude = attrs['longitude']
        latitude = attrs['latitude']
        place = attrs['place']
        photo = attrs['photo']
        announcement_type = attrs['announcement_type']
        age = attrs['age']
        contact_phone_number = attrs['contact_phone_number']

        if place:
            if longitude < -180.0 or longitude > 180.0:
                raise ValidationError({'error': 'Неверная долгота.'})

            if latitude < -90.0 or latitude > 90.0:
                raise ValidationError({'error': 'Неверная широта.'})
        else:
            attrs['latitude'] = None
            attrs['longitude'] = None

        if age:
            if age < 0:
                raise ValidationError({'error': 'Возраст животного не может быть отрицательным.'})

        if contact_phone_number:
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

        if not announcement_type in (1, 2):
            raise ValidationError({'error': 'Неверный тип объявления.'})

        return attrs

