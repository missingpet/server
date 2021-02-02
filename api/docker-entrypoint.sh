#!/bin/zsh
python manage.py migrate
python manage.py collectstatic
sh start-gunicorn.sh