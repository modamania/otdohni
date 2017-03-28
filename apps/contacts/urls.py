from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


#contacts urls
urlpatterns = patterns('contacts.views',
    url(r'^$', 'submit', name='submit_contacts'),
    url(r'^thanks/$', direct_to_template, {'template': 'contacts/thanks.html'}, name='contact_tnx'),
)

