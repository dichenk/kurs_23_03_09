from __future__ import absolute_import, unicode_literals

import os
from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.conf.timezone = 'Europe/Istanbul'

app.config_from_object(settings, namespace='CELERY')


app.conf.beat_schedule = {
    'every-20-seconds': {
        'task': 'app_spammy.tasks.make_something',
        'schedule': 10.0,
    },
    # 'every-15-seconds': {
        # 'task': 'app_spammy.tasks.send_pls',
        # 'schedule': 15.0,
    # },
}


# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')