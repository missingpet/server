from configparser import RawConfigParser
from os.path import dirname
from os.path import join

ENV_DEVELOPMENT = "development"
ENV_STAGE = "stage"
ENV_PRODUCTION = "production"

config = RawConfigParser()
path = join(dirname(__file__), "settings.ini")
config.read(path)

ENV = config.get("settings", "ENVIRONMENT") or "development"

ENVIRONMENTS = (ENV_DEVELOPMENT, ENV_STAGE, ENV_PRODUCTION)

if ENV not in ENVIRONMENTS:
    print("Invalid DJANGO_ENV")
    ENV = ENV_DEVELOPMENT

if ENV == ENV_DEVELOPMENT:
    from .development import *

if ENV == ENV_STAGE:
    from .stage import *

if ENV == ENV_PRODUCTION:
    from .production import *
