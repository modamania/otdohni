# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *



class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'title']
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name', 'slug', 'title']

admin.site.register(Tag, TagAdmin)
