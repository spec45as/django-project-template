# coding: utf-8

import os
import glob
import tempfile

from . import logger
from .utils import local
from .settings import ENV_FILE, PROJECT_NAME
from .path import base_path, manage_path
from .templates import render


def create_virtualenv():
    import venv
    venv.create('env', clear=True, with_pip=True)


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


def setup_npm_tools():
    local('npm install')


def setup_npm_tools_configs(*args, **kwargs):
    render(
        base_path('conf/gulpfile.js.template'),
        base_path('gulpfile.js'),
        *args,
        **kwargs
    )
    logger.info('Создан gulpfile.js')


def delete_common_files():
    for fname in ['README.rst', 'todo.txt']:
        try:
            os.unlink(fname)
        except OSError:
            pass
