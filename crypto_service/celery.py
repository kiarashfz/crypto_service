from __future__ import absolute_import

import os
import sys

from celery import Celery
from django.conf import settings
import django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crypto_service.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Local')

django.setup()
app = Celery('crypto_service', broker='redis://localhost:6379', backend='mongodb://localhost:27017/')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
