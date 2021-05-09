"""
Shared project settings.
"""
import datetime
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

APP = (
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_yasg",
    "django_cleanup.apps.CleanupConfig",
    "pet.apps.PetConfig",
)

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
) + APP

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
    "DIRS": [os.path.join(BASE_DIR, "templates/")],
    "APP_DIRS": True,
    "OPTIONS": {
        "context_processors": [
            "django.template.context_processors.debug",
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
        ],
    },
}, )

TEMPLATE_DIRS = (os.path.join(BASE_DIR, "templates"), )

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

AUTHENTICATION_BACKENDS = ("pet.auth.EmailAuthBackend", )

AUTH_USER_MODEL = "pet.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_VERSIONING_CLASS":
    "rest_framework.versioning.URLPathVersioning",
}

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer", ),
    "SLIDING_TOKEN_LIFETIME": datetime.timedelta(days=100000),
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.SlidingToken", ),
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

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

STATICFILES_DIRS = (os.path.join(BASE_DIR, "staticfiles/"), )

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

ANNOUNCEMENTS_PHOTOS = "announcements/"

MAX_PHOTO_UPLOAD_SIZE = 5 * 1024 * 1024

ALLOWED_UPLOAD_IMAGE_EXTENSIONS = ("jpeg", "png")

PASSWORD_RESET_CONFIRMATION_CODE_LIFE_TIME = 60 * 10
PASSWORD_RESET_CONFIRMATION_CODE_LENGTH = 6

SETTINGS_ACTUAL_NAME = "По умолчанию"

SEND_EMAIL_RATE_LIMIT = "2/10m"
