from multiprocessing import cpu_count


def workers_count():
    return 2 * cpu_count() + 1


command = ''
pythonpath = ''
user = ''
limit_request_fields = 32000
limit_request_field_size = 0
workers = workers_count()
raw_env = 'DJANGO_SETTINGS_MODULE=config.settings'
bind = '0.0.0.0:8001'
