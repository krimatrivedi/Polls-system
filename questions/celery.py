import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poll.settings')

app = Celery('questions')


BASE_REDIS_URL = os.environ.get('BROKER_URL', 'amqp://guest:guest@localhost:5672/')
CELERY_BROKER_URL = os.environ.get('BROKER_URL')
app.conf.broker_url = BASE_REDIS_URL


app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'every-3-minute':{
        'task':'questions.tasks.delete_file',
        'schedule':180,
    }
}
app.conf.timezone = 'Asia/Calcutta'

app.autodiscover_tasks()