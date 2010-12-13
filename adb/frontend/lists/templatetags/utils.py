#! -*- coding: utf-8 -*-

from coffin import template
from urllib import unquote

from django.utils.encoding import smart_unicode


register = template.Library()


@register.filter(jinja2_only=True)
def url(arg):
    return arg.get_absolute_url()


@register.filter(jinja2_only=True)
def shorturl(url, max_length):
    # Quoting and unquoting needed for double quoted utf8 chars in URLs
    url = unicode(unquote(url.encode('utf-8')), 'utf-8')
    return url[:max_length/2] + u'…' + url[-max_length/2:] if len(url) > max_length else url