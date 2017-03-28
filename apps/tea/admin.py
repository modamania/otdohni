#coding: utf-8

from django.contrib import admin
from common.actions import make_published, make_unpublished
from core.utils import ImgPreview
from django.utils.translation import ugettext_lazy as _
from tea.models import Interview

from omskadmin.admin import SiteOnlyAdmin

class InterviewAdmin(SiteOnlyAdmin, admin.ModelAdmin):
    list_display = ['title', 'preview',  'is_published', 'pub_date']
    list_editable = ('is_published', )
    list_filter = [ 'is_published',]
    date_hierarchy = 'pub_date'
    search_fields = ['title',]

    preview = ImgPreview(lambda x: x.image, (200, 75), _('photo'))

    actions = [make_published, make_unpublished]

admin.site.register(Interview, InterviewAdmin)

