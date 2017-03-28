# -*- coding: utf-8 -*-
from datetime import date, timedelta
from apps.place.utils import get_events_datelist
from apps.rating.models import Vote
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden,\
                        HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import simplejson
from django.conf import settings

from annoying.decorators import render_to, ajax_request

from place.models import Place, PlaceAddress, PlaceGallery, TempGallery
from place.forms import PlaceForm, PlaceAddressForm, PlaceGalerryForm,\
                        WorkTimeSet, AddressSet, GallerySet, FoursquarePhotoSet

from control.utils import crop_image, can_access


@can_access()
def change_image(request, image=None):
    """
    The save and cancel changes to the image
    """
    post = request.POST

    tp = True if image else False

    gallery_pk = int(post['gallery_id'])
    gallery = PlaceGallery.objects.get(pk=gallery_pk)

    temp, created = TempGallery.objects.get_or_create(gallery=gallery)

    if post.get('cancel', False):
        temp.delete()
        if not gallery.image:
            return HttpResponse(simplejson.dumps(
                {'empty': True}
            ))
        im = gallery.image
    else:
        if not image:
            image = request.FILES.values()[0]
        if not image.content_type.startswith('image'):
            raise TypeError
        temp.image = image
        temp.save()
        im = temp.image

    im.generate_thumbnails()

    json = {
        'image_url': im.url,
        'image_thumb_url': im.thumbnail.absolute_url,
    }

    if tp:
        return json
    return HttpResponse(simplejson.dumps(json))


@ajax_request
@can_access()
def gallery_photo(request):
    """
    Createion and deletion of new photos
    """
    post = request.POST

    order = int(post['order'])
    place_pk = int(post['place_id'])
    try:
        gallery_pk = int(post['gallery_id'])
    except ValueError:
        gallery_pk = None
    image = request.FILES.values()[0]

    place = get_object_or_404(Place, pk=int(place_pk))
    if gallery_pk:
        gallery = get_object_or_404(PlaceGallery, pk=int(gallery_pk))
    else:
        gallery = None

    cleaned_post = {
            "place": place.id,
            "order": order,
    }
    form = PlaceGalerryForm(cleaned_post, instance=gallery)
    if form.is_valid():
        inst = form.save()
        json = {
            'gallery_id': inst.id,
            'order': inst.order,
        }
        request.POST['gallery_id'] = inst.id
        json.update(change_image(request, image))
    else:
        json = {}

    return HttpResponse(simplejson.dumps(json))


@can_access()
@render_to('control/place_list.html')
def place_list(request):
    if not request.user.has_module_perms('place'):
        return HttpResponseForbidden()
    place_list = Place.objects.all().order_by('name')
    if 'q' in request.GET:
        q = request.GET['q']
        place_list = place_list.filter(Q(name__icontains=q))
    else:
        q = ''
    paginator = Paginator(place_list, settings.COMPANY_PER_PAGE)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        places = paginator.page(page)
    except (EmptyPage, InvalidPage):
        places = paginator.page(paginator.num_pages)

    return {
        'places': places,
        'q': q
    }


@can_access()
@render_to('control/place_show.html')
def place_show(request, place_pk):
    if not request.user.has_module_perms('place'):
        return HttpResponseForbidden()

    place = get_object_or_404(Place.objects.select_related(), pk=place_pk)
    address_list = place.address.select_related().all().order_by('-is_main_office')
    start_day = date.today()
    end_day = start_day + timedelta(days=6)
    datelist = get_events_datelist(
        place.periods.all(), start_day, end_day)
    is_voted = 0
    if request.user.is_authenticated():
        is_voted = list(Vote.objects.filter(user = request.user, object_id = place.id))

    return {
        'place': place,
        'is_voted': is_voted,
        'address_list': address_list,
        'occurences': place.periods.all(),
        'datelist': datelist,
        'address_count': address_list.count(),
        'YANDEX_MAPS_API_KEY': settings.YANDEX_MAPS_API_KEY,
        }



