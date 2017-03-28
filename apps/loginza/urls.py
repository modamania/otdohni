from django.conf.urls.defaults import *

urlpatterns = patterns('loginza.views',
    url(r'^return_callback/$', 'return_callback',
                            name='loginza_return'),
    url(r'^vote_callback/(?P<poll_id>\w+)/(?P<work_id>\w+)/$',
                            'return_vote_callback',
                            name='loginza_vote_return')
)
