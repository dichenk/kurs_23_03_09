from celery import shared_task
# from config import settings
from config import settings
from .views import test_mailll
from celery import Celery

# from config.celery import app
app = Celery('config')

@shared_task(bind=True)
def make_something(self):
    test_mailll()
    return 'done'

