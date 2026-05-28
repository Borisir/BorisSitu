#!/bin/bash
cd /home/site/wwwroot/src/ProyectoSITU
mkdir -p /home/data
python manage.py migrate --noinput
python manage.py collectstatic --noinput
exec gunicorn --bind=0.0.0.0:${PORT:-8000} --timeout 600 ProyectoSITU.wsgi:application
