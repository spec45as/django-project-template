# coding: utf-8

from __future__ import print_function

import os
import base64
import getpass

import jinja2

from fabric.operations import local, prompt
from fabric.contrib.console import confirm


# Базовый путь до корня проекта
BASE_PATH = os.path.abspath(os.path.dirname(__file__))

PROJECT_NAME = '{{ project_name }}'
# Путь до manage.py
MANAGE_PATH = os.path.join(BASE_PATH, PROJECT_NAME)
# Путь до директории проекта с файло settings.py
PROJECT_PATH = os.path.join(MANAGE_PATH, PROJECT_NAME)

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


def _base_path(*path):
    """Возвратить полный путь относительно корневой директории."""
    return os.path.join(BASE_PATH, *path)


def _manage_path(*path):
    """Возвратить полный путь относительно manage.py."""
    return os.path.join(MANAGE_PATH, *path)


def _project_path(*path):
    """Возвратить полный путь относительно проекта (settings.py)."""
    return os.path.join(PROJECT_PATH, *path)


def make_virtualenv():
    """Создать виртуальное окружение."""
    local('virtualenv env')


def install_requirements(env):
    """
    Установить зависимости в виртуальное окружение.

    Аргументы:
        env - окружение проекта. Если True - development, иначе
            production.
    """
    if env:
        req = 'local.txt'
    else:
        req = 'production.txt'
    cmd = ('source env/bin/activate && '
           'pip install -r requirements/{}'.format(req))
    local(cmd, shell='bash')


def generate_secret(length=512):
    """Сгенерировать секрет и записать в файл conf/secret."""

    with open(_base_path(SECRET_FILE), 'w') as f:
        secret_key = base64.urlsafe_b64encode(os.urandom(length))
        f.write(secret_key)
        _log('Сгенерирован секретный ключ: {}'.format(SECRET_FILE))


def create_config_ini():
    """Создать config.ini."""
    _render(_base_path('conf/config.ini.template'), _base_path('conf/config.ini'))
    _log('Создан файл {}'.format(USER_CONFIG_FILE))


def create_manage_script(settings_module_path):
    # Обновить manage.py для использования новых настроек
    new_manage_path = _manage_path('manage.py')
    _render(
        _base_path('conf/manage.py.template'),
        new_manage_path,
        config_path=settings_module_path,
    )
    local('chmod +x {}'.format(new_manage_path))
    _log('Создан скрипт "manage"')


def create_user_config_file():
    if confirm('Создать новую конфигурацию проекта для разработки?'):
        username = prompt('Имя пользователя',
                          default=getpass.getuser(),
                          validate=r'^.*$')

        src_settings = _base_path('conf/local_settings.template')
        dst_settings_path = os.path.join(
            PROJECT_NAME,
            'settings',
            'local_{}.py'.format(username)
        )
        dst_settings = _manage_path(dst_settings_path)

        # Создать local_<user>.py
        _render(src_settings, dst_settings)
        _log('Создан файл {}'.format(dst_settings_path))

        # Обновить manage.py для использования новых настроек
        config_path = os.path.splitext(dst_settings_path.replace('/', '.'))[0]
        create_manage_script(config_path)

        _log('Для запуска проекта осталось:')
        _log('\t - указать конфигурацию БД в {}'
             .format(USER_CONFIG_FILE))
        _log('\t - выполнить ./manage migrate')
        _log('\t - выполнить ./manage runserver')


def ask_if_development_deployment():
    return confirm('Проект разворачивается для локальной разработки?')


def bootstrap():
    """Разворачивает проект в виртуальном окружении."""
    make_virtualenv()
    development = ask_if_development_deployment()
    install_requirements(development)
    generate_secret()
    create_config_ini()
    if development:
        create_user_config_file()
    else:
        create_manage_script(PROJECT_NAME + '.settings.production')
