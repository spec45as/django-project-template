# coding: utf-8

from django import forms
from django.contrib.auth import forms as auth_forms

from users import models as m


class UserChangeForm(auth_forms.UserChangeForm):
    pass


class UserCreationForm(auth_forms.UserCreationForm):
    pass
