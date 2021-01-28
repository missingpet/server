#!/bin/bash
source /server/src/venv/bin/activate
exec gunicorn -c "/server/src/missing-pet-backend/gunicorn_config.py" config.wsgi