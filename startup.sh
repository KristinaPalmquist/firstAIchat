#!/bin/bash

# Azure Web App startup script
# This script will be executed when your app starts

# Collect static files
python manage.py collectstatic --noinput

# Run database migrations (optional - be careful in production)
# python manage.py migrate --noinput

# Start Gunicorn server
gunicorn --bind=0.0.0.0 --timeout 600 firstaichat.wsgi:application