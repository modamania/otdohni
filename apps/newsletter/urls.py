from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('newsletter.views',

    url(r'^filter/items/$', 'filter_items', name='filter_items'),
    url(r'^filter/events/$', 'filter_events', name='filter_events'),
    url(r'^subscribe/$', 'subscribe_request', name='newsletter_subscribe_request'),
    url(r'^subscribe/confirm/$', 'subscribe_request', kwargs={'confirm':True},
        name='newsletter_subscribe_confirm'),
    url(r'^unsubscribe/$', 'unsubscribe_request', name='newsletter_unsubscribe_request'),
    url(r'^unsubscribe/confirm/$', 'unsubscribe_request', kwargs={'confirm':True},
        name='newsletter_unsubscribe_confirm'),

    url(r'^subscription/(?P<email>[-_a-zA-Z0-9@\.\+~]+)/(?P<action>[a-z]+)/activate/(?P<activation_code>[a-zA-Z0-9]+)/$',
            'update_subscription', name='newsletter_update_activate'),
    url(r'^subscription/(?P<email>[-_a-zA-Z0-9@\.\+~]+)/(?P<action>[a-z]+)/activate/$',
            'update_subscription', name='newsletter_update'),

)

