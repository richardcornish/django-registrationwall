from django.conf.urls import url

from .views import ArticleDetailView, ArticleListView


urlpatterns = [
    url(r'^(?P<slug>[-\w]+)/$', ArticleDetailView.as_view(), name='article_detail'),
    url(r'^$', ArticleListView.as_view(), name='article_list'),
]
