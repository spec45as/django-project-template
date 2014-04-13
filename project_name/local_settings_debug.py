from ConfigParser import ConfigParser

from settings import *

cfg = ConfigParser()
cfg.readfp(open(os.path.join(BASE_DIR, '.config-dev-example.ini')))

DEBUG = True

TEMPLATE_DEBUG = True

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
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp/django_cache',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INTERNAL_IPS = ['127.0.0.1']

TEMPLATE_CONTEXT_PROCESSORS += ("django.core.context_processors.debug",)

# default template loaders w/o caching
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)
