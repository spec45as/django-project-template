try:
    from ConfigParser import ConfigParser
except ImportError:  # python3
    from configparser import ConfigParser

from {{ project_name }}.settings.base import *

cfg = ConfigParser()
cfg.readfp(open(os.path.normpath(os.path.join(BASE_DIR, '../conf/config.ini'))))

ADMINS = (
    ('username', 'user@email'),
)

MANAGERS = ADMINS

ALLOWED_HOSTS = ['.example.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': cfg.get('db', 'db'),
        'USER': cfg.get('db', 'user'),
        'PASSWORD': cfg.get('db', 'password'),
        'HOST': cfg.get('db', 'host'),
        'PORT': cfg.get('db', 'port'),
        'CONN_MAX_AGE': 60,
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache'),
        'TIMEOUT': 600,
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
        }
    }
}

DEFAULT_FROM_EMAIL = cfg.get('email', 'from_email')
SERVER_EMAIL = DEFAULT_FROM_EMAIL
EMAIL_HOST = cfg.get('email', 'host')
EMAIL_PORT = cfg.get('email', 'port')
EMAIL_HOST_USER = cfg.get('email', 'user')
EMAIL_HOST_PASSWORD = cfg.get('email', 'password')
EMAIL_SUBJECT_PREFIX = '{{ project_name }} '

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        'django.template.loaders.eggs.Loader',
    )),
)
