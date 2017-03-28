from django.conf.urls.defaults import patterns, url
from fashion.feeds import FashionFeed, FashionByTagFeed

urlpatterns = patterns('fashion.views',
    url('^$', 'fashion_list', name='fashion_list'),
    url('^(?P<slug>[-\w]+)/$', 'fashion_detail', name='fashion_detail'),
    url('^tag/(?P<tag_slug>[-\w]+)/$', 'fashion_list', name='fashion_tag_list'),
)

#Feeds
urlpatterns+= patterns('',
    url('^rss/$', FashionFeed(), name='fashion_feed'),
    url('^rss/(?P<tag_slug>[-\w]+)/$', FashionByTagFeed(), name='fashion_tag_feed'),
)
