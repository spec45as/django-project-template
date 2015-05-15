# coding: utf-8

from __future__ import print_function, unicode_literals, division

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from {{ project_name }} import views


project_urls = [
    url(r'^$', views.home, name='home'),
    url(r'^robots.txt$', views.robots_txt, name='robots_txt'),
]


apps_urls = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
]

urlpatterns = project_urls + apps_urls


if settings.DEBUG:
    urlpatterns.extend(
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) +
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )

    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
