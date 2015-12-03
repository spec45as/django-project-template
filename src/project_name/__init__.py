# coding: utf-8

from os import path as p

import envvars as env

env_file = p.normpath(p.join(p.abspath(p.dirname(__file__)), "../../conf/env"))
env.load(env_file)

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
try:
    from .celery import app as celery_app
except ImportError as e:
    print('{{ project_name }}/__init__.py: celery import error, ignoring')
