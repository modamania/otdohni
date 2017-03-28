from django.conf.urls.defaults import *

from event.views import EventOnDay


urlpatterns = patterns('event.views',
    url(r'^week/$', 'event_on_week', name='event_all_on_week'),
    url(r'^soon/$', 'event_soon', name='event_all_soon'),

    url(r'^all/$', 'event_list', name='event_list'),
    url(r'^all/week/', 'event_on_week', name='event_tab_on_week'),
    url(r'^all/soon/$', 'event_soon', name='event_tab_soon'),

    url(r'^(?P<category_slug>[-\w]+)/week/$', 'event_on_week', name='event_on_week'),
    url(r'^(?P<category_slug>[-\w]+)/soon/$', 'event_soon', name='event_soon'),
    url(r'^(?P<category_slug>[-\w]+)/$', 'event_category_list', name='event_category_list'),

    url(r'^navigation/?(?P<year>\d{4})?/?(?P<month>\d{1,2})?/$', 'calendar_navigation', name='calendar_navigation'),
    url(r'^visit/event(?P<event_id>\d+)/$', 'event_visit', name='event_visit'),
    url(r'^(?P<category_slug>[-\w]+)/event(?P<event_id>\d+)/$', 'event_detail', name='event_detail'),
    url(r'^(?P<category_slug>[-\w]+)/event(?P<event_id>\d+)/subscribe/$', 'event_comment_subscribe', name='event_comment_subscribe'),
    url(r'^(?P<category_slug>[-\w]+)/event(?P<event_id>\d+)/unsubscribe/$', 'event_comment_unsubscribe', name='event_comment_unsubscribe'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', EventOnDay.as_view(), name='event_on_day'),
    url(r'^(?P<category_slug>[-\w]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', EventOnDay.as_view(), name='event_all_on_day'),
)

urlpatterns += patterns('django.views.generic.simple',
    url(r'^all/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/soon/$', 'redirect_to', {'url': '/afisha/all/soon/'}),
    url(r'^all/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/week/$', 'redirect_to', {'url': '/afisha/all/week/'}),
    url(r'^koncerti/$', 'redirect_to', {'url': '/afisha/kontsertyi/'}),
    url(r'^clubs/$', 'redirect_to', {'url': '/afisha/klubyi/'}),
    url(r'^movie/$', 'redirect_to', {'url': '/afisha/kino/'}),
    url('^vistavki/$', 'redirect_to', {'url': '/afisha/vyistavki/'}),
)
