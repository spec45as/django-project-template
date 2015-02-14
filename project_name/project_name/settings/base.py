# coding: utf-8
"""
Settings for {{ project_name }} project.
"""

from __future__ import print_function, unicode_literals, division

import os
import sys


PROJECT_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
MANAGE_DIR = os.path.normpath(os.path.join(PROJECT_DIR, '..'))
ROOT_DIR = os.path.normpath(os.path.join(MANAGE_DIR, '..'))

SECRET_KEY = open(os.path.normpath(os.path.join(ROOT_DIR, 'conf/secret'))).read().strip()

INSTALLED_APPS = [
    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # third-party apps

    # project apps
    'core',
]

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
)

SITE_ID = 1

ROOT_URLCONF = '{{ project_name }}.urls'

WSGI_APPLICATION = '{{ project_name }}.wsgi.application'

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

FIRST_DAY_OF_WEEK = 1

USE_TZ = False

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)

LOCALE_PATHS = [
    os.path.abspath(os.path.join(PROJECT_DIR, 'locale')),
]

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.static',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

STATICFILES_DIRS = (
    ('css', os.path.join(STATIC_ROOT, 'css')),
    ('js', os.path.join(STATIC_ROOT, 'js')),
    ('img', os.path.join(STATIC_ROOT, 'img')),
    ('vendor', os.path.join(STATIC_ROOT, 'vendor')),
)

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')

CSRF_COOKIE_NAME = '__csrf'

LANGUAGE_COOKIE_NAME = '__lang'

SESSION_COOKIE_NAME = '__sid'

USE_ETAGS = False

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = 'auth_login'
LOGOUT_URL = 'auth_logout'

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'file_error_log': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(ROOT_DIR, 'var/log/error.log'),
        },
        'stdout': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'file_error_log'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# debug toolbar
DEBUG_TOOLBAR_PATCH_SETTINGS = False
DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': '/static/vendor/jquery/dist/jquery.js',
}