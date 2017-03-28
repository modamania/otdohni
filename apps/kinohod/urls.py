from django.conf.urls.defaults import *

urlpatterns = patterns('kinohod.views',
    url('^schedules/$', 'schedules', name='kinohod_schedules'),
)
