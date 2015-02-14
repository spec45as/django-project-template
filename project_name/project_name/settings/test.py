# coding: utf-8

from __future__ import print_function, unicode_literals, division

try:
    from ConfigParser import ConfigParser
except ImportError:  # python3
    from configparser import ConfigParser

from {{ project_name }}.settings.base import *

cfg = ConfigParser()
cfg.readfp(open(os.path.normpath(os.path.join(ROOT_DIR, 'conf/config.ini'))))

DEBUG = True

TEMPLATE_DEBUG = True

SECRET_KEY = 'test_key'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': cfg.get('db', 'db'),
        'USER': cfg.get('db', 'user'),
        'PASSWORD': cfg.get('db', 'password'),
        'HOST': cfg.get('db', 'host'),
        'PORT': cfg.get('db', 'port'),
        'CONN_MAX_AGE': 0,
    }
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
