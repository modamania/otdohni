from django.contrib import admin

from models import HeroCategory, MultiplePlace, PlaceUpdate, HeroTagging


class PlaceUpdateAdmin(admin.ModelAdmin):
    readonly_fields = ('response_url', 'place', 'place_object', )


class HeroCategoryAdmin(admin.ModelAdmin):
    raw_id_fields = ('category',)


class HeroTaggingAdmin(admin.ModelAdmin):
    raw_id_fields = ('tag',)


admin.site.register(PlaceUpdate, PlaceUpdateAdmin)
admin.site.register(HeroCategory, HeroCategoryAdmin)
admin.site.register(HeroTagging, HeroTaggingAdmin)
admin.site.register(MultiplePlace)