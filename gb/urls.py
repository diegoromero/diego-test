from django.conf.urls import patterns, url
from gb import views

urlpatterns = patterns('',
    url(r'^$', views.home),
)
