from django.contrib import admin
from core.utils import ImgPreview
from gourmet.forms import GourmetItemAdminForm
from gourmet.models import GourmetItem

from omskadmin.admin import SiteOnlyAdmin

class GourmetItemAdmin(SiteOnlyAdmin, admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ['title', 'preview', 'short_text', 'pub_date', 'is_published', 'is_fixed', 'get_sites']
    list_editable = ('is_published', 'is_fixed', )
    list_filter = [ 'is_published', 'is_fixed', 'sites__name']
    date_hierarchy = 'pub_date'
    search_fields = ['title', 'short_text', 'full_text']
    preview = ImgPreview(lambda x: x.get_image(), (200, 75))

    form = GourmetItemAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["initial"] = request.user
        return super(GourmetItemAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(GourmetItem, GourmetItemAdmin)
