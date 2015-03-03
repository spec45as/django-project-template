# coding: utf-8

from __future__ import print_function, unicode_literals, division

try:
    from ConfigParser import ConfigParser
except ImportError:  # python3
    from configparser import ConfigParser

import dj_database_url

from {{ project_name }}.settings.base import *

ADMINS = (
    ('username', 'user@email'),
)

MANAGERS = ()

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': dj_database_url.parse(e.get('DJANGO_DB')),
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(MANAGE_DIR, 'cache'),
        'TIMEOUT': 600,
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
        }
    }
}

DEFAULT_FROM_EMAIL = e.get('DJANGO_FROM_EMAIL')
SERVER_EMAIL = DEFAULT_FROM_EMAIL
EMAIL_HOST = e.get('DJANGO_EMAIL_HOST')
EMAIL_PORT = e.get('DJANGO_EMAIL_PORT')
EMAIL_HOST_USER = e.get('DJANGO_EMAIL_USER')
EMAIL_HOST_PASSWORD = e.get('DJANGO_EMAIL_PASSWORD')
EMAIL_SUBJECT_PREFIX = '{{ project_name }} '

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        'django.template.loaders.eggs.Loader',
    )),
)

# celery configuration
BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

