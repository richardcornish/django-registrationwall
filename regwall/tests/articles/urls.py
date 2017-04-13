from django.conf.urls import url

from .views import ArticleDetailView


urlpatterns = [
    url(r'^(?P<slug>[-\w]+)/$', ArticleDetailView.as_view(), name='article_detail'),
]
