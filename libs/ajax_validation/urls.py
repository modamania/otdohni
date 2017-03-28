from django.conf.urls.defaults import *


#ajax validation register url
urlpatterns = patterns('ajax_validation.views',
    url(r'^(?P<form_name>[\w]+)/$', 'validate', name='form_validate'),
)
