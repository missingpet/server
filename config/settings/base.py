from datetime import timedelta
from os.path import abspath, dirname, join

from .secret_key import *

BASE_DIR = dirname(dirname(dirname(abspath(__file__))))

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

EXTERNAL_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "drf_yasg",
    "admin_reorder",
]

INTERNAL_APPS = [
    "users.apps.UsersConfig",
    "announcements.apps.AnnouncementsConfig",
]

INSTALLED_APPS += EXTERNAL_APPS
INSTALLED_APPS += INTERNAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

EXTERNAL_MIDDLEWARE = [
    "admin_reorder.middleware.ModelAdminReorder",
]

MIDDLEWARE += EXTERNAL_MIDDLEWARE

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

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
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}

AUTH_USER_MODEL = "users.User"

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

STATIC_ROOT = join(BASE_DIR, "static/")
MEDIA_ROOT = join(BASE_DIR, "media/")

MEDIA_SPLIT_DIRS = "/%Y/%m/%d/"
ANNOUNCEMENTS_PHOTO = "announcements{}".format(MEDIA_SPLIT_DIRS)

SIMPLE_JWT = {
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": "Bearer",
    "ACCESS_TOKEN_LIFETIME": timedelta(days=3),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}

SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": True,
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}
    },
    "LOGIN_URL": "rest_framework:login",
    "LOGOUT_URL": "rest_framework:logout",
}

ADMIN_REORDER = [
    {
        "app": "announcements",
        "label": "Объявления",
    },
    {"app": "users", "label": "Пользователи"},
]
