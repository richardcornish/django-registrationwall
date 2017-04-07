from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Article(models.Model):
    headline = models.CharField(_("Headline"), max_length=255)
    slug = models.SlugField(_("Slug"), max_length=255, unique=True)
    body = models.TextField(_("Body"), )
    pub_date = models.DateTimeField(_("Pub date"), default=timezone.now)

    class Meta:
        ordering = ["-pub_date"]
        verbose_name = _("article")
        verbose_name_plural = _("articles")

    def __str__(self):
        return self.headline

    def get_absolute_url(self):
        return reverse("article_detail", args=[str(self.slug)])
