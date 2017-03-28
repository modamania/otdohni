#coding: utf-8

from django.contrib import admin
from core.utils import ImgPreview
from common.actions import make_unpublished, make_published
from sales.forms import CouponAdminForm
from sales.models import Coupon
from django.utils.translation import ugettext_lazy as _

class CouponAdmin(admin.ModelAdmin):
    list_display = ['title', 'preview', 'preview_small', 'start_date', 'end_date', 'is_published', 'views']
    list_editable = ('is_published', )
    list_filter = [ 'is_published',]
    date_hierarchy = 'start_date'
    search_fields = ['title',]
    preview = ImgPreview(lambda x: x.image, (200, 75), _('image'))
    preview_small = ImgPreview(lambda x: x.small_image, (200, 75), _('small image'))

    form = CouponAdminForm

    actions = [make_published, make_unpublished]

admin.site.register(Coupon, CouponAdmin)