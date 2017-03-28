# -*- coding:utf-8 -*-
from django.contrib import admin
from blog.models import Post
from blog.forms import PostAdminForm

from omskadmin.admin import SiteOnlyAdmin

class PostAdmin(SiteOnlyAdmin, admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ['title', 'short_text', 'pub_date', 'is_published', 'is_fixed', 'get_sites']
    list_editable = ('is_published', 'is_fixed', )
    list_filter = [ 'is_published', 'is_fixed', 'sites__name']
    date_hierarchy = 'pub_date'
    search_fields = ['title', 'short_text', 'full_text']
    raw_id_fields = ['user', 'sites']
    form = PostAdminForm


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["initial"] = request.user
        return super(PostAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Post, PostAdmin)
