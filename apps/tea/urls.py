from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('tea.views',
    url('^$', 'overview', name='overview_tea'),
    url('^(?P<interview_id>\d+)/$', 'interview_detail', name='interview_detail'),
    url('^all/$', 'interview_list', name='interview_list'),

)
