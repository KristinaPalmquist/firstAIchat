"""
Azure Web App startup script for Django application.
This script ensures proper initialization of the Django app on Azure.
"""

import os
from django.core.wsgi import get_wsgi_application

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'firstaichat.settings')

# Get the WSGI application
application = get_wsgi_application()