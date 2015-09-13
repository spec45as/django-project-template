# coding: utf-8

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import register

from users import models as m


@admin.register(m.User)
class UserAdmin(UserAdmin):
    pass
