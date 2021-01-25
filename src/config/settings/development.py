from .base import *

DEBUG = True

ALLOWED_HOSTS = ('*', )

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": join(BASE_DIR, "db.sqlite3"),
    }
}
