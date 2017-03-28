from django.conf.urls.defaults import *
from models import PhotoReport, Photo, PhotoReportUpload


urlpatterns = patterns('photoreport.views',
	url(r'^$', 'photoreport_list', name='photoreport_list'),
    url(r'^(?P<report_slug>[-\w]+)/$', 'photoreport_detail',
                                name='photoreport_detail'),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', 'photoreport_list',
                                name='photoreport_tag_list'),
	url(r'^(?P<report_slug>[-\w]+)/(?P<photo_id>[-\w]+)/$', 'photo_detail',
                                name='photo_detail'),
    url(r'^(?P<report_slug>[-\w]+)/(?P<photo_id>[-\w]+)/subscribe/$', 'photo_subscribe',
                                name='photo_subscribe'),
    url(r'^(?P<report_slug>[-\w]+)/(?P<photo_id>[-\w]+)/unsubscribe/$', 'photo_unsubscribe',
                                name='photo_unsubscribe'),
    url(r'^(?P<report_slug>[-\w]+)/(?P<photo_id>[-\w]+)/download/$', 'photo_dwnl',
        name='photo_download'),
)

