#!/bin/bash
. venv/bin/activate
make migrate
python manage.py runserver
