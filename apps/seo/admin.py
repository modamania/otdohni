from django.contrib import admin
from rollyourown.seo.admin import register_seo_admin
from apps.seo.models import Metadata

register_seo_admin(admin.site, Metadata)