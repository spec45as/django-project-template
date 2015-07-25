# coding: utf-8

from django.db import models


class DateTimeMixin(models.Model):
    date_created = models.DateTimeField(
        'Дата создания', auto_now_add=True)
    date_updated = models.DateTimeField(
        'Дата обновления', auto_now=True)

    class Meta:
        abstract = True
