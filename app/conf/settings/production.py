"""Production environment settings."""
import decouple

from .base import *  # NOQA

DEBUG = False

SECRET_KEY = decouple.config("SECRET_KEY")

ALLOWED_HOSTS = decouple.config(
    "ALLOWED_HOSTS",
    cast=decouple.Csv(post_process=tuple),
)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": decouple.config("RDS_DB_NAME"),
        "USER": decouple.config("RDS_USERNAME"),
        "PASSWORD": decouple.config("RDS_PASSWORD"),
        "HOST": decouple.config("RDS_HOSTNAME"),
        "PORT": decouple.config("RDS_PORT"),
    }
}

INSTALLED_APPS += ("storages", )

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_PORT = decouple.config("EMAIL_PORT")
EMAIL_HOST = decouple.config("EMAIL_HOST")
EMAIL_HOST_USER = decouple.config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = decouple.config("EMAIL_HOST_PASSWORD")

ADMIN_EMAIL = decouple.config("ADMIN_EMAIL")
ADMIN_NICKNAME = decouple.config("ADMIN_NICKNAME")
ADMIN_PASSWORD = decouple.config("ADMIN_PASSWORD")

AWS_S3_OBJECT_PARAMETERS = {
    "Expires": "Thu, 31 Dec 2099 20:00:00 GMT",
    "CacheControl": "max-age=94608000",
}

AWS_S3_REGION_NAME = decouple.config("AWS_S3_REGION_NAME")
AWS_ACCESS_KEY_ID = decouple.config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = decouple.config("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = decouple.config("AWS_STORAGE_BUCKET_NAME")
AWS_QUERYSTRING_AUTH = False
AWS_DEFAULT_ACL = None
AWS_S3_FILE_OVERWRITE = False

AWS_S3_CUSTOM_DOMAIN = "{}.s3.{}.amazonaws.com".format(
    AWS_STORAGE_BUCKET_NAME,
    AWS_S3_REGION_NAME,
)
DEFAULT_FILE_STORAGE = "pet.s3utils.MediaStorage"
STATICFILES_STORAGE = "pet.s3utils.StaticStorage"

MEDIA_FOLDER = "media/"
MEDIA_ROOT = os.path.join(AWS_S3_CUSTOM_DOMAIN, MEDIA_FOLDER)
MEDIA_URL = MEDIA_ROOT

STATIC_FOLDER = "static/"
STATIC_ROOT = os.path.join(AWS_S3_CUSTOM_DOMAIN, STATIC_FOLDER)
STATIC_URL = STATIC_ROOT
