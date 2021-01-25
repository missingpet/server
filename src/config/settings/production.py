from .base import *

DEBUG = False

ALLOWED_HOSTS = environ['ALLOWED_HOSTS'].split()

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": environ["DB_NAME"],
        "USER": environ["DB_USER"],
        "PASSWORD": environ["DB_PASSWORD"],
        "HOST": environ["DB_HOST"],
        "PORT": environ["DB_PORT"],
    }
}
