from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static
from gb import views

from django_sse.redisqueue import RedisQueueView

urlpatterns = patterns('',
    url(r'^home/$', views.home),
    url(r'^home1/$', views.Home1.as_view(), name='home1'),
    url(r'^home2/$', views.Home2.as_view(), name='home2'),
    url(r'^home3/$', views.Home3),                   

    url(r'^events1/$', views.MySseEvents.as_view(), name='events1'),
    url(r'^events2/$', RedisQueueView.as_view(), name='events2'),
)
