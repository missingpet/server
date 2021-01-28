[program:gunicorn]
command=/server/src/bin/start_gunicorn.sh
user=
process_name=%(program_name)s
numproc=1
autostart=1
autorestart=1
redirect_stderr=true
