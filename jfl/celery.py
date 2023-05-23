# celery.py

import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jfl.settings')

app = Celery('jfl')

# Load configuration from Django settings.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Discover tasks modules in your Django apps.
app.autodiscover_tasks()
