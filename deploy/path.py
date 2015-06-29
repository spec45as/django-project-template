# coding: utf-8

import os

from . import settings as s


def base_path(*path):
    """Возвратить полный путь относительно корневой директории."""
    return os.path.join(s.BASE_PATH, *path)


def manage_path(*path):
    """Возвратить полный путь относительно manage.py."""
    return os.path.join(s.MANAGE_PATH, *path)


def project_path(*path):
    """Возвратить полный путь относительно проекта (settings.py)."""
    return os.path.join(s.PROJECT_PATH, *path)


def config_path(config_name):
    return s.PROJECT_NAME + '.settings.' + config_name
