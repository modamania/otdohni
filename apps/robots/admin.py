# -*- coding:utf-8 -*-
from apps.robots.models import RobotsItem
from django.contrib import admin

class RobotsAdmin(admin.ModelAdmin):
    list_display = (
        'url',
        )

admin.site.register(RobotsItem, RobotsAdmin)
