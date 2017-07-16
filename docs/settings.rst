.. _settings:

Settings
********

The mixin tag offers three settings. By default, they are:

.. code-block:: python

   REGWALL_LIMIT = 10

   REGWALL_EXPIRE = 30

   REGWALL_SOCIAL = [
       'google',
       'facebook',
       'twitter',
   ]

``REGWALL_LIMIT``
=================

An integer indicating the number of resources to display before the registration wall appears.

The mixin displays ``10`` resources by default.

``REGWALL_EXPIRE``
==================

An integer indicating the number of days before the consumed resources count is reset to zero.

The mixin resets after ``30`` days by default.

``REGWALL_SOCIAL``
==================

A list of strings of domains whose referral does not increment the consumed resources count. In other words, visitors coming from these domains are not penalized. Previously, the app used a rudimentary method of domain checking with the |urlparse|_/|urllib_parse|_ modules. Because URLs vary so widely in construction, the app now uses the `tldextract <https://pypi.python.org/pypi/tldextract>`_ package to accurately extract the domain. Therefore, this setting should contain only `domains <https://en.wikipedia.org/wiki/Domain_name>`_ and not `top-level domains <https://en.wikipedia.org/wiki/Top-level_domain>`_, e.g. ``['google', 'facebook', 'twitter']`` and *not* ``['google.com', 'facebook.com', 'twitter.com']``.

The mixin allows referrals from Google, Facebook, and Twitter by default.

.. |urlparse| replace:: ``urlparse``
.. _urlparse: https://docs.python.org/2/library/urlparse.html

.. |urllib_parse| replace:: ``urllib.parse``
.. _urllib_parse: https://docs.python.org/3/library/urllib.parse.html