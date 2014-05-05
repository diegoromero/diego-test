from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static
from gb import views

urlpatterns = patterns('',
    url(r'^home/$', views.home),
    url(r'^sse/$', views.SSE.as_view(), name='sse'),  # this URL is arbitrary.
    url(r'^$', views.HomePage.as_view(), name='homepage'),                   
)
