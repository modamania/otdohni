from django.conf.urls.defaults import patterns, url
from gourmet.feeds import GourmetFeed, GourmetByTagFeed

urlpatterns = patterns('gourmet.views',
    url('^$', 'gourmet_list', name='gourmet_list'),
    url('^(?P<slug>[-\w]+)/$', 'gourmet_detail', name='gourmet_detail'),
    url('^tag/(?P<tag_slug>[-\w]+)/$', 'gourmet_list', name='gourmet_tag_list'),
)

#Feeds
urlpatterns+= patterns('',
    url('^rss/$', GourmetFeed(), name='gourmet_feed'),
    url('^rss/(?P<tag_slug>[-\w]+)/$', GourmetByTagFeed(), name='gourmet_tag_feed'),
)

