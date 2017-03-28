# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *



class ProfileAdmin(admin.ModelAdmin):
    list_filter = ('access_to_dasboard',)

admin.site.register(Profile, ProfileAdmin)
