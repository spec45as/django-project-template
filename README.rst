=======================
Django project template
=======================

Шаблон проекта для Django.

Шаблон разработан с целью облегчения и ускорения процесса
развёртывания нового проекта без рутины. Ориентирован
на разработку проекта несколькими людьми, поэтому для каждого
пользователя создаётся свой конфигурационный файл
(``local_setings.py``).

Настройки используемых сервисов, таких как БД и почты и секретный
ключ вынесены в отдельный файл ``conf/config.ini`` и не должны
храниться в системе контроля версий (смотри ``.gitignore``).

Вместе с проектом поставляется twitter bootstrap 3.


Requirements
============

- python >= 2.7
- django >= 1.6
- pip
- virtualenv
- fabric
- jinja2
- bash

Последние версии pip и setuptools можно установить командой::

    pip install --upgrade pip setuptools


Quickstart
==========
Для создания проекта необходимо выполнить действия:

    django-admin.py startproject --template=https://github.com/asyncee/django-project-template/zipball/master --extension py,template,ini <имя проекта>

Для разворачивания проекта в виртуальном окружении необходимо
выполнить команду::

    fab bootstrap

Произойдёт создание виртуального окружения, генерация секретного
ключа проекта, установка зависимостей и создание конфигурационных
файлов проекта.

Далее необходимо будет сконфигурировать базу данных/почту::

    vim conf/config.ini

И отредактировать настройки проекта::

    vim <название проекта>/settings/base.py          # общие настройки
    vim <название проекта>/settings/production.py    # продакшен
    vim <название проекта>/settings/local_<user>.py  # пользовательские настройки

Инициализировать БД::

    python manage.py migrate --settings=project_name.settings.local_username

Чтобы запустить проект в режиме дебага::

    # to run server
    python manage.py runserver --settings=project_name.settings.local_username

    # to syncdb
    python manage.py migrate --settings=project_name.settings.local_username

Параметр ``--settings`` можно опустить, так как после разворачивания
скрипт сам обновит файл `manage.py`.

Чтобы запустить проект на боевом сервере, можно воспользоваться
шаблонами конфигурации ``uwsgi`` и ``supervisor`` из директории
**templates**.


Configuration
-------------
Файлы конфигруации располагаются следующим образом:

``conf/config.ini`` - конфигурация реквизитов доступа к внешним ресурсам
``<project_name>/settings/base.py`` - основной конфиг проекта
``<project_name>/settings/production.py`` - конфиг для продакшена
``<project_name>/settings/local_user.py`` - конфиг для разработки

Файл `config.ini` должен быть уникальным для production
и development окружений и не должен храниться в VCS.
Все конфигурационные файлы из директории `settings` могут (и должны)
быть добавлены в систему контроля версий.


Directory structure
-------------------
Конфигруация директорий стандартна::

    static/
        css/
        js/
        img/
        vendor/
            bootstrap/

Где vendor - директория для ресурсов от сторонних разработчиков,
именно там можно найти установленный по-умолчанию twitter bootstrap.
