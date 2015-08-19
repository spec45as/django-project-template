import os
from hashlib import md5

from django.conf import settings
from django import template


register = template.Library()


@register.simple_tag
def file_version(path):
    full_path = os.path.join(settings.STATIC_ROOT, path)
    return md5(open(full_path, 'rb').read()).hexdigest()
