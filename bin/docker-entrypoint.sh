#!/usr/bin/env sh
python manage.py migrate --no-input
python manage.py collectstatic --no-input
python manage.py init_superuser
exec gunicorn -c "gunicorn_config.py" conf.wsgi
