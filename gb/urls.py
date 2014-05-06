from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static
from gb import views

urlpatterns = patterns('',
    url(r'^$', views.home),
)
