from django.conf.urls import patterns, url
from gb import views

urlpatterns = patterns('views',
    url(r'^$', home),
)
