# coding: utf-8

from django.apps import AppConfig


class DefaultConfig(AppConfig):
    name = 'users'
    verbose_name = 'Пользователи'

    def ready(self):
        # импортировать сигналы для их регистрации
        import users.signals
