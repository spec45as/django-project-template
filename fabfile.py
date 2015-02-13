# coding: utf-8

from __future__ import print_function

import os
import base64
import tempfile
import glob
import getpass

import jinja2

from fabric.operations import local, prompt
from fabric.contrib.console import confirm


PROJECT_NAME = '{{ project_name }}'
# Путь до корня проекта
BASE_PATH = os.path.abspath(os.path.dirname(__file__))
# Путь до manage.py
MANAGE_PATH = os.path.join(BASE_PATH, PROJECT_NAME)
# Путь до директории проекта с файло settings.py
PROJECT_PATH = os.path.join(MANAGE_PATH, PROJECT_NAME)

SECRET_FILE = 'conf/secret'
USER_CONFIG_FILE = 'conf/config.ini'


class Logger:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def __init__(self, color):
        self.color = color

    def start(self):
        return self.color

    def end(self):
        return self.ENDC

    def format(self, msg):
        return self.start() + msg + self.end()

    @property
    def _log(self):
        return print

    def log(self, msg):
        self._log(self.format(msg))

    def confirm(self, msg):
        self._log(self.start())
        answer = confirm(msg)
        self._log(self.end())
        return answer


logger = Logger(Logger.OKGREEN + Logger.BOLD)
_log = logger.log
_confirm = logger.confirm


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


def _make_config_pythonpath(config_name):
    return PROJECT_NAME + '.settings.' + config_name


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
    _render(
        _base_path('conf/config.ini.template'),
        _base_path('conf/config.ini'),
    )
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
    _log('Обновлён скрипт "manage.py"')


def create_user_config_file(username):
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


def ask_if_development_deployment():
    return _confirm('Проект разворачивается для локальной разработки?')


def ask_if_install_crontabs():
    return _confirm('Установить задачи в крон от текущего пользователя?')


def ask_if_create_new_development_configuration():
    return _confirm('Создать новую конфигурацию проекта для разработки?')


def install_crontab(filepath):
    """Установить задачу в крон."""
    _log('Установка задачи в крон {}'.format(
        os.path.basename(filepath)
    ))
    crontab_path = os.path.abspath(filepath)
    tmp_file = tempfile.mkstemp(suffix='crontab')[1]
    _render(
        src=crontab_path,
        dst=tmp_file,
        here=BASE_PATH,
        project_name=PROJECT_NAME,
    )
    local('crontab {}'.format(tmp_file))


def install_crontabs():
    """Найти и установить кронтабы."""
    crontabs = glob.glob('crontabs/*')
    for crontab in crontabs:
        install_crontab(crontab)


def delete_common_files():
    for fname in ['LICENSE.md', 'README.rst', 'todo.txt']:
        try:
            os.unlink(fname)
        except OSError:
            pass


def bootstrap():
    """Разворачивает проект в виртуальном окружении."""
    delete_common_files()
    make_virtualenv()
    development = ask_if_development_deployment()
    install_requirements(development)
    generate_secret()
    create_config_ini()
    if development and ask_if_create_new_development_configuration():
        username = prompt('Имя пользователя', default=getpass.getuser())
        create_user_config_file(username)
        config_name = 'local_' + username
    else:
        config_name = 'production'
        if ask_if_install_crontabs():
            install_crontabs()
    create_manage_script(_make_config_pythonpath(config_name))

    _log('Для запуска проекта осталось:')
    _log('\t - указать конфигурацию БД в {}'
         .format(USER_CONFIG_FILE))
    manage_path = PROJECT_NAME + '/manage.py'
    _log('\t - выполнить {} migrate'.format(manage_path))
    _log('\t - выполнить {} runserver'.format(manage_path))
