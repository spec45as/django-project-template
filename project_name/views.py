# coding: utf-8

from __future__ import print_function, unicode_literals, division

from django.shortcuts import render


def home(request):
    return render(request, 'home.html', {})


def robots_txt(request):
    return render(
        request, 'robots.txt', {}, content_type='text/plain')
