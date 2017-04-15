from django.conf.urls import include, url


urlpatterns = [
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^articles/', include('regwall.tests.articles.urls')),
]
