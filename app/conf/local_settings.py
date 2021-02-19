import decouple

DEBUG = decouple.config("DEBUG", default=False, cast=bool)

SECRET_KEY = decouple.config("SECRET_KEY")

ALLOWED_HOSTS = decouple.config("ALLOWED_HOSTS",
                                cast=decouple.Csv(post_process=tuple))

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": decouple.config("POSTGRES_DB"),
        "USER": decouple.config("POSTGRES_USER"),
        "PASSWORD": decouple.config("POSTGRES_PASSWORD"),
        "HOST": decouple.config("POSTGRES_HOST"),
        "PORT": decouple.config("POSTGRES_PORT"),
    }
}
