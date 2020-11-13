import re
import imghdr

from rest_framework.serializers import ValidationError


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
        validate_longitude(longitude)
        validate_latitude(latitude)
    else:
        address, latitude, longitude = None, None, None
    return address, latitude, longitude


def validate_latitude(latitude):
    if latitude < -90.0 or latitude > 90.0:
        raise ValidationError('Wrong latitude.')
    return latitude


def validate_longitude(longitude):
    if longitude < -180.0 or longitude > 180.0:
        raise ValidationError('Wrong longitude.')
    return longitude


def validate_announcement_type(announcement_type):
    if announcement_type not in (1, 2):
        raise ValidationError('Wrong announcement type.')
    return announcement_type


def validate_animal_type(animal_type):
    if animal_type not in (1, 2, 3):
        raise ValidationError('Wrong animal type.')
    return animal_type
