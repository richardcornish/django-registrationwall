from __future__ import unicode_literals

try:
    from django.contrib.auth.mixins import AccessMixin
except ImportError:
    raise ImportError('Django Registration Wall requires Django 1.9 or greater.')

import tldextract

from . import settings


class RaiseRegWallMixin(AccessMixin):
    """View mixin that increments an anonymous user's article count."""

    def get_or_create_regwall_list(self, list_name):
        try:
            regwall = self.request.session['regwall']
        except KeyError:
            seconds = 60 * 60 * 24 * settings.REGWALL_EXPIRE
            self.request.session.set_expiry(seconds)
            self.request.session['regwall'] = {}
            regwall = self.request.session['regwall']
        try:
            return regwall[list_name]
        except KeyError:
            regwall[list_name] = []
            self.request.session.modified = True
            return regwall[list_name]

    def increment_regwall_list(self, regwall_list):
        obj = self.get_object()
        regwall_list.append({
            'app_label': obj._meta.app_label,
            'id': obj.id,
            'headline': obj.headline or obj.title or obj.name or '',
            'url': obj.get_absolute_url(),
        })
        self.request.session.modified = True

    def is_under_limit(self, regwall_list):
        return len(regwall_list) <= settings.REGWALL_LIMIT

    @property
    def is_authenticated(self):
        try:
            return self.request.user.is_authenticated()
        except TypeError:
            return self.request.user.is_authenticated

    @property
    def is_social(self):
        try:
            referer = self.request.META['HTTP_REFERER']
        except KeyError:
            return False
        ext = tldextract.extract(referer)
        return ext.domain in settings.REGWALL_SOCIAL

    @property
    def has_visited(self):
        successes_list = self.get_or_create_regwall_list('successes')
        value_list = [article[key] for article in successes_list for key in article]
        obj = self.get_object()
        return obj.get_absolute_url() in value_list

    def dispatch(self, request, *args, **kwargs):
        attempts_list = self.get_or_create_regwall_list('attempts')
        successes_list = self.get_or_create_regwall_list('successes')
        if not self.is_authenticated and not self.is_social and not self.has_visited:
            self.increment_regwall_list(attempts_list)
            if self.is_under_limit(attempts_list):
                self.increment_regwall_list(successes_list)
            else:
                return self.handle_no_permission()
        return super(RaiseRegWallMixin, self).dispatch(request, *args, **kwargs)
