# coding: utf-8

from __future__ import print_function, unicode_literals, division

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin


project_urlpatterns = patterns('{{ project_name }}.views',
    url(r'^$', 'home', name='home'),
    url(r'^robots.txt$', 'robots_txt', name='robots_txt'),
)


apps_patterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns = project_urlpatterns + apps_patterns


if settings.DEBUG:
    urlpatterns += (
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) +
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )

    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
