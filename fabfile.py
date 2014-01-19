# coding: utf-8

import os
import base64
import getpass

from fabric.operations import local, prompt
from fabric.context_managers import lcd
from fabric.contrib.console import confirm


# full path to this file
BASE_PATH = os.path.abspath(os.path.dirname(__file__))

PROJECT_NAME = '{{ project_name }}'
PROJECT_PATH = os.path.join(BASE_PATH, PROJECT_NAME)


def make_virtualenv():
    """Creates virtualenv in local directory."""
    local('virtualenv env')


def install_requirements(wheels=None, noindex=False):
    """
    Installs requirements to the local virtualenv.
    If wheels directory is not None then wheel installation is performed.
    """
    if wheels is not None:
        source = 'source env/bin/activate'
        index = '--no-index' if noindex else ''
        pip_wheels = ('pip install --use-wheel {no_index} --find-links={wheels}'
                      ' -r requirements.txt'.format(no_index=index, wheels=wheels))
        local('{} && {}'.format(source, pip_wheels), shell='bash')
    else:
        local('source env/bin/activate && pip install -r requirements.txt',
              shell='bash')


def make_wheels(path='./wheels'):
    """Packages all requirements into specified directory using wheel format (*.whl)."""
    local('mkdir -p {}'.format(path))
    local('pip wheel --wheel-dir={} -r requirements.txt'.format(path))


def generate_secret():
    """Generates 512-length secret key and writes it to the file `.secret`."""
    SECRET_FILE = os.path.join(PROJECT_NAME, '.secret')

    with open(SECRET_FILE, 'w') as f:
        secret_key = base64.urlsafe_b64encode(os.urandom(512))
        f.write(secret_key)
        print 'generated secret key: {}'.format(SECRET_FILE)


def create_user_config_file():
    print
    if confirm('Do you want to create your new development configuration?'):
        username = prompt('Enter your username',
                          default=getpass.getuser(),
                          validate=r'^.*$')
        with lcd(PROJECT_NAME):
            ini_file = '.config-dev-{}.ini'.format(username)
            py_file = 'local_settings_{}.py'.format(username)
            local('cp .config-dev-example.ini {}'.format(ini_file))
            local('cp local_settings_debug.py {}'.format(py_file))
            with open(os.path.join(PROJECT_PATH, py_file), 'r+') as f:
                data = f.read().replace('.config-dev-example.ini', ini_file)
                f.seek(0)
                f.write(data)
                f.truncate()

            print 'created {}'.format(ini_file)
            print 'created {}'.format(py_file)
            print ('now you should modify your database settings in {}'
                   .format(ini_file))
            print 'you can run django development server with following command:'
            print ('\tpython manage.py runserver --settings={}'
                   '.local_settings_{}'.format(PROJECT_NAME, username))
            print "but remeber to source your virtual env first:"
            print '\tsource env/bin/activate'


def bootstrap(wheels=None, noindex=False):
    """Installs everything."""
    make_virtualenv()
    install_requirements(wheels, noindex)
    generate_secret()
    create_user_config_file()
