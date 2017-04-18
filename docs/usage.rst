.. _usage:

Usage
*****

Views
=====

The app is almost entirely a `mixin <https://docs.djangoproject.com/en/1.11/topics/class-based-views/mixins/>`_ that subclasses Django's |AccessMixin|_. Import the mixin and subclass it in a ``DetailView`` or a view that uses ``SingleObjectMixin``.

.. code-block:: python

   from django.views.generic import DetailView

   from regwall.mixins import RaiseRegWallMixin

   from .models import Article


   class ArticleDetailView(RaiseRegWallMixin, DetailView):
       model = Article

.. |AccessMixin| replace:: ``AccessMixin``
.. _AccessMixin: https://docs.djangoproject.com/en/1.11/topics/auth/default/#django.contrib.auth.mixins.AccessMixin

On each request, the mixin increments the number of consumed resources and checks its count against the ``REGWALL_LIMIT`` setting. Resources contain information about each view's main object, which means the mixin expects to be added to views that focus on a single object such as |DetailView|_, although technically any view that incorporates |SingleObjectMixin|_ is valid.

.. |DetailView| replace:: ``DetailView``
.. _DetailView: https://docs.djangoproject.com/en/1.11/ref/class-based-views/generic-display/#detailview

.. |SingleObjectMixin| replace:: ``SingleObjectMixin``
.. _SingleObjectMixin: https://docs.djangoproject.com/en/1.11/ref/class-based-views/mixins-single-object/#singleobjectmixin

The app stores the visited resources into the browser `session <https://docs.djangoproject.com/en/1.11/topics/http/sessions/>`_, whose session ID is stored in a cookie in the user's web browser. The app does not employ more sophisticated user tracking such as IP detection and storage.

Template tags
=============

The bulk of the app's logic is in the mixin, but `template tags <https://docs.djangoproject.com/en/1.11/howto/custom-template-tags/>`_ allow for display of the list of resources consumed, the limit, and the days of expiration.

Load the template tags.

.. code-block:: django

   {% load regwall_tags %}

Assign any of the tags' output to a variable with the ``as`` syntax.

.. code-block:: django

   {% load regwall_tags %}

   {% get_regwall_limit as regwall_limit %}
   {% get_regwall_expire as regwall_expire %}
   {% get_regwall_attempts as regwall_attempts %}
   {% get_regwall_successes as regwall_successes %}

Use the assigned variables as you like.

``{% get_regwall_limit %}``
---------------------------

Gets the number of resources a user can consume before the registration wall is raised.

.. code-block:: django

   {% load regwall_tags %}

   {% get_regwall_limit as regwall_limit %}

   <p>The limit is {{ regwall_limit }} articles.</p>

``{% get_regwall_expire %}``
----------------------------

Gets the number of days until the consumed resources count is reset to zero.

.. code-block:: django

   {% load regwall_tags %}

   {% get_regwall_limit as regwall_limit %}
   {% get_regwall_expire as regwall_expire %}

   <p>The limit is {{ regwall_limit }} articles for {{ regwall_expire }} days.</p>

``{% get_regwall_attempts %}``
------------------------------

Gets a list of the attempted consumed resources. The mixin logs each attempt a user makes for a request, which is not necessarily the same as a successful request. Each item of the list is a dictionary, which contains the ``app_label``, ``id``, ``headline``, and ``url`` of a single resource. You will probably use the ``length`` filter on ``get_regwall_attempts`` to get the number of attempted consumed resources.

.. code-block:: django

   {% get_regwall_attempts as regwall_attempts %}

   <p>You tried to read {{ regwall_attempts|length }} free articles.</p>

Use ``get_regwall_attempts`` to check against the result of ``get_regwall_limit``.

.. code-block:: django

   {% get_regwall_limit as regwall_limit %}
   {% get_regwall_expire as regwall_expire %}
   {% get_regwall_attempts as regwall_attempts %}

   {% if regwall_attempts|length >= regwall_limit %}
   <p>You read all of your {{ regwall_limit }} articles for {{ regwall_expire }} days.</p>
   {% endif %}

``{% get_regwall_successes %}``
-------------------------------

