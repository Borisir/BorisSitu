#!/bin/bash
cd /home/site/wwwroot/src/ProyectoSITU
pip install -r /home/site/wwwroot/requirements.txt
python3 manage.py migrate
gunicorn --bind=0.0.0.0:8000 --timeout 600 ProyectoSITU.wsgi:application