#!/bin/bash
set -e

echo "Starting Django application deployment..."

# Navigate to application directory
cd /home/site/wwwroot/src/ProyectoSITU

# Create persistent data directories
echo "Creating persistent data directories..."
mkdir -p /home/situ_data/db
mkdir -p /home/situ_data/media
mkdir -p /home/situ_data/media/img
chmod -R 755 /home/situ_data

# Run Django migrations
echo "Running Django migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn \
    --bind=0.0.0.0:${PORT:-8000} \
    --timeout 600 \
    --workers 2 \
    --error-logfile - \
    --access-logfile - \
    ProyectoSITU.wsgi:application
