# coding: utf-8

import jinja2

from .path import base_path
from .settings import ENV_FILE


def render(src, dst, **kwargs):
    """
    Отрендерить jinja2 шаблон.

    Аргументы:
        src - путь к шаблону
        dst - путь к выходному файлу
        **kwargs - параметры для передачи в шаблон
    """
    kwargs.update({
        'env_file': base_path(ENV_FILE),
    })
    with open(src) as f:
        template = jinja2.Template(f.read())
    with open(dst, 'w') as f:
        f.write(template.render(**kwargs))
