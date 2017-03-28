from django.conf.urls.defaults import patterns, url
from news.feeds import NewsFeed, NewsByTagFeed

urlpatterns = patterns('news.views',
    #Feeds
    url('^rss/$', NewsFeed(), name='news_feed'),
    url('^rss/(?P<tag_slug>[-\w]+)/$', NewsByTagFeed(), name='news_tag_feed'),

    url('^$', 'news_list', name='news_list'),
    url('^(?P<slug>[-\w]+)/$', 'news_detail', name='news_detail'),
    url('^(?P<slug>[-\w]+)/subscribe/$', 'news_comment_subscribe', name='news_comment_subscribe'),
    url('^(?P<slug>[-\w]+)/unsubscribe/$', 'news_comment_unsubscribe', name='news_comment_unsubscribe'),
    url('^tag/(?P<tag_slug>[-\w]+)/$', 'news_list', name='news_tag_list'),
)
