from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('blog.views',
    url('^$', 'index', name='blog_index'),
    url('^(?P<slug>[-\w]+)/$', 'post_detail', name='post_detail'),
    url('^(?P<slug>[-\w]+)/subscribe/$', 'post_comment_subscribe', name='post_comment_subscribe'),
    url('^(?P<slug>[-\w]+)/unsubscribe/$', 'post_comment_unsubscribe', name='post_comment_unsubscribe'),
    url('^tag/(?P<tag_slug>[-\w]+)/$', 'index', name='post_tag_list'),
)
