"""Development environment settings."""
from .base import *

DEBUG = True

SECRET_KEY = 'q!%*q6__xj96xzhdm8i7()3cd1z2@_j0%_!-(r94w2i!2uj++%'

ALLOWED_HOSTS = ('*',)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_TEST_ROOT = os.path.join(MEDIA_ROOT, 'tests/')
