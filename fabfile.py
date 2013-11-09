# coding: utf-8

import re
import os
import sys
import base64
import getpass

from fabric.operations import local, prompt
from fabric.context_managers import lcd
from fabric.contrib.console import confirm


MAKE = 'gmake' if 'freebsd' in sys.platform else 'make'

# full path to this file
BASE_PATH = os.path.abspath(os.path.dirname(__file__))

PROJECT_NAME = '{{ project_name }}'
PROJECT_PATH = os.path.join(BASE_PATH, PROJECT_NAME)

CRONTAB_PRE = '#-- crontab {name}\n'
CRONTAB_LINE = '{line}\n'
CRONTAB_POST = '#-- end crontab {name}\n'
CRONTAB_TEMPLATE = '{pre}{line}{post}'.format(pre=CRONTAB_PRE,
                                              post=CRONTAB_POST,
                                              line=CRONTAB_LINE)


def _load_settings(fname='config.yml'):
    import yaml
    return yaml.load(open(fname))


def _read_crontab():
    """Reads user crontab into string and returns it w/o modifications."""
    crontab = os.popen('crontab -l')
    lines = crontab.read()
    crontab.close()
    return lines


def _write_crontab(data):
    """Re-writes whole crontab with data."""
    fallback = _read_crontab()
    crontab = os.popen('crontab -', 'w')
    crontab.write(data)
    code = crontab.close()
    if code:
        fb = os.popen('crontab -', 'w')
        fb.write(fallback)
        fb.close()
        print 'failed to install crontab {}'.format(name)


def _add_task(name, line):
    """Adds new task or updates existing."""
    _del_task(name)
    lines = _read_crontab()
    task = CRONTAB_TEMPLATE.format(name=name, line=line)
    data = '{}\n{}'.format(lines, task)
    _write_crontab(data)


def _del_task(name):
    """Deletes existing task with supplied name."""
    lines = _read_crontab()
    pre = CRONTAB_PRE.format(name=name)
    post = CRONTAB_POST.format(name=name)
    pattern = r'(\n{pre}.*?{post})'.format(pre=pre, post=post)

    result = re.sub(pattern, '', lines, count=0, flags=re.M|re.S)
    _write_crontab(result)


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


def install_crontabs():
    """Installs project crontabs."""
    crontabs = _load_settings()['crontabs']

    if crontabs is not None:
        for crontab in crontabs:
            name = crontab['name']
            command = crontab['crontab'].format(
                base_path=BASE_PATH,
                project_path=PROJECT_PATH,
                project_name=PROJECT_NAME,
            )
            print 'installing crontab "{}": {}'.format(name, command)
            _add_task(name, command)


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


def install_nodejs_modules():
    """Installs nodejs minification modules."""
    modules = ['uglify-js', 'clean-css']
    local('bin/npm install -g {}'.format(' '.join(modules)))


def install_nodejs(version='0.10.21', cpus=1):
    """
    Installs nodejs in local directory.

    Downloads nodejs sources, compiles it in temp directory with `cpus` number
    of jobs (1 is by default), then installs in local directory. Temporary
    directory removed after installing.
    """
    node_file = 'node-v{}.tar.gz'.format(version)
    node_url = 'http://nodejs.org/dist/v{}/{}'.format(version, node_file)
    build_dir = 'fabric_build'

    local('mkdir -p {}'.format(build_dir))
    with lcd(build_dir):
        local('wget {} -O {}'.format(node_url, node_file))
        local('tar xzf {}'.format(node_file))
        with lcd('node-v{}'.format(version)):
            local('./configure --prefix={}'.format(BASE_PATH))
            local('{} -j{}'.format(MAKE, cpus))
            local('{} install'.format(MAKE))
    local('rm -rf {}'.format(build_dir))

    install_nodejs_modules()


def _minify(section_name, minify_cmd):
    sections = _load_settings()[section_name]
    if sections:
        for section in sections:
            input_files = section['from']
            output_file = section['to']
            if not isinstance(input_files, list):
                input_files = [input_files]
            minify_cmd(input_files, output_file)


def _minify_js(input_files, output_file):
    cmd = 'PATH=$PATH:`pwd`/bin bash -c "bin/uglifyjs {} -o {}"'.format(
        ' '.join(input_files), output_file
    )
    local(cmd)


def _minify_css(input_files, output_file):
    cmd = 'PATH=$PATH:`pwd`/bin bash -c "cat {} | bin/cleancss -o {}"'.format(
        ' '.join(input_files), output_file
    )
    local(cmd)


def minifycss():
    _minify('minify_css', _minify_css)


def minifyjs():
    _minify('minify_js', _minify_js)


def minify():
    """Minifies js and css for whole project."""
    minifyjs()
    minifycss()


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


def bootstrap(nonode=None, cpus=1, wheels=None, noindex=False):
    """Installs everything."""
    make_virtualenv()
    install_requirements(wheels, noindex)
    generate_secret()
    create_user_config_file()
