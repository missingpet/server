"""
Production environment settings.
"""
import decouple

from .base import *  # NOQA

DEBUG = False

SECRET_KEY = decouple.config("SECRET_KEY")

ALLOWED_HOSTS = decouple.config(
    "ALLOWED_HOSTS",
    cast=decouple.Csv(post_process=tuple),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': decouple.config('DB_NAME'),
        'USER': decouple.config('DB_USER'),
        'PASSWORD': decouple.config('DB_PASSWORD'),
        'HOST': decouple.config('DB_HOST'),
        'PORT': decouple.config('DB_PORT'),
    }
}

ADMIN_EMAIL = decouple.config("ADMIN_EMAIL")
ADMIN_NICKNAME = decouple.config("ADMIN_NICKNAME")
ADMIN_PASSWORD = decouple.config("ADMIN_PASSWORD")