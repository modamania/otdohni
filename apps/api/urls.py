from django.conf.urls.defaults import *


urlpatterns = patterns('',
    (r'^places/search/$', 'api.place.views.search_by_name'),
    (r'^search/$', 'api.place.views.search_all'),
    (r'^places/([-\w]+)/$', 'api.place.views.count_place_in_category'),

    (r'^json/places/(?P<slug>[-\w]+)/$', 'api.place.views.place_list_by_url'),
    (r'^json/places/tag/(?P<tag>[-\w]+)/$', 'api.place.views.place_list_by_url'),
    (r'^json/dostavka_edy/$', 'api.place.views.place_list_by_url',
                        {'slug': 'dostavka_edy'}),

    (r'^json/holiday/$', 'api.place.views.place_list_by_url',
                        {'slug': 'holiday'}),

    (r'^json/hobbi/$', 'api.place.views.place_list_by_url',
                        {'slug': 'hobbi'}),

    (r'^json/avto/$', 'api.place.views.place_list_by_url',
                        {'slug': 'avto'}),

    (r'^json/taxi/$', 'api.place.views.place_list_by_url',
                        {'slug': 'taxi'}),
    
    (r'^([-_\w]+)/$', 'api.place.views.count_place_in_category'),
    (r'^comment/relate/(\w+)/(\d+)/$', 'api.comment.views.relate_comment'),
    url(r'^comment/remove/(\d+)/$', 'api.comment.views.remove_comment', name='api_comment_remove'),
)

# VIEWS API
urlpatterns += patterns('api.views',
    url(r'^event/on_day/$', 'event_on_day', name='api_event_on_day'),
)

# PLACES API
urlpatterns += patterns('api.views',
    url(r'^place/for_event/$', 'place_for_event', name='api_place_for_event'),
)
