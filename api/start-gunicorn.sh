#!/bin/zsh
source venv/bin/activate
exec gunicorn -c "gunicorn_config.py" conf.wsgi
