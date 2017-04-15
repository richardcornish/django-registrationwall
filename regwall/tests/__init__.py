from __future__ import unicode_literals

import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.utils import timezone

from .articles.models import Article


class RegWallTestCase(TestCase):
    """Registration Wall test cases."""

    fixtures = ['articles_article.json']

    def setUp(self):
        self.client = Client()

    def test_regwall(self):
        for article in Article.objects.all()[:10]:
            response = self.client.get(reverse('article_detail', args=[article.slug]))
        self.assertEqual(response.request['PATH_INFO'], '/articles/2/')

    def test_regwall_raise(self):
        for article in Article.objects.all():
            response = self.client.get(reverse('article_detail', args=[article.slug]))
        self.assertRedirects(response, '/accounts/login/?next=/articles/1/')
