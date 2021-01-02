from os.path import join

from .base import *

DEBUG = True

ALLOWED_HOSTS = ("127.0.0.1", "localhost")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": join(BASE_DIR, "db.sqlite3"),
    }
}
