# coding: utf-8

from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserChangeForm(auth_forms.UserChangeForm):
    pass


class UserCreationForm(auth_forms.UserCreationForm):
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(**{User.USERNAME_FIELD + '__iexact': username}).exists():
            raise forms.ValidationError(
                User._meta.get_field(User.USERNAME_FIELD).error_messages['unique'],
                code='unique',
            )
        return username
