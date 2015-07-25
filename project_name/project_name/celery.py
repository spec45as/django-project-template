# coding: utf-8

from celery import Celery
from django.conf import settings

app = Celery('{{ project_name }}')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(settings.INSTALLED_APPS, related_name='tasks')
