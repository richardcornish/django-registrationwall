from django.conf import settings
from django.contrib.auth.mixins import AccessMixin

PAYWALL_LIMIT = getattr(settings, 'PAYWALL_LIMIT', 10)
PAYWALL_EXPIRE = getattr(settings, 'PAYWALL_EXPIRE', 30)
PAYWALL_SOCIAL = getattr(settings, 'PAYWALL_SOCIAL', ['google.com', 'facebook.com', 'twitter.com'])


class RaisePaywallMixin(AccessMixin):
    """
    View mixin that requires anonymous user's visited article list length,
    based on their browser session, to be less than the article limit setting
    """
    def passed_social(self):
        try:
            return self.request.META['HTTP_REFERER'] in PAYWALL_SOCIAL
        except KeyError:
            return False

    def exceeded_limit(self):

        # Use session if already exists or create a new one
        if 'paywall_list' in self.request.session:
            paywall_list = self.request.session['paywall_list']
        else:
            seconds = 60 * 60 * 24 * PAYWALL_EXPIRE
            self.request.session.set_expiry(seconds)
            paywall_list = []

        # Count articles if visiting for first time
        if not next((article for article in paywall_list if article['app_label'] == self.get_object()._meta.app_label and article['pk'] == self.get_object().pk), None):
            paywall_list.append({
                'app_label': self.get_object()._meta.app_label,
                'pk': self.get_object().pk,
                'url': self.get_object().get_absolute_url()
            })

        self.request.session['paywall_list'] = paywall_list
        self.request.session['paywall_list_count'] = str(len(self.request.session['paywall_list']))
        self.request.session['paywall_limit'] = str(PAYWALL_LIMIT)
        self.request.session['paywall_expire'] = str(PAYWALL_EXPIRE)
        return len(self.request.session['paywall_list']) > PAYWALL_LIMIT

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated() and not self.passed_social() and self.exceeded_limit():
            return self.handle_no_permission()
        return super(RaisePaywallMixin, self).dispatch(request, *args, **kwargs)
