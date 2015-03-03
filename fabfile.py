# coding: utf-8

from __future__ import print_function

import os
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

ENV_FILE = 'conf/env'


class Logger:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def __init__(self, color, force_defaults=False):
        self.color = color
        self.force_defaults = force_defaults

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
        if self.force_defaults:
            return True

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
    kwargs.update({
        'env_file': _base_path(ENV_FILE),
    })
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


def install_requirements(reqs_file):
    """
    Установить зависимости в виртуальное окружение.

    Аргументы:
        env - окружение проекта. Если True - development, иначе
            production.
    """
    cmd = ('source env/bin/activate && '
           'pip install -r requirements/{}'.format(reqs_file))
    local(cmd, shell='bash')


def create_env_file(*args, **kwargs):
    """Создать файл с настройками окружения `env`"""
    _render(
        _base_path('conf/env.template'),
        _base_path(ENV_FILE),
        *args,
        **kwargs
    )
    _log('Создан файл {}'.format(ENV_FILE))


def update_manage_script():
    """Обновить manage.py для использования новых настроек."""
    new_manage_path = _manage_path('manage.py')
    _render(
        _base_path('conf/manage.py.template'),
        new_manage_path,
    )
    local('chmod +x {}'.format(new_manage_path))
    _log('Обновлён скрипт "manage.py"')


def update_project_init():
    """Обновить __init__.py проекта для использования настроек."""
    _render(
        _base_path('conf/project__init__.py.template'),
        _project_path('__init__.py'),
    )
    _log('Обновлён "__init__.py" проекта')


def create_user_config_file(settings_module):
        src_settings = _base_path('conf/local_settings.template')
        dst_settings_path = os.path.join(
            PROJECT_NAME,
            'settings',
            settings_module + '.py',
        )
        dst_settings = _manage_path(dst_settings_path)

        # Создать локальные настройки пользователя
        _render(src_settings, dst_settings)
        _log('Создан файл {}'.format(dst_settings_path))


def ask_if_development():
    return _confirm('Проект разворачивается для локальной разработки?')


def ask_if_install_crontabs():
    return _confirm('Установить задачи в крон от текущего пользователя?')


def ask_if_create_new_development_configuration():
    return _confirm('Создать новую конфигурацию проекта для разработки?')


def ask_username(question=None):
    return prompt(
        question or 'Имя пользователя', default=getpass.getuser())


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


def setup_static():
    local('bower install --save')


def bootstrap_development():
    install_requirements('local.txt')
    settings_format = 'local_{}'

    if ask_if_create_new_development_configuration():
        settings = settings_format.format(ask_username())
        create_user_config_file(settings)
        return settings

    return settings_format.format(getpass.getuser())


def bootstrap_production():
    settings = 'production'
    install_requirements('production.txt')

    if ask_if_install_crontabs():
        install_crontabs()

    return settings


def bootstrap(production=False, defaults=False):
    """Разворачивает проект в виртуальном окружении."""
    logger.force_defaults = defaults

    delete_common_files()
    make_virtualenv()
    setup_static()
    update_manage_script()
    update_project_init()

    if not production and ask_if_development():
        settings = bootstrap_development()
    else:
        settings = bootstrap_production()

    create_env_file(
        settings_module=_make_config_pythonpath(settings),
    )

    _log('Для запуска проекта осталось:')
    _log('\t - указать конфигурацию БД в {}'
         .format(ENV_FILE))
    manage_path = PROJECT_NAME + '/manage.py'
    _log('\t - выполнить {} migrate'.format(manage_path))
    _log('\t - выполнить {} runserver'.format(manage_path))
