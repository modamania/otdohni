from django.conf.urls.defaults import *

core = patterns('apps.control.views.core',
    url(r'^$', 'dashboard', name='control_core_dashboard'),
    url(r'^(?P<model_name>\w+)/$', 'list'),
    url(r'^(?P<model_name>\w+)/add/$', 'form'),
    url(r'^(?P<model_name>\w+)/edit/(?P<pk>\d+)/$', 'form'),
    url(r'^(?P<model_name>\w+)/remove/(?P<pk>\d+)/$', 'remove'),
)

urlpatterns = patterns('apps.control.views',
    url(r'^$', 'dashboard', name='dashboard'),
    url(r'^user/list/$', 'user_list', name='control_user_list'),
    url(r'^user/edit/(\d+)/$', 'user_edit', name='control_user_edit'),
    (r'^core/', include(core)),
)

urlpatterns += patterns('apps.control.views',
    url(r'^place/list/$', 'place_list', name='control_place_list'),
    url(r'^place/show/(\d+)/$', 'place_show', name='control_place_show'),
    url(r'^place/new/$', 'place_form', name='control_edit_add'),
    url(r'^place/edit/(\d+)/$', 'place_form', name='control_place_edit'),
    url(r'^place/edit/address/(?P<place_pk>\d+)/$', 'address_form', name='control_address_form_new'),
    url(r'^place/edit/address/(?P<place_pk>\d+)/(?P<address_pk>\d+)/$', 'address_form', name='control_address_form_edit'),
    url(r'^place/edit/gallery/$', 'gallery_photo', name='control_gallery_photo'),
    url(r'^place/edit/image/$', 'change_image', name='control_change_image'),
)

urlpatterns += patterns('apps.control.views',
    url(r'^event/list/$', 'event_list', name='control_event_list'),
    url(r'^event/show/(\d+)/$', 'event_show', name='control_event_show'),
    url(r'^event/new/$', 'event_form', name='control_event_add'),
    url(r'^event/edit/(\d+)/$', 'event_form', name='control_event_edit'),
)

urlpatterns += patterns('apps.control.views',
    url(r'^specproject/list/$', 'spec_list', name='control_spec_list'),
    url(r'^specproject/show/(?P<spec_slug>[-\w]+)/$', 'spec_show', name='control_spec_show'),
    url(r'^specproject/new/$', 'spec_form', name='control_spec_add'),
    url(r'^specproject/edit/(?P<spec_slug>[-\w]+)/$', 'spec_form', name='control_spec_edit'),
)

urlpatterns += patterns('apps.control.views',
    url(r'^sale/list/$', 'sale_list', name='control_sale_list'),
    url(r'^sale/show/(?P<sale_pk>\d+)/$', 'sale_show', name='control_sale_show'),
    url(r'^sale/new/$', 'sale_form', name='control_sale_add'),
    url(r'^sale/edit/(?P<sale_pk>\d+)/$', 'sale_form', name='control_sale_edit'),
    url(r'^sale/delete/(?P<sale_pk>\d+)/$', 'sale_delete', name='control_sale_delete'),
)

urlpatterns += patterns('apps.control.views',
    url(r'^tea/list/$', 'tea_list', name='control_tea_list'),
    url(r'^tea/show/(?P<tea_pk>\d+)/$', 'tea_show', name='control_tea_show'),
    url(r'^tea/new/$', 'tea_form', name='control_tea_add'),
    url(r'^tea/edit/(?P<tea_pk>\d+)/$', 'tea_form', name='control_tea_edit'),
)

urlpatterns += patterns('apps.control.views',
    url(r'^news/list/$', 'news_list', name='control_news_list'),
    url(r'^news/show/(?P<news_pk>\d+)/$', 'news_show', name='control_news_show'),
    url(r'^news/new/$', 'news_form', name='control_news_add'),
    url(r'^news/edit/(?P<news_pk>\d+)/$', 'news_form', name='control_news_edit'),
)

urlpatterns += patterns('apps.control.views.blog',
    url(r'^blog/list/$', 'blog_list', name='control_blog_list'),
    url(r'^blog/show/(?P<post_pk>\d+)/$', 'blog_show', name='control_blog_show'),
    url(r'^blog/new/$', 'blog_form', name='control_blog_add'),
    url(r'^blog/edit/(?P<post_pk>\d+)/$', 'blog_form', name='control_blog_edit'),
)

urlpatterns += patterns('apps.control.views',
    url(r'^photoreport/list/$', 'photoreport_list', name='control_photoreport_list'),
    url(r'^photoreport/show/(?P<photoreport_pk>\d+)/$', 'photoreport_show', name='control_photoreport_show'),
    url(r'^photoreport/new/$', 'photoreport_form', name='control_photoreport_add'),
    url(r'^photoreport/edit/(?P<photoreport_pk>\d+)/$', 'photoreport_form', name='control_photoreport_edit'),
    url(r'^photoreport/(?P<photoreport_pk>\d+)/upload_photo/$', 'photoreport_upload', name='control_photoreport_upload'),
    url(r'^photoreport/(?P<photoreport_pk>\d+)/new_photo/$', 'photoreport_photo_form', name='control_photoreport_photo_add'),
    url(r'^photoreport/(?P<photoreport_pk>\d+)/edit_photo/(?P<photo_pk>\d+)/$', 'photoreport_photo_form', name='control_photoreport_photo_edit'),
)

urlpatterns += patterns('apps.control.views',
    url(r'^action/list/$', 'action_list', name='control_action_list'),
    url(r'^action/show/(?P<action_pk>\d+)/$', 'action_show', name='control_action_show'),
    url(r'^action/new/$', 'action_form', name='control_action_add'),
    url(r'^action/edit/(?P<action_pk>\d+)/$', 'action_form', name='control_action_edit'),
    url(r'^action/(?P<action_pk>\d+)/new_poll/$', 'action_poll_form', name='control_action_poll_add'),
    url(r'^action/(?P<action_pk>\d+)/edit_poll/(?P<poll_pk>\d+)/$', 'action_poll_form', name='control_action_poll_edit'),
    url(r'^action/(?P<action_pk>\d+)/new_winner/$', 'action_winner_form', name='control_action_winner_add'),
    url(r'^action/(?P<action_pk>\d+)/edit_winner/(?P<winner_pk>\d+)/$', 'action_winner_form', name='control_action_winner_edit'),
    url(r'^action/(?P<action_pk>\d+)/poll/(?P<poll_pk>\d+)/new_work/$', 'workbidder_form', name='control_workbidder_add'),
    url(r'^action/(?P<action_pk>\d+)/poll/(?P<poll_pk>\d+)/edit_work/(?P<work_pk>\d+)/$', 'workbidder_form', name='control_workbidder_edit'),
)

urlpatterns += patterns('apps.control.views',
    url(r'^seo/$', 'seo_form', name='control_seo_edit'),
)

urlpatterns += patterns('apps.control.views',
    url(r'^graber/$', 'graber_dashboard', name='control_graber_dashboard'),
    url(r'^graber/clone/list/$', 'graber_clone_list', name='control_graber_clone_list'),
    url(r'^graber/clone/(\d+)/$', 'graber_clone_item', name='control_graber_clone_item'),
    url(r'^graber/update/list/$', 'graber_place_update_list', name='control_graber_place_update_list'),
    url(r'^graber/update/(\d+)/$', 'graber_place_update_form', name='control_graber_place_update_form'),
)
