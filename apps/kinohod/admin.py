from django.contrib import admin

from models import KinohodSeance


class KinohodSeanceAdmin(admin.ModelAdmin):
    list_filter = ('dt', 'event', 'place',)
    list_display = ('place', 'event', 'dt', 'seance_id',)

admin.site.register(KinohodSeance, KinohodSeanceAdmin)