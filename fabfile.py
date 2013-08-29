# coding: utf-8

import os
import base64
import getpass

from fabric.operations import local, prompt
from fabric.context_managers import lcd
from fabric.contrib.console import confirm


def _absolute_dir(*dirs):
    """Returns absolute path to this file, joined with dirs."""
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *dirs)


PROJECT_NAME = '{{ project_name }}'
PROJECT_PATH = _absolute_dir(PROJECT_NAME)

CSS_SRC_DIR = os.path.join(PROJECT_PATH, 'static/css/src')
CSS_BUILD_DIR = os.path.join(PROJECT_PATH, 'static/css/build')
CSS_STYLUS_DIR = os.path.join(PROJECT_PATH, 'static/css/styl')

JS_SRC_DIR = os.path.join(PROJECT_PATH, 'static/js/src')
JS_BUILD_DIR = os.path.join(PROJECT_PATH, 'static/js/build')


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
    local('mkdir -p {}'.format(path))
    local('pip wheel --wheel-dir={} -r requirements.txt'.format(path))


def generate_secret():
    """Generates 512-length secret key and writes it to the file `.secret`."""
    SECRET_FILE = os.path.join(PROJECT_NAME, '.secret')

    with open(SECRET_FILE, 'w') as f:
        secret_key = base64.urlsafe_b64encode(os.urandom(512))
        f.write(secret_key)
        print 'generated secret key: {}'.format(SECRET_FILE)


def install_nodejs(version='0.10.12', cpus=1):
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
            local('./configure --prefix={}'.format(_absolute_dir()))
            local('make -j{}'.format(cpus))
            local('make install')
    local('rm -rf {}'.format(build_dir))


def install_nodejs_modules():
    """Installs nodejs minification modules."""
    modules = ['uglify-js', 'stylus', 'clean-css']
    local('bin/npm install -g {}'.format(' '.join(modules)))


def minifyjs():
    """Minifies all *.js files found in js/build directory to js/src/script.js."""
    with lcd(PROJECT_NAME):
        local('mkdir -p {}'.format(JS_BUILD_DIR))
        js_files = []
        for root, dirs, files in os.walk(JS_SRC_DIR):
            for fname in files:
                if fname.endswith('.js'):
                    js_files.append(os.path.join(root, fname))
    if js_files:
        local('PATH=$PATH:`pwd`/bin bash -c "bin/uglifyjs {} -o {}/script.min.js"'.format(
            ' '.join(js_files), JS_BUILD_DIR
        ))
    else:
        print 'no javascript files to minify found'


def stylus_convert():
    """Processes all *.styl files from css/styl to css/src."""
    for root, dirs, files in os.walk(CSS_STYLUS_DIR):
        for fname in files:
            if fname.endswith('.styl'):
                local('PATH=$PATH:`pwd`/bin bash -c "bin/stylus < {} > {}"'.format(
                    os.path.join(root, fname),
                    os.path.join(CSS_SRC_DIR, fname.replace('.styl', '.css')),
                ))


def minifycss():
    """Minifies css files from css/src to css/build."""
    css_files = []
    for root, dirs, files in os.walk(CSS_SRC_DIR):
        for fname in files:
            if fname.endswith('.css'):
                css_files.append(os.path.join(root, fname))
    if css_files:
        local('PATH=$PATH:`pwd`/bin bash -c "cat {} | bin/cleancss -o {}/style.min.css"'.format(
            ' '.join(css_files), CSS_BUILD_DIR
        ))
    else:
        print 'no css files to minify found'


def minify():
    """Minifies js and css for whole project."""
    minifyjs()
    stylus_convert()
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
    if nonode is None:
        install_nodejs(cpus=cpus)
        install_nodejs_modules()
    create_user_config_file()
