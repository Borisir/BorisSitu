#!/bin/bash
cd /home/site/wwwroot/src/ProyectoSITU
python manage.py migrate --noinput
gunicorn --bind=0.0.0.0:8000 --timeout 600 ProyectoSITU.wsgi:application
