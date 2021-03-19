import decouple
from django.core.exceptions import ImproperlyConfigured

ENV_PRODUCTION = "production"
ENV_DEVELOPMENT = "development"

APPLICATION_ENVIRONMENT = decouple.config("APPLICATION_ENVIRONMENT")

ENVIRONMENTS = (ENV_PRODUCTION, ENV_DEVELOPMENT)

if APPLICATION_ENVIRONMENT not in ENVIRONMENTS:
    raise ImproperlyConfigured("Invalid APPLICATION_ENVIRONMENT setting")

if APPLICATION_ENVIRONMENT == ENV_DEVELOPMENT:
    from .development import *
elif APPLICATION_ENVIRONMENT == ENV_PRODUCTION:
    from .production import *
