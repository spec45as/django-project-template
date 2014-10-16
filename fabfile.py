# coding: utf-8

from __future__ import print_function

import os
import base64
import getpass

import jinja2

from fabric.operations import local, prompt
from fabric.contrib.console import confirm


BASE_PATH = os.path.abspath(os.path.dirname(__file__))

PROJECT_NAME = '{{ project_name }}'
PROJECT_PATH = os.path.join(BASE_PATH, PROJECT_NAME)
SECRET_FILE = 'conf/secret'
USER_CONFIG_FILE = 'conf/config.ini'


def _log(message):
    print(message)


def _render(src, dst, **kwargs):
    """
    Отрендерить jinja2 шаблон.

    Аргументы:
        src - путь к шаблону
        dst - путь к выходному файлу
        **kwargs - параметры для передачи в шаблон
    """
    with open(src) as f:
        template = jinja2.Template(f.read())
    with open(dst, 'w') as f:
        f.write(template.render(**kwargs))


def _rel(*path):
    """Возвратить полный путь относительно директории проекта."""
    return os.path.join(BASE_PATH, *path)


def make_virtualenv():
    """Создать виртуальное окружение."""
    local('virtualenv env')


def install_requirements():
    """Установить зависимости в виртуальное окружение."""
    local('source env/bin/activate && pip install -r requirements.txt',
          shell='bash')


def generate_secret(length=512):
    """Сгенерировать секрет и записать в файл conf/secret."""

    with open(_rel(SECRET_FILE), 'w') as f:
        secret_key = base64.urlsafe_b64encode(os.urandom(length))
        f.write(secret_key)
        _log('Сгенерирован секретный ключ: {}'.format(SECRET_FILE))


def create_user_config_file():
    if confirm('Создать новую конфигурацию проекта?'):
        username = prompt('Имя пользователя',
                          default=getpass.getuser(),
                          validate=r'^.*$')

        src_settings = _rel('conf/local_settings.template')
        dst_settings_path = os.path.join(
            PROJECT_NAME,
            'settings',
            'local_{}.py'.format(username)
        )
        dst_settings = _rel(dst_settings_path)

        # Создать local_<user>.py
        _render(src_settings, dst_settings)
        _log('Создан файл {}'.format(dst_settings_path))

        # Создать config.ini
        _render(_rel('conf/config.ini.template'), _rel('conf/config.ini'))
        _log('Создан файл {}'.format(USER_CONFIG_FILE))

        # Обновить manage.py для использования новых настроек
        config_path = os.path.splitext(dst_settings_path.replace('/', '.'))[0]
        _render(_rel('conf/manage.py.template'), _rel('manage'),
                config_path=config_path)
        local('chmod +x manage')
        _log('Создан скрипт "manage"')

        _log('Осталось указать конфигурацию БД в {}'
             .format(USER_CONFIG_FILE))


def bootstrap():
    """Разворачивает проект в виртуальном окружении."""
    make_virtualenv()
    install_requirements()
    generate_secret()
    create_user_config_file()
