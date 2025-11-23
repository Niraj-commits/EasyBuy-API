from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main_folder.settings')

app = Celery('main_folder')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# celery -A main_folder worker --loglevel=info
