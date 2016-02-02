# coding: utf-8

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from {{ project_name }} import views


handler400 = 'core.views.bad_request'
handler403 = 'core.views.permission_denied'
handler404 = 'core.views.page_not_found'
handler500 = 'core.views.server_error'


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^robots.txt$', views.robots_txt, name='robots_txt'),

    url(r'^admin/', admin.site.urls),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^accounts/', include('allauth.urls')),
]


if settings.DEBUG:
    urlpatterns.extend(
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) +
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )

    urlpatterns += [
        url(r'^400/$', 'core.views.bad_request', {'exception': 'test'}),
        url(r'^403/$', 'core.views.permission_denied', {'exception': 'test'}),
        url(r'^403_csrf/$', 'core.views.csrf_failure', {'force_display': True}),
        url(r'^404/$', 'core.views.page_not_found', {'exception': 'test'}),
        url(r'^500/$', 'core.views.server_error'),
    ]

    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