Similar to ``get_regwall_attempts``, but ``get_regwall_successes`` gets a list of the resources that were successful delivered to the user.

.. code-block:: django

   {% load regwall_tags %}

   {% get_regwall_limit as regwall_limit %}
   {% get_regwall_expire as regwall_expire %}
   {% get_regwall_attempts as regwall_attempts %}
   {% get_regwall_successes as regwall_successes %}

   {% if regwall_attempts|length >= regwall_limit %}
   <p>You read all {{ regwall_successes|length }} of your {{ regwall_limit }} articles for {{ regwall_expire }} days.</p>
   <ol>
       {% for article in regwall_successes %}
       <li><a href="{{ article.url }}">{{ article.headline }}</a></li>
       {% endfor %}
   </ol>
   {% endif %}

Note that because different models can use different conventions for what constitutes a "headline," the template tag checks against these model attributes in this order: ``headline``, ``title``, ``name``, and finally empty string.

Includes
========

To ease the creation of probable messages displayed to users, use (or be inspired by) the app's template `includes <https://docs.djangoproject.com/en/1.11/ref/templates/builtins/#include>`_ in the ``regwall`` directory.

``regwall/detail.html``
-----------------------

Usage in a template, intended for a "detail" template whose view probably uses a ``DetailView`` of your own creation:

.. code-block:: django

   {% include 'regwall/detail.html' %}

The result:

.. code-block:: django

   {% load regwall_tags %}

   {% get_regwall_attempts as regwall_attempts %}
   {% get_regwall_successes as regwall_successes %}
   {% get_regwall_limit as regwall_limit %}
   {% get_regwall_expire as regwall_expire %}

   {% if regwall_successes|length > 0 %}
   <p>You read {{ regwall_successes|length }} of your {{ regwall_limit }} free article{{ regwall_limit|pluralize }} for {{ regwall_expire }} day{{ regwall_expire|pluralize }}. <a href="{% url 'login' %}">Log in or register to read unlimited articles</a>.</p>
   {% endif %}

``regwall/login.html``
----------------------

Usage in a template, intended for ``registration/login.html``:

.. code-block:: django

   {% include 'regwall/login.html' %}

The result:

.. code-block:: django

   {% load regwall_tags %}

   {% get_regwall_attempts as regwall_attempts %}
   {% get_regwall_successes as regwall_successes %}
   {% get_regwall_limit as regwall_limit %}
   {% get_regwall_expire as regwall_expire %}

   {% if regwall_attempts|length >= regwall_limit %}
   <p>You read {{ regwall_successes|length }} of your {{ regwall_limit }} free article{{ regwall_limit|pluralize }} for {{ regwall_expire }} day{{ regwall_expire|pluralize }}. Log in or register to read unlimited articles.</p>
   {% endif %}

``regwall/history.html``
------------------------

Usage in a template, intended for ``registration/login.html``:

.. code-block:: django

   {% include 'regwall/history.html' %}

The result:

.. code-block:: django

   {% load i18n regwall_tags %}

   {% get_regwall_attempts as regwall_attempts %}
   {% get_regwall_successes as regwall_successes %}
   {% get_regwall_limit as regwall_limit %}

   {% if regwall_attempts|length >= regwall_limit %}
   <h2>{% trans 'You read these articles' %}</h2>
   <ol>
       {% for article in regwall_successes %}
       <li><a href="{{ article.url }}">{{ article.headline }}</a></li>
       {% endfor %}
   </ol>
   {% endif %}

Demo
====

The repo contains a sample Django project that shows how a typical intergration might occur with the template tags and includes. A fixture with sample data is also included to quickly test.

.. code-block:: django

   $ mkvirtualenv -p python3 demo
   (demo)$ git clone git@github.com:richardcornish/django-registrationwall.git
   (demo)$ cd django-registrationwall/demo/
   (demo)$ pip install -r requirements.txt
   (demo)$ cd demo/
   (demo)$ python manage.py migrate
   (demo)$ python manage.py loaddata articles_article.json
   (demo)$ python manage.py runserver

Open `http://127.0.0.1:8000/articles/ <http://127.0.0.1:8000/articles/>`_.
