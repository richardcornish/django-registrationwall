from django.views.generic import DetailView

from regwall.mixins import RaiseRegWallMixin

from .models import Article


class ArticleDetailView(RaiseRegWallMixin, DetailView):
    model = Article
