"""Production environment settings."""
import decouple

from .base import *  # NOQA

DEBUG = False

SECRET_KEY = decouple.config("SECRET_KEY")

ALLOWED_HOSTS = decouple.config("ALLOWED_HOSTS", cast=decouple.Csv(post_process=tuple))

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": decouple.config("POSTGRES_DB"),
        "USER": decouple.config("POSTGRES_USER"),
        "PASSWORD": decouple.config("POSTGRES_PASSWORD"),
        "HOST": decouple.config("POSTGRES_HOST"),
        "PORT": decouple.config("POSTGRES_PORT"),
    }
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = decouple.config("EMAIL_HOST")
EMAIL_HOST_USER = decouple.config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = decouple.config("EMAIL_HOST_PASSWORD")

ADMIN_EMAIL = decouple.config("ADMIN_EMAIL")
ADMIN_NICKNAME = decouple.config("ADMIN_NICKNAME")
ADMIN_PASSWORD = decouple.config("ADMIN_PASSWORD")

SERVER_DIR = os.path.dirname(BASE_DIR)

MEDIA_ROOT = os.path.join(SERVER_DIR, "media/")

STATIC_ROOT = os.path.join(SERVER_DIR, "static/")
