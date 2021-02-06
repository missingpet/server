"""Gunicorn WSGI-server configuration module."""
from multiprocessing import cpu_count

workers = 2 * cpu_count() + 1
proxy_allow_ips = '0.0.0.0'
forwarded_allow_ips = '0.0.0.0'
bind = '0.0.0.0:8001'
limit_request_fields = 32768
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=conf.settings'
