# -*- coding: utf-8 -*-
from django.contrib import admin
from adminsortable.admin import SortableAdmin
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from django.shortcuts import render

from models import PlaceAddress, Place, PlaceGallery, PlaceCategory,\
                    PlaceAddressWorkTime, RateCategories, \
                    FoursquarePhoto
from forms import ChangeCategoryForm, ChangeTaggingForm


def uppand_category(formModel, action, field_name_action, func_name_rus, modeladmin, request, queryset):
    form = None

    if 'apply' in request.POST:
        form = formModel(request.POST)

        if form.is_valid():
            categorys = form.cleaned_data['categorys']

            count = 0
            for item in queryset:
                field_name, func_name = field_name_action.split('.')
                field = getattr(item, field_name)
                func = getattr(field, func_name)
                func(*categorys)
                item.save()
                count += 1

            modeladmin.message_user(request, "Категории %s в %d заведениях." % (action, count))
            return HttpResponseRedirect(request.get_full_path())

    if not form:
        form = formModel(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

    data = {
        'items': queryset,
        'form': form,
        'title': u'%s у заведений' % func_name_rus,
        'action': action,
    }
    return render(request, 'place/change_places_tags.html', data)


def append_category(*args):
    return uppand_category(ChangeCategoryForm, 'append_category',
                           'category.add', u'Добавить категории', *args)
append_category.short_description = "Добавить категорию"


def remove_category(*args):
    return uppand_category(ChangeCategoryForm, 'remove_category',
                           'category.remove', u'Удалить категории', *args)
remove_category.short_description = "Удалить категорию"


def append_tagging(*args):
    return uppand_category(ChangeTaggingForm, 'append_tagging', 'tagging.add',
                           u'Добавить тэги', *args)
append_tagging.short_description = "Добавить тэги"


def remove_tagging(*args):
    return uppand_category(ChangeTaggingForm, 'remove_tagging', 'tagging.remove',
                           u'Удалить тэги', *args)
remove_tagging.short_description = "Удалить тэги"


class AddressInline(admin.StackedInline):
    model = PlaceAddress
    extra = 0


class FoursquarePhotoInline(admin.StackedInline):
    model = FoursquarePhoto
    extra = 0
    readonly_fields = ['photo_id', 'prefix', 'suffix']



class PlaceAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'kinohod_place_id',
        'is_published',
        'promo_is_up',
        'expert_choice',
        'can_buy_tiket',
    )
    list_editable = (
        'kinohod_place_id',
        'can_buy_tiket',
    )
    list_filter = (
        'sites',
        'is_published',
        'promo_is_up',
        'expert_choice',
        'payments',
        'category',
    )
    search_fields = (
        'name',
    )
    filter_horizontal = [
        'category',
        'tagging'
    ]
    inlines = (
        AddressInline,
        FoursquarePhotoInline,
    )
    actions = [
        append_category,
        remove_category,
        append_tagging,
        remove_tagging,
    ]


class WorkTimeInline(admin.TabularInline):
    model = PlaceAddressWorkTime
    extra = 0


class AddressAdmin(admin.ModelAdmin):
    search_fields = (
        'address',
    )
    inlines = (
        WorkTimeInline,
    )
    list_filter = (
        'place',
    )


class WorkTimeAdmin(admin.ModelAdmin):
    list_filter = (
        'all_day',
        'day_off',
        'from_time',
        'till_time',
    )


class SortableAdminPlaceCategory(SortableAdmin):
    """Any admin options you need go here"""
    fieldsets = ((_('Content'), {'fields': ('main_tag', 'name',
                                'rating_title', 'is_published')}),
                (_('Options'), {'fields': ('places', 'tagging', 'order')}),
                )
    list_display = (
        '__unicode__',
        'order',
        'category_mean',
        'rating_title'
    )
    list_display_links = (
        # 'order',
        '__unicode__',
    )
    list_editable = (
        'order',
    )
    filter_horizontal = ['places']
    order_by = ['-order']


class RateCategoriesAdmin(admin.ModelAdmin):
    list_display = ('category', 'place', 'rate', 'num_votes')


class PlaceGalleryAdmin(admin.ModelAdmin):
    order_by = ['-order']


admin.site.register(PlaceAddress, AddressAdmin)
admin.site.register(PlaceAddressWorkTime, WorkTimeAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(PlaceGallery, PlaceGalleryAdmin)
admin.site.register(RateCategories, RateCategoriesAdmin)
admin.site.register(PlaceCategory, SortableAdminPlaceCategory)
