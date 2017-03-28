from django.contrib import admin
from common.actions import make_published, make_unpublished
from core.utils import ImgPreview

from lunch.forms import LunchObjectAdminForm
from lunch.models import LunchObject

from omskadmin.admin import SiteOnlyAdmin

from django.utils.translation import ugettext_lazy as _


class LunchObjectAdmin(SiteOnlyAdmin, admin.ModelAdmin):

    list_display = ['title', 'is_published', 'start_date', 'end_date', 'get_sites']
    list_editable = ('is_published', )
    list_filter = [ 'is_published', 'sites__name']
    search_fields = ['title', 'description', ]
    preview = ImgPreview(lambda x: x.image, (200, 75), _('logo'))

    form = LunchObjectAdminForm

    actions = [make_published, make_unpublished]


admin.site.register(LunchObject, LunchObjectAdmin)
