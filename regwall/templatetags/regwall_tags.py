from django import template

from .. import mixins
from .. import settings

register = template.Library()


@register.simple_tag(takes_context=True)
def get_regwall_attempts(context):
    request = context['request']
    return request.session['regwall']['attempts']


@register.simple_tag(takes_context=True)
def get_regwall_successes(context):
    request = context['request']
    return request.session['regwall']['successes']


@register.simple_tag
def get_regwall_limit():
    return settings.REGWALL_LIMIT


@register.simple_tag
def get_regwall_expire():
    return settings.REGWALL_EXPIRE
