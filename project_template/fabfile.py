# coding: utf-8

import os
import base64

from fabric.operations import local
from fabric.context_managers import lcd, settings, hide
from fabric.api import env, task


def _relative_dir(dirs=None):
    if dirs is None:
        dirs = []
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *dirs)


def make_virtualenv():
    local('virtualenv env')


def install_requirements():
    local('source env/bin/activate && pip install -r requirements.txt',
          shell='bash')


def generate_secret():
    SECRET_FILE = os.path.join('{{project_name}}', '.secret')

    with open(SECRET_FILE, 'w') as f:
        secret_key = base64.urlsafe_b64encode(os.urandom(512))
        f.write(secret_key)
        print 'generated secret key: {}'.format(SECRET_FILE)


def on_complete():
    print ('Now go to {{ project_name }} directory and configure database/mail,'
           ' using example configs. You may copy and extend your local_settings'
           ' by appending your name to the file, e.g. local_settings_username.py,'
           ' or just use existing templates.')


def install_nodejs(version='0.10.12', cpus=1):
    node_file = 'node-v{}.tar.gz'.format(version)
    node_url = 'http://nodejs.org/dist/v{}/{}'.format(version, node_file)
    gpg_file = 'SHASUMS256.txt'
    gpg_url = 'http://nodejs.org/dist/v{}/{}'.format(version, gpg_file)
    build_dir = 'fabric_build'

    print 'installing node.js v{}'.format(version)
    local('mkdir -p {}'.format(build_dir))
    with lcd(build_dir):
        local('wget {} -O {}'.format(node_url, node_file))
        local('tar xzf {}'.format(node_file))
        with lcd('node-v{}'.format(version)):
            local('./configure --prefix={}'.format(_relative_dir()))
            local('make -j{}'.format(cpus))
            local('make install')
    local('rm -rf {}'.format(build_dir))
    print 'install complete'


def install_nodejs_modules():
    modules = ['uglify-js', 'stylus', 'clean-css']
    local('bin/npm install -g {}'.format(' '.join(modules)))


def minifyjs():
    src_dir = 'static/js/src'
    build_dir = 'static/js/build'
    local('mkdir -p {}'.format(build_dir))
    js_files = []
    for root, dirs, files in os.walk(src_dir):
        for fname in files:
            if fname.endswith('.js'):
                js_files.append(os.path.join(root, fname))
    local('bin/uglifyjs {} -o {}/script.js'.format(
            ' '.join(js_files), build_dir
          ))


def minifycss():
    src_dir = 'static/css/src'
    styl_dir = 'static/css/styl'
    build_dir = 'static/css/build'

    local('bin/stylus < {}/style.styl > {}/style.css'.format(styl_dir, src_dir))
    local('cat {src}/normalize.css {src}/foundation.min.css {src}/style.css |'
          ' bin/cleancss -o {build}/style.css'.format(
            src=src_dir, build=build_dir
          ))


def minify():
    minifyjs()
    minifycss()


def bootstrap():
    make_virtualenv()
    install_requirements()
    generate_secret()
    install_nodejs()
    install_nodejs_modules()
    on_complete()
