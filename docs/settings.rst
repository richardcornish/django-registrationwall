.. _settings:

Settings
********

The mixin tag offers three settings. By default, they are:

.. code-block:: python

   REGWALL_LIMIT = 10

   REGWALL_EXPIRE = 30

   REGWALL_SOCIAL = [
       'google.com',
       'facebook.com',
       'twitter.com',
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

A list of strings of hosts of whose referral does not increment the consumed resources count. In other words, visitors coming from these domains are not penalized. Alternate ``www`` versions of the domains are automatically added to the list.

The mixin allows referrals from Google, Facebook, and Twitter by default.
