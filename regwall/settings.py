from __future__ import unicode_literals

from django.conf import settings


REGWALL_LIMIT = getattr(settings, 'REGWALL_LIMIT', 10)

REGWALL_EXPIRE = getattr(settings, 'REGWALL_EXPIRE', 30)

REGWALL_SOCIAL = getattr(settings, 'REGWALL_SOCIAL', [
    'google.com',
    'facebook.com',
    'twitter.com',
])
