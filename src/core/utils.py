# coding: utf-8

import os
from hashlib import md5

from django.template.loader import render_to_string
from django.conf import settings


def upload_to(directory=None):
    """Загрузить файл в директорию `directory` с хешированным именем."""

    def uploader(instance, filename):
        ext = os.path.splitext(filename)[1]
        h = md5(filename.encode('utf-8')).hexdigest()
        parts = [h[:2], h[2:4], h + ext]
        if directory is not None:
            parts.insert(0, directory)
        return '/'.join(parts)

    return uploader


def send_mail(email, subject, template_html, template_txt, context, **kwargs):
    """
    Отправить email пользователю.

    Аргументы:
        email - адрес электронной почты
        subject - заголовок письма
        template_html - путь до шаблона с html разметкой
        template_txt - путь до текстового шаблона
        context - словарь с данными, с которыми будут отрендерены шаблоны
    """
    email_html = render_to_string(template_html, context)
    email_text = render_to_string(template_txt, context)
    send_mail(
        auth_user=settings.EMAIL_HOST_USER,
        auth_password=settings.EMAIL_HOST_PASSWORD,
        from_email=settings.DEFAULT_FROM_EMAIL,
        subject=subject,
        recipient_list=[email],
        fail_silently=kwargs.pop('fail_silently', True),
        html_message=email_html,
        message=email_text,
        **kwargs
    )
