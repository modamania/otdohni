#coding: utf-8
from django.forms import Media
from django.conf.urls.defaults import *
from django.utils.translation import ugettext_lazy as _

from django.contrib import admin

from omskadmin.admin import SiteOnlyAdmin
from core.utils import ImgPreview
from models import *


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 2


class PhotoReportAdmin(SiteOnlyAdmin, admin.ModelAdmin):
    fieldsets = (
        (_('Content'), {
            'fields': ('title', 'date_event', 'event', 'place', 'slug', 'description',),
        }),
        (_('Options'), {
            'fields': ('is_published', 'on_mainpage'),
            'classes': ('collapse', 'collapse-closed')
        }),
        (_('Publication'), {
            'fields': ('sites', 'tags', 'pub_date')
        }),
    )

    list_display = (
        'title',
        'on_mainpage', 'is_published',
        'date_event', 'num_photos',
        'get_sites', 'pub_date',
    )
    list_editable = (
        'is_published', 'on_mainpage',
    )
    filter_horizontal = (
        'sites', 'tags',
    )
    list_filter = [
        'is_published', 'on_mainpage'
    ]
    search_fields = [
        'title', 'description',
    ]
    prepopulated_fields = {
        'slug': ('title',)
    }
    date_hierarchy = 'date_event'
    change_form_template = 'photoreport/admin/add_photoreport.html'

    icon = ImgPreview(lambda x: x.get_preview(), (200, 75))

    def get_urls(self):
        photoreport_admin_urls = super(PhotoReportAdmin, self).get_urls()
        urls = patterns('django.views.generic.simple',
                        url(r'^autocomplete_tags/$', 'direct_to_template',
                            {'template': 'photoreport/admin/autocomplete_tags.js',
                             'mimetype': 'application/javascript'},
                            name='photoreport_autocomplete_tags'),)
        return urls + photoreport_admin_urls

    def _media(self):
        MEDIA_URL = settings.MEDIA_URL
        media = super(PhotoReportAdmin, self).media + \
                Media(css={'all': ('%scss/jquery.autocomplete.css' % MEDIA_URL,),},
                      js=('%sjs/jquery.js' % MEDIA_URL,
                          '%sjs/jquery.bgiframe.js' % MEDIA_URL,
                          '%sjs/jquery.autocomplete.js' % MEDIA_URL,
                          reverse('admin:photoreport_autocomplete_tags'),))

        return media
    media = property(_media)

    #actions = [make_published, make_unpublished]


class PhotoAdmin(admin.ModelAdmin):
    list_filter = (
        'photoreport',
        'date_added',
    )
    list_display = (
        '__unicode__',
        'icon',
        'photoreport',
    )
    list_display_links = (
        '__unicode__',
    )
    search_fields = (
        'title',
        'caption',
    )
    prepopulated_fields = {
        'slug': ('title',)
    }
    list_per_page = 50
    icon = ImgPreview(lambda x: x.get_image, (200, 75))


admin.site.register(PhotoReport, PhotoReportAdmin)
admin.site.register(PhotoReportUpload)
admin.site.register(Photo, PhotoAdmin)
