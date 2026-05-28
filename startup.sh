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

# Make sure staticfiles directory exists and has permissions
echo "Setting up static files directory..."
mkdir -p /home/site/wwwroot/src/ProyectoSITU/staticfiles
chmod -R 755 /home/site/wwwroot/src/ProyectoSITU/staticfiles

# Run Django migrations
echo "Running Django migrations..."
python manage.py migrate --noinput 2>&1 || echo "Migration warning: $?"

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --verbosity 2 2>&1 || echo "Collectstatic warning: $?"

echo "Static files collected to: $(pwd)/staticfiles"
ls -la $(pwd)/staticfiles 2>&1 || echo "Staticfiles directory check failed"

# Start Gunicorn
echo "Starting Gunicorn on port ${PORT:-8000}..."
exec gunicorn \
    --bind=0.0.0.0:${PORT:-8000} \
    --timeout 600 \
    --workers 2 \
    --error-logfile - \
    --access-logfile - \
    ProyectoSITU.wsgi:application
