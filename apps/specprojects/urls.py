from django.conf.urls.defaults import *

urlpatterns = patterns('specprojects.views',
    url(r'^$', 'spec_list', name='spec_list'),
    url(r'^(?P<spec_slug>[-\w]+)/$', 'spec_detail',
        name='spec_detail'),
)
