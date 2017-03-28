from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from core.utils import ImgPreview

from omskadmin.admin import SiteOnlyAdmin
from models import Action, Poll, WorkBidder


class ActionAdmin(SiteOnlyAdmin, admin.ModelAdmin):
    fieldsets = ((_('Content'), {'fields': ('title', 'slug', 'image',
                                'short_text', 'full_text')}),
                (_('Publication'), {'fields': ('pub_date','is_published',
                                'is_completed', 'sites')})
                )
    prepopulated_fields = {"slug": ("title",)}
    list_display = ['title', 'is_published', 'is_completed', 'get_sites']
    list_editable = ('is_published', 'is_completed')
    list_filter = [ 'is_published', 'sites__name']
    date_hierarchy = 'pub_date'
    search_fields = ['title', 'short_text', 'full_text']


class PollAdmin(admin.ModelAdmin):
    fieldsets = ((_('Content'), {'fields': ('action', 'title', 'can_vote', 'vote_frequency',
                                'start_date', 'end_date')}),
                (_('Publication'), {'fields': ('is_published', 'status')})
                )
    list_display = ['title', 'action', 'start_date', 'end_date', 'status', 'is_published']
    list_editable = ('is_published', 'status')
    date_hierarchy = 'pub_date'


class WorkBidderAdmin(admin.ModelAdmin):
    fields = ['poll', 'title', 'author_name', 'photo', 'text', 'total_likes']
    list_display = ['preview', 'poll', 'author_name', 'title', 'total_likes']
    preview = ImgPreview(lambda x: x.photo, (200, 75))


admin.site.register(Action, ActionAdmin)
admin.site.register(Poll, PollAdmin)
admin.site.register(WorkBidder, WorkBidderAdmin)
