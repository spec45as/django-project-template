=======================
Django project template
=======================

Шаблон проекта для Django.

Шаблон разработан с целью облегчения и ускорения процесса
развёртывания нового проекта без рутины.

**Note**: поддержка этого шаблона прекращена в пользу
cookiecutter-django_.

.. _cookiecutter-django: https://github.com/asyncee/cookiecutter-django


Features
========

- Для каждого пользователя создаётся свой конфигурационный файл
  (``local_<username>.py``) и сохраняется в репозитории.
- Конфигурация внешних сервисов из переменных окружения или файла ``conf/env``.
- Интеграция с webpack, bower и gulp.
- Поддержка ES2015, ES7, JSX, SCSS.
- Frontend-ассеты хранятся в директории ``assets``.
- Регистрация by django-allauth
- По-умолчанию установлено приложение ``django.contrib.flatpages``
  с ``ckeditor`` из коробки.
- Кастомная модель пользователя в приложении ``users``.
- Кастомные страницы ошибок 400, 403, 403 (csrf), 404 и 500.
- Поддержка Celery 4 из коробки


Requirements
============

System
------

- Bash
- Python 3.4+
- Node

Python packages (system)
------------------------

- Pip
- Django
- Jinja2


Production / deploy requirements
--------------------------------

Для запуска в продакшене может быть использован любой инструментарий.
Конфигурация для **uwsgi** и **supervisord** идёт в комплекте с
проектом, см. директорию ``conf``.


Quickstart
==========
Создать проект можно командой::

    django-admin.py startproject --template=https://github.com/asyncee/django-project-template/zipball/master --name=gulpfile.js,.bowerrc,tox.ini --extension py,template,rst <имя проекта>

Разворачивание **для разработки** в виртуальном окружении::

    python bootstrap.py

Разворачивание **для продакшена**::

    python bootstrap.py --production

Произойдёт создание виртуального окружения, генерация секретного
ключа проекта, установка зависимостей и создание конфигурационных
файлов проекта.

Далее необходимо будет сконфигурировать базу данных/почту::

    vim conf/env

И отредактировать настройки проекта::

    vim project_name/settings/base.py          # общие настройки
    vim project_name/settings/production.py    # продакшен
    vim project_name/settings/local_<user>.py  # пользовательские настройки

Провести миграции и запустить сервер::

    src/manage.py migrate
    src/manage.py runserver  # если необходимо запустить только сервер django, либо
    gulp                     # если необходимо работать с фронтендом


Testing
-------
Шаблон включает в себя конфигурацию для тестирования проекта
с помощью pytest и tox.

Для запуска тестов достаточно выполнить команду::

    tox

При этом виртуальное окружение активировать не нужно.
