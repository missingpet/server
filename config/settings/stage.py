from .base import *

DEBUG = False

ALLOWED_HOSTS = ("127.0.0.1", "localhost")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "0000",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
