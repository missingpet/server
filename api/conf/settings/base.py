"""Shared project settings."""
import os
from datetime import timedelta

SECRET_KEY = os.environ["APP_SECRET"]

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

LOGS_DIR = os.path.join(BASE_DIR, "logs/")

try:
    os.mkdir(LOGS_DIR)
except OSError:
    pass

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGS_DIR, "debug.log"),
            "maxBytes": 1024 * 1024 * 20,
            "backupCount": 4,
            "formatter": "verbose",
        },
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "level": "DEBUG",
            "propagate": True,
        },
        "django.template": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

LOCAL_APPS = ('pet.apps.PetConfig', )

THIRD_PARTY_APPS = (
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_yasg",
    "django_cleanup.apps.CleanupConfig",
)

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
) + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = (
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

ROOT_URLCONF = "conf.urls"

TEMPLATES = ({
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [],
    "APP_DIRS": True,
    "OPTIONS": {
        "context_processors": (
            "django.template.context_processors.debug",
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
        ),
    },
},)

WSGI_APPLICATION = "conf.wsgi.application"

AUTH_PASSWORD_VALIDATORS = (
    {
        "NAME":
        "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
)

LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

AUTHENTICATION_BACKENDS = ("pet.auth.EmailAuthBackend", )

AUTH_USER_MODEL = "pet.User"

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

MEDIA_TEST_ROOT = os.path.join(MEDIA_ROOT, "tests/")

ANNOUNCEMENTS_PHOTO = "announcements/%Y/%m/%d/"

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer", ),
    "SIGNING_KEY": SECRET_KEY,
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken", ),
}

SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": True,
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "JWT authorization",
        }
    },
    "LOGIN_URL": "rest_framework:login",
    "LOGOUT_URL": "rest_framework:logout",
}
