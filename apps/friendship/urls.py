from django.conf.urls.defaults import *

from views import *


urlpatterns = patterns('',
    url(r'^add/(\d+)/$', add_friendship, name='add_friendship'),
    url(r'^remove/(\d+)/$', remove_friendship, name='remove_friendship'),
)
