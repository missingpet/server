#!/bin/bash
source /server/src/venv/bin/activate
exec gunicorn -c "/server/src/gunicorn_config.py" config.wsgi
