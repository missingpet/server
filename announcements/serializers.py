import re
import imghdr

from .models import Announcement

from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import ValidationError
from rest_framework.serializers import DateTimeField
from rest_framework.serializers import FloatField
from rest_framework.serializers import IntegerField
from rest_framework.serializers import ImageField
from rest_framework.serializers import CharField


def validate_contact_phone_number(contact_phone_number):
    if not re.match(r'\+7\d{10}$', contact_phone_number):
        raise ValidationError('Wrong phone number format.')
    return contact_phone_number


def validate_photo(photo):
    if imghdr.what(photo) not in ('jpeg', 'png'):
        raise ValidationError('Image extension should be jpeg or png.')
    if photo.size > 5242880:
        raise ValidationError('Image size should be less than 5 megabytes.')
    return photo


def validate_address_and_coordinates(address, latitude, longitude):
    if address and longitude and latitude:
        if longitude < -180.0 or longitude > 180.0:
            raise ValidationError('Wrong longitude.')
        if latitude < -90.0 or latitude > 90.0:
            raise ValidationError('Wrong latitude.')
    else:
        address, latitude, longitude = None, None, None
    return address, latitude, longitude


def validate_announcement_type(announcement_type):
    if announcement_type not in (1, 2):
        raise ValidationError('Wrong announcement type.')
    return announcement_type


def validate_animal_type(animal_type):
    if animal_type not in (1, 2, 3):
        raise ValidationError('Wrong animal type.')
    return animal_type


class AnnouncementRetrieveSerializer(ModelSerializer):
    user = CharField(
        source='user.username',
        read_only=True
    )

    class Meta:
        model = Announcement
        fields = '__all__'


class AnnouncementCreateSerializer(ModelSerializer):
    user = CharField(
        source='user.username',
        read_only=True
    )

    class Meta:
        model = Announcement
        fields = '__all__'

    def validate(self, attrs):

        attrs['address'], attrs['latitude'], attrs['longitude'] = validate_address_and_coordinates(
            attrs.get('address'),
            attrs.get('latitude'),
            attrs.get('longitude')
        )
        validate_contact_phone_number(attrs.get('contact_phone_number'))
        validate_photo(attrs.get('photo'))
        validate_announcement_type(attrs.get('announcement_type'))
        validate_animal_type(attrs.get('animal_type'))

        return attrs


class MapInfoSerializer(ModelSerializer):

    class Meta:
        model = Announcement
        fields = ('id', 'latitude', 'longitude')
