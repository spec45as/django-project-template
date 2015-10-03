# coding: utf-8

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import register

from users import models as m
from users import forms as f


@admin.register(m.User)
class UserAdmin(UserAdmin):
    form = f.UserChangeForm
    add_form = f.UserCreationForm

    # override fieldsets if new fields were added
    # fieldsets = ...
