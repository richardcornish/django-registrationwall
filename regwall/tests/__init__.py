from __future__ import unicode_literals

import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.utils import timezone

from .articles.models import Article


class RegWallTestCase(TestCase):
    """Registration Wall test cases."""

    def setUp(self):
        self.client = Client()

        # article 1
        Article.objects.create(
            headline='Guy wearing thumb drive around neck wonders if you tried hard reboot',
            slug='1',
            body='Lorem ipsum dolor sit amet.',
            pub_date=timezone.make_aware(datetime.datetime.strptime('2015-12-22T05:04:33', '%Y-%m-%dT%H:%M:%S')),
        )

        # article 2
        Article.objects.create(
            headline='Study finds majority of accidental heroin overdoses could be prevented with less heroin',
            slug='2',
            body='Lorem ipsum dolor sit amet.',
            pub_date=timezone.make_aware(datetime.datetime.strptime('2015-12-22T05:04:49', '%Y-%m-%dT%H:%M:%S')),
        )

        # article 3
        Article.objects.create(
            headline='EPA urges nation to develop new air source',
            slug='3',
            body='Lorem ipsum dolor sit amet.',
            pub_date=timezone.make_aware(datetime.datetime.strptime('2015-12-22T05:04:59', '%Y-%m-%dT%H:%M:%S')),
        )

        # article 4
        Article.objects.create(
            headline='Astronomers discover previously unknown cluster of nothingness in deep space',
            slug='4',
            body='Lorem ipsum dolor sit amet.',
            pub_date=timezone.make_aware(datetime.datetime.strptime('2015-12-22T05:06:05', '%Y-%m-%dT%H:%M:%S')),
        )

        # article 5
        Article.objects.create(
            headline="Elderly woman relieved to know she's tackled last technological advancement of lifetime",
            slug='5',
            body='Lorem ipsum dolor sit amet.',
            pub_date=timezone.make_aware(datetime.datetime.strptime('2015-12-22T05:06:11', '%Y-%m-%dT%H:%M:%S')),
        )

        # article 6
        Article.objects.create(
            headline="'Seek funding' step added to scientific method",
            slug='6',
            body='Lorem ipsum dolor sit amet.',
            pub_date=timezone.make_aware(datetime.datetime.strptime('2015-12-22T05:06:21', '%Y-%m-%dT%H:%M:%S')),
        )

        # article 7
        Article.objects.create(
            headline='Nation figured everything would run on some kind of cubes of blue energy by now',
            slug='7',
            body='Lorem ipsum dolor sit amet.',
            pub_date=timezone.make_aware(datetime.datetime.strptime('2015-12-22T05:06:31', '%Y-%m-%dT%H:%M:%S')),
        )

        # article 8
        Article.objects.create(
            headline="New study finds box still world's most popular container",
            slug='8',
            body='Lorem ipsum dolor sit amet.',
            pub_date=timezone.make_aware(datetime.datetime.strptime('2015-12-22T05:06:40', '%Y-%m-%dT%H:%M:%S')),
        )

        # article 9
        Article.objects.create(
            headline='Archaeologists discover ancient femur that could make mouthwatering broth',
            slug='9',
            body='Lorem ipsum dolor sit amet.',
            pub_date=timezone.make_aware(datetime.datetime.strptime('2015-12-22T05:06:50', '%Y-%m-%dT%H:%M:%S')),
        )

        # article 10
        Article.objects.create(
            headline='Groundbreaking study finds gratification can be deliberately postponed',
            slug='10',
            body='Lorem ipsum dolor sit amet.',
            pub_date=timezone.make_aware(datetime.datetime.strptime('2015-12-22T05:07:00', '%Y-%m-%dT%H:%M:%S')),
        )

        # article 11
        Article.objects.create(
            headline='Jeff Bezos assures Amazon employees that HR working 100 hours a week to address their complaints',
            slug='11',
            body='Lorem ipsum dolor sit amet.',
            pub_date=timezone.make_aware(datetime.datetime.strptime('2015-12-22T05:07:09', '%Y-%m-%dT%H:%M:%S')),
        )

    def test_regwall(self):
        for article in Article.objects.all()[:10]:
            response = self.client.get(reverse('article_detail', args=[article.slug]))
        self.assertEqual(response.request['PATH_INFO'], '/articles/2/')

    def test_regwall_raise(self):
        for article in Article.objects.all():
            response = self.client.get(reverse('article_detail', args=[article.slug]))
        self.assertRedirects(response, '/accounts/login/?next=/articles/1/')
