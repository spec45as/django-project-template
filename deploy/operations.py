# coding: utf-8

from __future__ import unicode_literals

import os
import sys
import glob
import tempfile

from . import logger
from .utils import local
from .settings import ENV_FILE, PROJECT_NAME
from .path import base_path, manage_path
from .templates import render


PYTHON_VERSION = sys.version_info.major


def create_virtualenv():
    if PYTHON_VERSION == 2:
        create_virtualenv_python2()
    else:
        create_virtualenv_python3()


def create_virtualenv_python3():
    import venv
    venv.create('env', clear=True, with_pip=True)


def create_virtualenv_python2():
    local('virtualenv env')


def install_requirements(reqs_file):
    """Установить зависимости в виртуальное окружение. """
    cmd = ('source env/bin/activate && '
           'pip install -r requirements/{}'.format(reqs_file))
    local(cmd, shell='bash')


def create_env_file(*args, **kwargs):
    """Создать файл с настройками окружения `env`"""
    render(
        base_path('conf/env.template'),
        base_path(ENV_FILE),
        *args,
        **kwargs
    )
    logger.info('Создан файл {}'.format(ENV_FILE))


def install_crontab(filepath):
    """Установить задачу в крон."""
    logger.info('Установка задачи в крон {}'.format(
        os.path.basename(filepath)
    ))
    crontab_path = os.path.abspath(filepath)
    tmp_file = tempfile.mkstemp(suffix='crontab')[1]
    render(
        src=crontab_path,
        dst=tmp_file,
        here=base_path(),
        project_name=PROJECT_NAME,
    )
    local('crontab {}'.format(tmp_file))


def install_crontabs():
    """Найти и установить кронтабы."""
    crontabs = glob.glob('crontabs/*')
    for crontab in crontabs:
        install_crontab(crontab)


def create_user_config_file(settings_module):
    src_settings = base_path('conf/local_settings.template')
    dst_settings_path = os.path.join(
        PROJECT_NAME,
        'settings',
        settings_module + '.py',
    )
    dst_settings = manage_path(dst_settings_path)

    # Создать локальные настройки пользователя
    render(src_settings, dst_settings)
    logger.info('Создан файл {}'.format(dst_settings_path))


def setup_static():
    local('bower install --save')


def delete_common_files():
    for fname in ['LICENSE.md', 'README.rst', 'todo.txt']:
        try:
            os.unlink(fname)
        except OSError:
            pass
