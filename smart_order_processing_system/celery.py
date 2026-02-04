import os
from celery import Celery

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'smart_order_processing_system.settings'
)

app = Celery('smart_order_processing_system')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
