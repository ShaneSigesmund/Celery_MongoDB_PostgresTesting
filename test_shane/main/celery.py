import os
from celery import Celery

# Set default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_shane.settings')

# Create default Celery app
app = Celery('tasks',backend='redis://127.0.0.1:6379', broker='redis://127.0.0.1:6379')


# Use $ celery -A main.celery worker --loglevel=info to run


# namespace='CELERY' means all celery-related configuration keys
# should be uppercased and have a `CELERY_` prefix in Django settings.
# https://docs.celeryproject.org/en/stable/userguide/configuration.html
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.broker_transport_options = {'visibility_timeout': 60}


# When we use the following in Django, it loads all the <appname>.tasks
# files and registers any tasks it finds in them. We can import the
# tasks files some other way if we prefer.
app.autodiscover_tasks()


@app.task
def add(x, y):
    return x + y