@can_access()
@render_to('control/place_form.html')
def place_form(request, place_pk=None):

    def save_gallery(formset, place):
        formset.save()
        for inst, form in zip(formset.get_queryset(), formset):
            if TempGallery.objects.filter(gallery=inst).exists():
                temp = TempGallery.objects.get(gallery=inst)
                inst.image = temp.image
                inst.title = form.instance.title
                inst.save()
            if form.instance.id:
                crop = [form.cleaned_data.pop(key)
                        for key in\
                        ('crop_x', 'crop_y', 'crop_x2', 'crop_y2')]
                if all(crop):
                    crop_image(inst.image, *crop)

    def save_place(form):
        place = form.save()
        place.manual_changed = True
        if 'tagging' in form.cleaned_data:
            for tag in form.cleaned_data['tagging']:
                place.tagging.add(tag)
        if 'category' in form.cleaned_data:
            for category in form.cleaned_data['category']:
                place.category.add(category)
        place.save()
        return place

    if not request.user.has_module_perms('place'):
        return HttpResponseForbidden()

    if place_pk:
        place = get_object_or_404(Place, pk=place_pk)
        gallery = place.gallery.order_by('order')
    else:
        place = None
        gallery = PlaceGallery.objects.none()

    if gallery.count() < 20:
        gallery_extra = 20 - gallery.count()
    else:
        gallery_extra = 0
    GallerySet.extra = gallery_extra

    if request.method == 'POST':
        form = PlaceForm(request.POST, request.FILES, instance=place)
        if place:
            address_formset = AddressSet(request.POST,
                                        instance=place, prefix='address')
            gallery_formset = GallerySet(request.POST, request.FILES,
                                        instance=place, prefix='gallery')
            fs_formset = FoursquarePhotoSet(request.POST,
                                        instance=place, prefix='fs')

            if form.is_valid() and address_formset.is_valid()\
                    and gallery_formset.is_valid():
                place = save_place(form)
                save_gallery(gallery_formset, place)
                address_formset.save(commit=False)
                fs_formset.save()
                return HttpResponseRedirect(
                                    reverse(place_show, args=[place.pk]))
        else:
            if form.is_valid():
                place = save_place(form)
                return HttpResponseRedirect(
                                    reverse(place_show, args=[place.pk]))
            else:
                return {
                    'form': form,
                }
    else:
        if place:
            for g in place.gallery.all():
                if not g.image: g.delete()

            if place.gallery.count() < 20:
                gallery_extra = 20 - place.gallery.count()
            else:
                gallery_extra = 0
        else:
            gallery_extra = 20
        GallerySet.extra = gallery_extra

        form = PlaceForm(instance=place)
        address_formset = AddressSet(instance=place, prefix='address')
        gallery_formset = GallerySet(instance=place, prefix='gallery')
        fs_formset = FoursquarePhotoSet(instance=place, prefix='fs')

    return {
        'place': place,
        'form': form,
        'address_formset': address_formset,
        'gallery_formset': gallery_formset,
        'fs_formset': fs_formset,
    }


@can_access()
@render_to('control/address_form.html')
def address_form(request, place_pk, address_pk=None):

    place = get_object_or_404(Place, pk=int(place_pk))

    if address_pk:
        address = get_object_or_404(PlaceAddress, pk=int(address_pk))
    else:
        address = None

    if address and address.work_time.exists():
        WorkTimeSet.extra = 0
    else:
        WorkTimeSet.extra = 1

    if request.method == 'POST':
        form = PlaceAddressForm(request.POST, instance=address)
        formset = WorkTimeSet(request.POST, instance=address)

        if form.is_valid() and formset.is_valid():
            address = form.save(commit=False)
            address.place = place
            address.save()
            form.save_m2m()

            formset.instance = address
            formset.save()

            if len(formset) != address.work_time.count():
                idx = (work_time.cleaned_data['id'].pk
                        for work_time in formset
                        if 'id' in work_time.cleaned_data
                        and work_time.cleaned_data['id'])
                address.work_time.exclude(pk__in=idx).delete()
            return HttpResponseRedirect(reverse(place_form, args=[address.place.pk]))
    else:
        form = PlaceAddressForm(instance=address)
        formset = WorkTimeSet(instance=address)

    return {
        "address": address,
        "formset": formset,
        "place": place,
        "form": form,
    }
