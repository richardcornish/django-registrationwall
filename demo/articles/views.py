from django.views.generic import ListView, DetailView

from paywall.mixins import RaisePaywallMixin

from .models import Article


class ArticleListView(ListView):
    model = Article


class ArticleDetailView(RaisePaywallMixin, DetailView):
    model = Article
