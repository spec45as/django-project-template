# coding: utf-8

import os

PROJECT_NAME = '{{ project_name }}'
# Путь до корня проекта
BASE_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')
)
# Путь до manage.py
MANAGE_PATH = os.path.join(BASE_PATH, PROJECT_NAME)
# Путь до директории проекта с файлом settings.py
PROJECT_PATH = os.path.join(MANAGE_PATH, PROJECT_NAME)

ENV_FILE = 'conf/env'
