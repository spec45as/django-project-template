# coding: utf-8

from __future__ import print_function, unicode_literals, division

from django.db import models


class DateTimeMixin(models.Model):
    date_created = models.DateTimeField(
        u'Дата создания', auto_now_add=True)
    date_updated = models.DateTimeField(
        u'Дата обновления', auto_now=True)

    class Meta:
        abstract = True
