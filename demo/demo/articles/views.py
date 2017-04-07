from django.views.generic import DetailView, ListView

from regwall.mixins import RaiseRegWallMixin

from .models import Article


class ArticleDetailView(RaiseRegWallMixin, DetailView):
    model = Article


class ArticleListView(ListView):
    model = Article
