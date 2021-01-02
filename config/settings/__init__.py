from os.path import join
from os.path import dirname

from configparser import RawConfigParser


ENV_PRODUCTION = "production"
ENV_DEVELOPMENT = "development"

config = RawConfigParser()
path = join(dirname(__file__), "settings.ini")
config.read(path)

ENV = config.get("settings", "ENVIRONMENT") or "development"

ENVIRONMENTS = (ENV_PRODUCTION, ENV_DEVELOPMENT)

if ENV not in ENVIRONMENTS:
    print("Invalid DJANGO_ENV")
    ENV = ENV_DEVELOPMENT

if ENV == ENV_DEVELOPMENT:
    from .development import *

if ENV == ENV_PRODUCTION:
    from .production import *
