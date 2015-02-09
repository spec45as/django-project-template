# coding: utf-8

"""
Модуль для переопределения переводов из сторонних приложений.

Для переопределения перевода необходимо:

    1. Найти оригинальную строку, перевод для которой необходимо
        заменить.
    2. Записать её в массив `messages_to_override`.
    3. Выполнить команды:

        cd {{ project_name }}
        ../manage.py makemigrations -l ru

        После этого будет сгенерирован файл с переводом с нужными
        строками.

    4. Перевести строку в сгенерированном файле:

        vim {{ project_name }}/locale/ru/LC_MESSAGES/django.po

    5. Скомпилировать перевод:

        cd {{ project_name }}
        ../manage.py compilemessages -l ru

    6. Перезапустить сервер. Готово.
"""

_ = lambda s: s

messages_to_override = [
    #_("A string from another package to override on package-level"),
]
