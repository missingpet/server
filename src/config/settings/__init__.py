from configparser import RawConfigParser
from os.path import dirname, join

ENV_DEVELOPMENT = "development"
ENV_PRODUCTION = "production"

config = RawConfigParser()
path = join(dirname(__file__), "settings.ini")
config.read(path)

ENV = config.get("settings", "ENVIRONMENT") or "development"

ENVIRONMENTS = (ENV_DEVELOPMENT, ENV_PRODUCTION)

if ENV not in ENVIRONMENTS:
    print("Invalid DJANGO_ENV")
    ENV = ENV_DEVELOPMENT

if ENV == ENV_DEVELOPMENT:
    from .development import *

if ENV == ENV_PRODUCTION:
    from .production import *
