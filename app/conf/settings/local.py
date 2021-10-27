import decouple

DEBUG = decouple.config('DEBUG', cast=bool)

SECRET_KEY = decouple.config("SECRET_KEY")

ALLOWED_HOSTS = decouple.config(
    "ALLOWED_HOSTS",
    cast=decouple.Csv(post_process=tuple),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': decouple.config('POSTGRES_NAME'),
        'USER': decouple.config('POSTGRES_USER'),
        'PASSWORD': decouple.config('POSTGRES_PASSWORD'),
        'HOST': decouple.config('POSTGRES_HOST'),
        'PORT': decouple.config('POSTGRES_PORT'),
    }
}

ADMIN_EMAIL = decouple.config('ADMIN_EMAIL')
ADMIN_NICKNAME = decouple.config('ADMIN_NICKNAME')
ADMIN_PASSWORD = decouple.config('ADMIN_PASSWORD')