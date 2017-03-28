from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('sales.views',
    url('^$', 'coupon_list', name='coupon_list'),
    url('^(?P<coupon_id>\d+)/$', 'coupon_detail', name='coupon_detail'),
)