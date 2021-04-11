import decouple
from django.core.exceptions import ImproperlyConfigured

ENV_PRODUCTION = "production"
ENV_DEVELOPMENT = "development"

DJANGO_ENV = decouple.config("DJANGO_ENV", default="development")

ENVIRONMENTS = (ENV_PRODUCTION, ENV_DEVELOPMENT)

if DJANGO_ENV not in ENVIRONMENTS:
    raise ImproperlyConfigured("Invalid DJANGO_ENV setting")

if DJANGO_ENV == ENV_DEVELOPMENT:
    from .development import *  # NOQA
elif DJANGO_ENV == ENV_PRODUCTION:
    from .production import *  # NOQA
