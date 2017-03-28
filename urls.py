# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template
from django.views.generic.simple import redirect_to

from common.forms import FeedbackForm

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',

    (r'^api/kinohod/', include('kinohod.urls')),
    (r'^api/', include('api.urls')),

    (r'^admin/filebrowser/', include('filebrowser.urls')),
    (r'^admin_tools/', include('admin_tools.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^tinymce/', include('tinymce.urls')),
    (r'^loginza/', include('loginza.urls')),
    (r'^validate/', include('ajax_validation.urls')),
    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^elfinder/', include('elfinder.urls')),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^django-rq/', include('django_rq.urls')),

    #redirect
    ('^places/all/$', redirect_to, {'url': '/places/'}),
    ('^afisha/clubs/$', redirect_to, {'url': '/afisha/klubyi/'}),
    ('^afisha/movie/$', redirect_to, {'url': '/afisha/kino/'}),
    ('^afisha/vistavki/$', redirect_to, {'url': '/afisha/vyistavki/'}),
    ('^afisha/koncerti/$', redirect_to, {'url': '/afisha/kontsertyi/'}),
    ('^tea-with-a-star.html/$', redirect_to, {'url': '/tea-with-a-star/'}),
    #end redirect

    url(r'^$', 'core.views.index', name='main'),
    url(r'^robots.txt$', 'robots.views.robots'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^addnew/$', 'common.views.addnew', name='addnew'),
    url(r'^addnew_success/$', 'common.views.addnew_success', name='addnew_success'),
    url(r'^feedback/$', 'common.views.feedback', name='feedback'),
    (r'^registration/', include('registration.urls')),
    (r'^users/', include('profile.urls')),
    (r'^control/', include('control.urls')),
    (r'^friendship/', include('friendship.urls')),
    (r'^messages/', include('private_messages2.urls')),
    (r'^places/', include('place.urls')),
    (r'comments/post/$', 'threadedcomments.views.post_comment'),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^news/', include('news.urls')),
    (r'^blog/', include('blog.urls')),
    (r'^sales/', include('sales.urls')),
    (r'^business-lunch/', include('lunch.urls')),
    (r'^tea-with-a-star/', include('tea.urls')),
    (r'^rating/', include('rating.urls')),
    (r'^photo/', include('photoreport.urls')),
    (r'^actions/', include('action.urls')),
    (r'^afisha/', include('event.urls')),
    (r'^gourmet/', include('gourmet.urls')),
    (r'^fashion/', include('fashion.urls')),
    (r'^newsletter/', include('newsletter.urls')),
    (r'^contacts/', include('contacts.urls')),
    (r'^specprojects/', include('specprojects.urls')),

    (r'^dostavka_edy/$', 'place.views.show_category',
                        {'slug': 'dostavka_edy'}),

    (r'^holiday/$', 'place.views.show_category',
                        {'slug': 'holiday'}),

    (r'^hobbi/$', 'place.views.show_category',
                        {'slug': 'hobbi'}),

    (r'^avto/$', 'place.views.show_category',
                        {'slug': 'avto'}),

    (r'^taxi/$', 'place.views.show_category',
                        {'slug': 'taxi'}),

    (r'^taggit_autocomplete/', include('taggit_autocomplete.urls')),
    (r'^desired-path-to-chosen/', include('chosen.urls')),

    #flatpage
    (r'^sales2/$', direct_to_template, \
        {'template': 'sales.html'}),

    #flatpage
    (r'^tea-with-a-star/$', direct_to_template, \
        {'template': 'tea-with-a-star.html'}),

    #flatpage
    (r'^places/placeinf/$', direct_to_template, \
        {'template': 'placeinf.html'}),

    #flatpage
    url(r'^about/$', 'common.views.feedback', name='about'),


    #static content

    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT,'show_indexes': True}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,'show_indexes': True}),

        (r'^control/event/$', direct_to_template, \
     {'template': 'control/event_form.html'}),

    #redirects for pages

    ('^news/latest/rebrending-otdohniomsk.ru.html/$', redirect_to, {'url': '/news/rebrending-otdohniomskru/'}),
    ('^foto/$', redirect_to, {'url': '/photo/'}),
    ('^services/taxi/$', redirect_to, {'url': '/taxi/'}),
    ('^bileti_online/$', redirect_to, {'url': '/afisha/kino/'}),
)

