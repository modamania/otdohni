from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

# General
urlpatterns = patterns('elfinder.views',
    url(r'^$', "elfinder", name="elfinder_index"),
    url(r'connector',"connector",name="elfinder_connector"),
)
