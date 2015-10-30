# coding: utf-8

from django.db import models


class DateTimeMixin(models.Model):
    date_created = models.DateTimeField(
        'Дата создания', auto_now_add=True)
    date_updated = models.DateTimeField(
        'Дата обновления', auto_now=True)

    class Meta:
        abstract = True


class MetaFieldsMixin(models.Model):
    meta_title = models.CharField(
        'Тег <title>', max_length=255, blank=True, default='')
    meta_keywords = models.TextField(
        'Тег <keywords>', blank=True, default='')
    meta_description = models.TextField(
        'Тег <description>', blank=True, default='')

    class Meta:
        abstract = True
