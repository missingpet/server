from .base import AnnouncementBaseSerializer, MapInfoBaseSerializer

from .validators import validate_address_and_coordinates
from .validators import validate_contact_phone_number
from .validators import validate_announcement_type
from .validators import validate_animal_type
from .validators import validate_photo


class AnnouncementRetrieveSerializer(AnnouncementBaseSerializer):
    pass


class AnnouncementCreateSerializer(AnnouncementBaseSerializer):

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


class FeedMapInfoSerializer(MapInfoBaseSerializer):
    pass
