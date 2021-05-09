#!/usr/bin/env bash
python manage.py migrate --no-input
python manage.py collectstatic --no-input
python manage.py createsu
exec gunicorn -c "gunicorn_config.py" conf.wsgi