from django.conf.urls.defaults import *
from registration.views import activate
from registration.views import register
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views as auth_views

from views import *


urlpatterns = patterns('',
    url(r'^(\d+)/$', profile_show, name='profile_show'),
    url(r'^list/$', user_list, name='user_list'),
    url(r'friends/$', user_list, {'only_friends': True}, name='friends_list'),
    (r'^change_my_profile/$', profile_edit),

    (r'^password/change/$', auth_views.password_change),
    (r'^password/change/done/$', auth_views.password_change_done),
    (r'^password/reset/$', auth_views.password_reset),
    (r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', \
       auth_views.password_reset_confirm),
    (r'^password/reset/complete/$', auth_views.password_reset_complete),
    (r'^password/reset/done/$', auth_views.password_reset_done),
)
