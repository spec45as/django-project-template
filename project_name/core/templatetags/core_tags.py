import os
from hashlib import md5

from django.conf import settings
from django import template


register = template.Library()


@register.simple_tag
def file_version(path):
    """Вернуть md5-хэш от статического файла."""
    full_path = os.path.join(settings.STATIC_ROOT, path)
    try:
        return md5(open(full_path, 'rb').read()).hexdigest()
    except IOError:
        return ''


@register.simple_tag(takes_context=True)
def is_view(context, view_name=None, namespace=None, output='active', **kwargs):
    """
    Вернуть `value`, если название текущего view совпадает с заданным
    значенем.

    Используется в для задания активного элемента меню.

        {% is_view "homepage" %}

    вернёт "active", если текущий view обрабатывается функцией 'homepage'.

        {% is_view namespace="forum" %}

    вернёт "active", если view, обрабатывающий запрос находится в приложении
    с пространством имёт `namespace`.
    """
    resolver_match = resolve(context['request'].path)

    if namespace and namespace == resolver_match.namespace:
        return output

    if view_name and resolver_match.url_name == view_name:
        if all(resolver_match.kwargs[k] == kwargs[k] for k in kwargs.keys()):
            return output
    return ''




@register.filter
def chunked_by(it, n):
    """
    Разбить массив на массив массивов длинной в n.
    Возвращает генераторное выражение.

    >>> x = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> chunked_by(x, 2)
    [[1,2], [3,4], [5,6], [7,8], [9]]

    Использование в шаблоне:

    {% for chunk in x|chunked_by:"2" %}
        {% for item in chunk %}
            {{ z }}
        {% endfor %},
    {% endfor %}

    Выведет: "0 1, 2 3, 4 5, 6 7, 8 9"
    """
    n = int(n)
    return (it[i:i+n] for i in xrange(0, len(it), n))




@register.filter
def make_agree_with_number(word, number):
    """Согласовать указанное слово `word` с числительным `number`."""
    try:
        parsed_word = settings.MORPH.parse(word)[0]
        result = parsed_word.make_agree_with_number(int(number)).word
    except (TypeError, AttributeError, IndexError, ValueError):
        return word

    return result
