# coding: utf-8

import os
import base64
import getpass

from fabric.operations import local, prompt
from fabric.context_managers import lcd
from fabric.contrib.console import confirm

import jinja2


# full path to this file
BASE_PATH = os.path.abspath(os.path.dirname(__file__))

PROJECT_NAME = '{{ project_name }}'
PROJECT_PATH = os.path.join(BASE_PATH, PROJECT_NAME)
USER_CONFIG_FILE = 'conf/config.ini'


def make_virtualenv():
    """Creates virtualenv in local directory."""
    local('virtualenv env')


def install_requirements():
    """
    Installs requirements to the local virtualenv.
    If wheels directory is not None then wheel installation is performed.
    """
    local('source env/bin/activate && pip install -r requirements.txt',
          shell='bash')


def generate_secret():
    """Generates 512-length secret key and writes it to the file `.secret`."""
    SECRET_FILE = os.path.normpath(os.path.join(PROJECT_NAME, '../conf/secret'))

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
            local_template_path = 'conf/local_settings.template'
            result_filename = 'local_%s.py' % username
            result_file_path = os.path.join(PROJECT_PATH, 'settings',
                                            result_filename)

            # create local_<user>.py
            with open(result_file_path, 'w') as dest, open(local_template_path, 'r') as src:
                dest.write(src.read())
                print 'created {}'.format(result_file_path)

            # create config.ini
            with open('conf/config.ini', 'w') as dest, open('conf/config.ini.template', 'r') as src:
                dest.write(src.read())
                print 'created {}'.format(USER_CONFIG_FILE)

            # update manage.py
            manage_py_template = jinja2.Template(open('conf/manage.py.template').read())
            output = manage_py_template.render(config_name=result_filename[:-3])
            with open('manage.py', 'w') as f:
                f.write(output)
                print 'updated manage.py'

            print ('now you should modify your database settings in {}'
                   .format(result_file_path))


def bootstrap():
    """Installs everything."""
    make_virtualenv()
    install_requirements()
    generate_secret()
    create_user_config_file()
