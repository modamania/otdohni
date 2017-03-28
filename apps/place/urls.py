from django.conf.urls.defaults import *

from views import *

urlpatterns = patterns('',
    url(r'^$', main_page, name='place_list'),
    url(r'^place/search/$', search_by_name),
    url(r'^(\d+)/$', place_show, name='place_show'),
    url(r'^tag/([-\w]+)/$', show_places_by_tag, name='show_places_by_tag'),
    url(r'^([-\w]+)/$', show_category, name='place_show_category'),
)


