#!/usr/bin/python

# coding: utf-8

from __future__ import print_function

import argparse
import getpass

from deploy import (
    prompt, confirm, config_path,
    create_virtualenv, install_requirements,
    create_env_file, install_crontabs, create_user_config_file,
    setup_static, delete_common_files, logger,
)
from deploy.settings import ENV_FILE, PROJECT_NAME


def ask_if_development():
    return confirm('Проект разворачивается для локальной разработки?')


def ask_if_install_crontabs():
    return confirm('Установить задачи в крон от текущего пользователя?')


def ask_if_create_new_development_configuration():
    return confirm('Создать новую конфигурацию проекта для разработки?')


def ask_username(question=None):
    return prompt(
        question or 'Имя пользователя', default=getpass.getuser())


def bootstrap_production():
    delete_common_files()
    create_virtualenv()
    setup_static()

    install_requirements('production.txt')

    if ask_if_install_crontabs():
        install_crontabs()

    create_env_file(
        settings_module=config_path('production'),
    )


def bootstrap_development():
    delete_common_files()
    create_virtualenv()
    setup_static()

    install_requirements('local.txt')
    settings_format = 'local_{}'

    if ask_if_create_new_development_configuration():
        settings = settings_format.format(ask_username())
        create_user_config_file(settings)
    else:
        settings = settings_format.format(getpass.getuser())

    create_env_file(
        settings_module=config_path(settings),
    )

    logger.info('Для запуска проекта осталось:')
    logger.info('\t - указать конфигурацию БД в {}'
         .format(ENV_FILE))
    managepy_path = PROJECT_NAME + '/manage.py'
    logger.info('\t - выполнить {} migrate'.format(managepy_path))
    logger.info('\t - выполнить {} runserver'.format(managepy_path))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Deploy project')
    parser.add_argument('-p', '--production', dest='production',
                        action='store_const', const=True,
                        default=False)

    args = parser.parse_args()

    if args.production:
        logger.info('Проект разворачивается для продакшена.')
        bootstrap_production()
    else:
        logger.info('Проект разворачивается для разработки.')
        bootstrap_development()
