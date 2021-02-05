#!/bin/bash
python manage.py makemigrations
python manage.py migrate
Python manage.py rumserver 0.0.0.0:8001
