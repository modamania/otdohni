from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import redirect_to

from views import Inbox, View, Delete, Compose, Undelete, Unread, Read


urlpatterns = patterns('',
    url(r'^$', redirect_to, {'url': 'inbox/'}),
    url(r'^inbox/$', Inbox.as_view(), name='messages_inbox'),
    url(r'^view/(?P<pk>[\d]+)/$', View.as_view(), name='messages_view'),
    url(r'^delete_list/$', Delete.as_view(), name='messages_delete_list'),
    url(r'^delete/(?P<pk>[\d]+)/$', Delete.as_view(), name='messages_delete'),
    url(r'^compose/$', Compose.as_view(), name='messages_compose'),
    url(r'^compose/(?P<to>[\d]+)/$', Compose.as_view(), name='messages_compose_to'),
    url(r'^undelete/$', Undelete.as_view(), name='messages_undelete'),
    url(r'^mark_as_unread/$', Unread.as_view(), name='messages_unread'),
    url(r'^mark_as_read/$', Read.as_view(), name='messages_read'),
)
