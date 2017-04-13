from django.conf.urls import url, include


urlpatterns = [
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^articles/', include('regwall.tests.articles.urls')),
]
