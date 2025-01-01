import os
from celery import Celery
import logging

# Logging settings for Celery
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'golden_clean_backend.settings')

app = Celery('golden_clean_backend')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# Task of debugging
@app.task(bind=True)
def debug_task(self):
    logger.debug(f'Request: {self.request!r}')
