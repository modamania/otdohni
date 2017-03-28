from django.contrib import admin
from models import Event, EventCategory, Occurrence, TodayEvent, SoonEvent
from forms import EventAdminForm, OccurrenceForm
from kinohod.models import KinohodSeance

from django.utils.translation import ugettext_lazy as _


class PlaceInline(admin.TabularInline):
    model = Occurrence
    extra = 1
    form = OccurrenceForm


class KinohodInline(admin.TabularInline):
    model = KinohodSeance
    extra = 1
    # form = OccurrenceForm


class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'category_mean', 'rating_title']
    prepopulated_fields = {'slug': ('title',)}


class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'original_title', 'category', 'get_places', 'rate', 'num_votes']
    list_filter = [ 'category']
    search_fields = ['title', 'category__title', 'description']
    inlines = [PlaceInline, KinohodInline, ]
    date_hierarchy = 'pub_date'

    def get_places(self, obj):
        """Return the places linked in HTML"""
        return '<br/>'.join(['%s(%s)' %
        (period.place, period.start_date.strftime('%d.%m.%Y')) for period in obj.periods.all()])

    get_places.allow_tags = True
    get_places.short_description = _('place(s)')
    model = EventAdminForm


admin.site.register(Event, EventAdmin)
admin.site.register(EventCategory, EventCategoryAdmin)
admin.site.register(TodayEvent)
admin.site.register(SoonEvent)