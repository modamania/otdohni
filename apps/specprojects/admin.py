# -*- coding: utf-8 -*-
from specprojects.models import SpecProject
from django.contrib import admin

class SpecProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("top_title",)}
    list_display = ['top_title', 'title', 'is_in_top']
    list_filter = [ 'is_in_top']
    search_fields = ['top_title', 'title', 'slug']
    fields = ('title', 'is_in_top', 'top_title', 'slug', 'color', 'description', 'sites')

admin.site.register(SpecProject, SpecProjectAdmin)