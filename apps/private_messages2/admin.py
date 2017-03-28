# -*- coding: utf-8 -*-
from django.contrib import admin

from models import Chain, Message

# class ChainAdmin(admin.ModelAdmin):


admin.site.register(Chain)
admin.site.register(Message)