# coding: utf-8

from __future__ import print_function, unicode_literals, division

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
try:
    from .celery import app as celery_app
except ImportError as e:
    print('{{ project_name }}/__init__.py: celery import error, ignoring')
