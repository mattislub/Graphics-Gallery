"""
Celery config for app project.
"""
import os

from celery import Celery  # type: ignore

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check_unpaid_basket_every_7_days': {
        'task': 'shop.tasks.check_unpaid_basket',
        'schedule': 86400 * 7,  # seconds per days * days
    },
}

# For append tasks create 'tasks.py' file:
#
# from celery import shared_task
#
# @shared_task
# def task():
#     pass
