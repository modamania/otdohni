from django.conf.urls.defaults import *
from models import *


urlpatterns = patterns('action.views',
    url(r'^$', 'action_list', name='action_list'),
    url(r'^complete/$', 'action_list', {'status':'complete'}, name='complete_action_list'),
    url(r'^winners/$', 'winners_list', name='action_winners_list'),
    url(r'^polls/$', 'poll_list', name='poll_list'),
    url(r'^polls/(?P<poll_id>\d+)/$', 'poll_detail',
                                name='poll_detail'),
    url(r'^(?P<action_slug>[-\w]+)/$', 'action_detail',
                                name='action_detail'),
    url(r'^(?P<poll_id>\d+)/work/(?P<work_id>\d+)/$', 'liked_work',
                                name='liked_work')
)
