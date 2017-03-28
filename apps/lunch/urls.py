from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('lunch.views',
    url('^$', 'lunch_list', name='lunch_list'),
)