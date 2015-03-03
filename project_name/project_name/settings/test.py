# coding: utf-8

from __future__ import print_function, unicode_literals, division

try:
    from ConfigParser import ConfigParser
except ImportError:  # python3
    from configparser import ConfigParser

import dj_database_url

from {{ project_name }}.settings.base import *

DEBUG = True

TEMPLATE_DEBUG = True

SECRET_KEY = 'test_key'

DATABASES = {
    'default': dj_database_url.parse(e.get('DJANGO_DB')),
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INTERNAL_IPS = ['127.0.0.1']

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)
