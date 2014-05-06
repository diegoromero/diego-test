from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static
from gb import views

from django_sse.redisqueue import RedisQueueView

from sse_wrapper.views import EventStreamView
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^home/$', views.home),
    url(r'^home1/$', views.Home1.as_view(), name='home1'),
    url(r'^home2/$', views.Home2.as_view(), name='home2'),
    url(r'^home3/$', views.Home3),                   

    url(r'^events1/$', views.MySseEvents.as_view(), name='events1'),
    url(r'^events2/$', RedisQueueView.as_view(), name='events2'),
    url(r'^events3/$', views.Screen.as_view(), name='events3'),

    # index page.
    url(r'^$', TemplateView.as_view(
        template_name='index.html'), name='index'),

    # sample views that sends events in the channel course-state.
    url(r'^start-course/(?P<course_id>\d+)/$',
        'gb.views.start_course', name='start_course'),
    url(r'^stop-course/(?P<course_id>\d+)/$',
        'gb.views.stop_course', name='stop_course'),
    url(r'^course-state/(?P<course_id>\d+)/$',
        'gb.views.course_state', name='course_state'),

    # event stream - course-state.
    url(r'^course-state-stream/(?P<channel_extension>[\w]+)/$',
        EventStreamView.as_view(channel='course-state'),
        name='course_state_stream'),
)
