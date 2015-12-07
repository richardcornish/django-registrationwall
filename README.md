# Django Paywall

Django Paywall is a [Django](https://www.djangoproject.com/) [app](https://docs.djangoproject.com/en/1.9/intro/reusable-apps/) that limits an [anonymous user](https://docs.djangoproject.com/en/1.9/ref/contrib/auth/#anonymous-users)'s access to a specified number of URL resources, after which the user is redirected to the [login URL](https://docs.djangoproject.com/en/1.9/ref/settings/#std:setting-LOGIN_URL). The app is modeled after the common [paywall](https://en.wikipedia.org/wiki/Paywall) scenario, which limits free access to content.

The app is almost entirely a basic [mixin](https://docs.djangoproject.com/en/1.9/topics/class-based-views/mixins/) that subclasses Django's [`AccessMixin`](https://docs.djangoproject.com/en/1.9/topics/auth/default/#django.contrib.auth.mixins.AccessMixin). It increments the number of resources the user visits and then checks the total against the `PAYWALL_LIMIT` setting. On each request, the mixin looks up and stores the current object of the view, which means the mixin should only be added to views that focus on a single object like [`DetailView`](https://docs.djangoproject.com/en/1.9/ref/class-based-views/generic-display/#detailview), although technically any view that incorporates [`SingleObjectMixin`](https://docs.djangoproject.com/en/1.9/ref/class-based-views/mixins-single-object/#singleobjectmixin) is valid. In general the use case is to count individual "detail" resources like articles or something similar in nature.

The app stores the visited resources into the session, whose session ID is stored in a cookie in the user's web browser. The app does not employ more sophisticated user tracking like IP detection and storage.

Note that the app is not a "true" paywall in the sense that it checks if an authenticated user is a valid "subscriber" or other such classification of customer. Checking for additional validity beyond an authenticated user would require additional data stored on either a customer user model or in another connected app and is outside the scope of this app. It might be easier to think of this app as a "registration wall" although customization for a more typical paywall scenario exists.

## Requirements

- \>= Django 1.9

## Installation

1. Install with [pip](https://pip.pypa.io/).

	```
	pip install -e git+https://github.com/richardcornish/django-paywall.git#egg=django-paywall
	```

2. Add to `settings.py`.

	```
	INSTALLED_APPS = (
	    # ...
	    'paywall',
	)
	```

3. Add to one of your `views.py`:

	```
	from django.views.generic import DetailView
	
	from paywall import RaisePaywallMixin
	
	
	class ArticleDetailView(RaisePaywallMixin, DetailView):
	    model = Article
	```

## Settings

Change the default behavior by adding any of these settings to `settings.py` and changing their values.

The default free resource limit is `10`. Customize with any integer.

```
PAYWALL_LIMIT = 10  # articles
```

The default expiration until resources can be freely visited again is `30` days. Customize with any integer.

```
PAYWALL_EXPIRE = 30  # days
```

News organizations often allow visitors coming from a social website, usually Google News, a "free pass" that does not count toward their free resource limit. The app's default behavior mimics this practice with a whitelist of hosts, whose default is Google, Facebook, and Twitter. Customize the list with your own hosts or empty it (`[]`) to prevent "free pass" behavior.

```
# Coming from Google, Facebook, or Twitter is always free
PAYWALL_SOCIAL = [
    'google.com',
    'facebook.com',
    'twitter.com'
]
```

## Customization

You can further customize much of the functionality of `RaisePaywallMixin` because it inherits from Django's [`AccessMixin`](https://docs.djangoproject.com/en/1.9/topics/auth/default/#django.contrib.auth.mixins.AccessMixin). Say you wanted to raise a [`PermissionDenied`](https://docs.djangoproject.com/en/1.9/ref/exceptions/#permissiondenied) exception, which would likely trip your [`403.html` template](https://docs.djangoproject.com/en/1.9/ref/views/#the-403-http-forbidden-view), instead of redirecting to the login URL.

In your own code, perhaps in a `mixins.py`, subclass `RaisePaywallMixin` and set [`raise_exception`](https://docs.djangoproject.com/en/1.9/topics/auth/default/#django.contrib.auth.mixins.AccessMixin.raise_exception) to `True`.

```
from paywall import RaisePaywallMixin


class MyCustomRaisePaywallMixin(RaisePaywallMixin):
    raise_exception = True
```

Then add your own mixin to your views.

```
from django.views.generic import DetailView

from .mixins import MyCustomRaisePaywallMixin


class ArticleDetailView(MyCustomRaisePaywallMixin, DetailView):
    model = Article
```

If you wanted a "true" paywall, override the `dispatch` method for handling authenticated users with whatever check you have on valid, likely paying, users.

```
from paywall import RaisePaywallMixin


class MyCustomRaisePaywallMixin(RaisePaywallMixin):
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_subscriber() and not self.social_pass() and self.exceeded_limit():
            return self.handle_no_permission()
        return super(MyCustomRaisePaywallMixin, self).dispatch(request, *args, **kwargs)
```

Here the custom method is `is_subscriber`, which should probably have an `is_authenticated` check and your own way of determining what a subscriber is, likely a model method on the user model. After all, just because a user is authenticated doesn't mean they are a valid subscriber.

## Templates

The app stores not just the visited resources in the session but several additional variables that can be used to provide a message to users who reached their resource limit.

- `{{ request.session.paywall_list }}`

    The list of free visited resources

- `{{ request.session.paywall_list_count }}`

    The number of free visited resources

- `{{ request.session.paywall_limit }}`

    The maximum number of free resources a user can visit

- `{{ request.session.paywall_expire }}`

    The number of days until a user can browse free resources again

For example, the [login template](https://docs.djangoproject.com/en/1.9/topics/auth/default/#django.contrib.auth.views.login) might look like:

```
{% extends "base.html" %}

{% block content %}
    {% if request.session.paywall_list_count >= request.session.paywall_limit %}
        <p>We're sorry, but you reached the limit of {{ request.session.paywall_limit }} free news articles for {{ request.session.paywall_expire }} days.</p>
        <p>Please become a subscriber to fund the important work of journalism.</p>
        <p>You read these great articles:</p>
        <ul>
            {% for article in request.session.paywall_list %}
            <li><a href="{{ article.get_absolute_url }}">{{ article.headline }}</a></li>
            {% endfor %}
        </ul>
    {% endif %}
    {# Include login stuff like the form, error handling, etc. #}
{% endblock %}
```
