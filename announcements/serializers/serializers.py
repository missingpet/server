import re
import imghdr

from rest_framework.exceptions import ValidationError

from .base import AnnouncementBaseSerializer
from .base import MapInfoBaseSerializer

from django.utils.translation import gettext_lazy as _


class AnnouncementRetrieveSerializer(AnnouncementBaseSerializer):
    pass


class AnnouncementCreateSerializer(AnnouncementBaseSerializer):

    def validate(self, attrs):
        contact_phone_number = attrs.get('contact_phone_number')
        photo = attrs.get('photo')
        address = attrs.get('address')
        latitude = attrs.get('latitude')
        longitude = attrs.get('longitude')
        announcement_type = attrs.get('announcement_type')
        animal_type = attrs.get('animal_type')

        if not re.match(r'\+7\d{10}$', contact_phone_number):
            raise ValidationError(
                _('Contact phone number should starts with +7 and contains 12 characters total.')
            )

        if imghdr.what(photo) not in ('jpeg', 'png'):
            raise ValidationError(
                _('Image extension should be jpeg or png.')
            )
        if photo.size > 5242880:
            raise ValidationError(
                _('Image size should be less than 5 megabytes.')
            )

        if address:
            if not latitude:
                raise ValidationError(
                    _('Address is given but latitude isn`t.')
                )
            if not longitude:
                raise ValidationError(
                    _('Address is given but longitude isn`t.')
                )
            if latitude < -90.0 or latitude > 90.0:
                raise ValidationError(
                    _('Latitude should take value between -90,0 and 90,0.')
                )
            if longitude < -180.0 or longitude > 180.0:
                raise ValidationError(
                    _('Longitude should take value between -180,0 and 180,0.')
                )
        elif latitude:
            raise ValidationError(
                _('Latitude is given but address isn`t.')
            )
        elif longitude:
            raise ValidationError(
                _('Longitude is given but address isn`t.')
            )

        if announcement_type not in (1, 2):
            raise ValidationError(
                _('Announcement type should be 1 (if you lost an animal) or 2 (if you found one).')
            )

        if animal_type not in (1, 2, 3):
            raise ValidationError(
                _('Animal type should be 1 (for dogs), 2 (for cats) or 3 (for other animals).')
            )

        return attrs


class FeedMapInfoSerializer(MapInfoBaseSerializer):
    pass
