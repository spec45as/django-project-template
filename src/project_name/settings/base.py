# coding: utf-8
"""
Settings for {{ project_name }} project.
"""

import os
import sys

import envvars as e

from django.contrib.messages import constants as messages


PROJECT_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
MANAGE_DIR = os.path.normpath(os.path.join(PROJECT_DIR, '..'))
ROOT_DIR = os.path.normpath(os.path.join(MANAGE_DIR, '..'))

e.load(os.path.join(ROOT_DIR, 'conf/env'))

SECRET_KEY = e.get('DJANGO_SECRET')

INSTALLED_APPS = [
    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',

    # third-party apps
    'allauth',
    'allauth.account',
    'cmstemplates',
    'widget_tweaks',
    'ckeditor',
    'ckeditor_uploader',

    # wagtail
    'taggit',
    'modelcluster',

    'wagtail.wagtailcore',
    'wagtail.wagtailadmin',
    'wagtail.wagtaildocs',
    'wagtail.wagtailsnippets',
    'wagtail.wagtailusers',
    'wagtail.wagtailimages',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsearch',
    'wagtail.wagtailsites',
    'wagtail.wagtailredirects',
    'wagtail.wagtailforms',

    # project apps
    'core',
    'users',
]

AUTH_USER_MODEL = 'users.User'

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',

    # wagtail
    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',
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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
        'OPTIONS': {
            'context_processors': (
                # django builtin processors
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.request",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            )
        }
    },
]

LOCALE_PATHS = [
    os.path.abspath(os.path.join(PROJECT_DIR, 'locale')),
]

AUTHENTICATION_BACKENDS = (
    # default django backend
    "django.contrib.auth.backends.ModelBackend",
    # django-allauth
    "allauth.account.auth_backends.AuthenticationBackend",
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

STATICFILES_DIRS = (
    ('assets', os.path.join(STATIC_ROOT, 'assets')),
    ('vendor', os.path.join(STATIC_ROOT, 'vendor')),
    ('build', os.path.join(STATIC_ROOT, 'build')),
)

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')

CSRF_COOKIE_NAME = '__csrf'

LANGUAGE_COOKIE_NAME = '__lang'

SESSION_COOKIE_NAME = '__sid'

USE_ETAGS = False

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = 'account_login'
LOGOUT_URL = 'account_logout'

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

SECURE_BROWSER_XSS_FILTER = True

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

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

# debug toolbar
DEBUG_TOOLBAR_PATCH_SETTINGS = False
DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': '/static/vendor/jquery/dist/jquery.js',
}

# django-allauth
ACCOUNT_ADAPTER = "allauth.account.adapter.DefaultAccountAdapter"
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = LOGIN_URL
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = None
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http"
ACCOUNT_FORMS = {}
ACCOUNT_LOGOUT_ON_GET = False
ACCOUNT_LOGOUT_REDIRECT_URL = "/"
ACCOUNT_SIGNUP_FORM_CLASS = None
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = False  # одно поле для пароля
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_MIN_LENGTH = 1
ACCOUNT_USERNAME_BLACKLIST = ['admin', 'administrator', 'superuser']
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_PASSWORD_INPUT_RENDER_VALUE = True
ACCOUNT_PASSWORD_MIN_LENGTH = 3
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_SESSION_REMEMBER = True

# django-cmstemplates
CMSTEMPLATES_USE_CODEMIRROR = True

# django-codemirror-widget
CODEMIRROR_PATH = 'vendor/codemirror'
CODEMIRROR_THEME = 'default'
CODEMIRROR_CONFIG = {'lineNumbers': True}

# django-ckeditor
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_JQUERY_URL = os.path.join(STATIC_URL, 'vendor/jquery/dist/jquery.min.js')
CKEDITOR_RESTRICT_BY_USER = True

#CKEDITOR_CONFIGS = {
#    'default': {}
#}

# wagtail
WAGTAIL_SITE_NAME = '{{ project_name }}'
WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.wagtailsearch.backends.db.DBSearch',
        'INDEX': '{{ project_name }}',
        #'BACKEND': 'wagtail.wagtailsearch.backends.elasticsearch.ElasticSearch',
        #'URLS': ['http://localhost:9200'],
        #'TIMEOUT': 5,
    }
}
WAGTAIL_ENABLE_UPDATE_CHECK = False

# таймаут для задач - 1 минута
CELERYD_TASK_SOFT_TIME_LIMIT = 60
BROKER_URL = e.get('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = e.get('CELERY_RESULT_BACKEND')

# pymorphy
import pymorphy2
MORPH = pymorphy2.MorphAnalyzer()
