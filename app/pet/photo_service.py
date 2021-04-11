import os
from uuid import uuid4

from django.conf import settings


def upload_photo(instance, filename):
    extension = os.path.splitext(filename)[1]
    filename = uuid4().hex
    path = os.path.join(settings.ANNOUNCEMENTS_PHOTO, f"{filename}{extension}")
    return path