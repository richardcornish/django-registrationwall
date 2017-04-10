from django import template

from .. import settings

register = template.Library()


@register.simple_tag(takes_context=True)
def get_regwall_list(context):
    request = context['request']
    return request.session.get('regwall_list', None)


@register.simple_tag(takes_context=True)
def get_regwall_list_read(context):
    request = context['request']
    try:
        return request.session['regwall_list'][:settings.REGWALL_LIMIT]
    except KeyError:
        return []


@register.simple_tag
def get_regwall_limit():
    return settings.REGWALL_LIMIT


@register.simple_tag
def get_regwall_expire():
    return settings.REGWALL_EXPIRE
