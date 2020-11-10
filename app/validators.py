import re

from rest_framework.serializers import ValidationError


def validate_contact_phone_number(contact_phone_number):
    if not re.match(r'\+7\d{10}$', contact_phone_number):
        raise ValidationError('Неверный формат номера телефона.')
    return contact_phone_number


def validate_username(username):
    if not username.isalnum():
        raise ValidationError('Имя пользователя должно содержать только буквенно-цифровые символы.')
    return username


def validate_photo(photo):
    if photo.size > 5242880:
        raise ValidationError('Размер изображения не должен превышать 5 мегабайт.')
    return photo


def validate_address_and_coordinates(address, latitude, longitude):
    if address and longitude and latitude:
        if longitude < -180.0 or longitude > 180.0:
            raise ValidationError('Неверная долгота.')
        if latitude < -90.0 or latitude > 90.0:
            raise ValidationError('Неверная широта.')
    else:
        address = None
        latitude = None
        longitude = None
    return address, latitude, longitude


def validate_announcement_type(announcement_type):
    if announcement_type not in (1, 2):
        raise ValidationError('Неверный тип объявления.')
    return announcement_type


def validate_animal_type(animal_type):
    if animal_type not in (1, 2, 3):
        raise ValidationError('Неверный тип животного.')
    return animal_type
