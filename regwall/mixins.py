from __future__ import unicode_literals

try:
    from urlparse import urlparse  # Python 2
except ImportError:
    from urllib.parse import urlparse

try:
    from django.contrib.auth.mixins import AccessMixin
except ImportError:
    raise ImportError('Django Registration Wall requires Django 1.9 or greater.')

from . import settings


class RaiseRegWallMixin(AccessMixin):
    """View mixin that increments an anonymous user's article count."""

    def get_expire_seconds(self):
        return 60 * 60 * 24 * settings.REGWALL_EXPIRE

    def get_social_list(self):
        social_list = settings.REGWALL_SOCIAL
        social_list.extend(['www.' + social for social in social_list])
        return social_list

    def get_regwall_list(self):
        try:
            return self.request.session['regwall_list']
        except KeyError:
            seconds = self.get_expire_seconds()
            self.request.session.set_expiry(seconds)
            self.request.session['regwall_list'] = []
            return self.request.session['regwall_list']

    def increment_regwall_list(self):
        obj = self.get_object()
        regwall_list = self.get_regwall_list()
        regwall_list.append({
            'app_label': obj._meta.app_label,
            'id': obj.id,
            'headline': obj.headline or obj.title or obj.name or '',
            'url': obj.get_absolute_url(),
        })
        self.request.session.modified = True

    def is_authenticated(self):
        return self.request.user.is_authenticated()

    def is_social(self):
        try:
            url_tuple = urlparse(self.request.META['HTTP_REFERER'])
        except KeyError:
            return False
        return url_tuple.netloc in self.get_social_list()

    def is_under_limit(self):
        regwall_list = self.get_regwall_list()
        return len(regwall_list) <= settings.REGWALL_LIMIT

    def has_visited(self):
        obj = self.get_object()
        regwall_list = self.get_regwall_list()
        value_list = [article[key] for article in regwall_list for key in article]
        return obj.get_absolute_url() in value_list

    def dispatch(self, request, *args, **kwargs):
        if not self.is_authenticated() and not self.is_social() and not self.has_visited():
            self.increment_regwall_list()
            if not self.is_under_limit():
                return self.handle_no_permission()
        return super(RaiseRegWallMixin, self).dispatch(request, *args, **kwargs)
