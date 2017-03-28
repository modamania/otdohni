# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import cache_page

from annoying.decorators import render_to

from tagging.models import Tag
from rating.models import Vote
from core import Indexable
from core.utils import denormalize_comments_async

from place.models import Place, PlaceCategory
from place.utils import render_place_list, sort_by_name, get_events_datelist
from place import fs

import math
from datetime import time, date, timedelta

import django_rq

queue = django_rq.get_queue('asap')


def default_sort_place_list(place_list):
    (
        place_list_with_promo,
        place_list_without_promo
    ) = map(
        lambda x: sorted(x, sort_by_name), (
            place_list.filter(promo_is_up=True).order_by('-priority'),
            place_list.filter(promo_is_up=False).order_by('-priority')
            )
    )

    place_list_with_promo.sort(key=lambda x: x.priority, reverse=True)
    place_list_without_promo.sort(key=lambda x: x.priority, reverse=True)

    place_list = place_list_with_promo + place_list_without_promo
    return place_list

def sort_place_list(request, place_list):
    sort_type = request.GET.get('order_by', 'default')
    if sort_type == 'default':
        return default_sort_place_list(place_list)
    elif sort_type == 'alphabet':
        return sorted(place_list, sort_by_name)
    elif sort_type == 'rating':
        return place_list.order_by('-score')
    return Place.objects.empty()


def get_paginator(request, place_list):
    page = request.GET.get('page', 1)
    try:
        page = int(page)
    except ValueError:
        if not page:
            page = 1
        else:
            raise Http404

    if page < 1:
        raise Http404

    place_list = sort_place_list(request, place_list)
    paginator = Paginator(place_list, settings.COMPANY_PER_PAGE)

    try:
        places = paginator.page(page)
    except (EmptyPage, InvalidPage):
        raise Http404

    return places, paginator


@render_place_list('place/search.html')
def search_by_name(request):
    name = request.GET.get('t', '')
    if name:
        info_about_result = _('Result search company by name: %(name)s' \
            % {'name': name})
        results = Place.search.query("*%s*" % name)
        ids = [m.id for m in results]
        place_list = Place.objects.published().filter(id__in=ids)
        place_list, paginator = get_paginator(request, place_list)
    else:
        info_about_result = _('Few charaters to search')
        place_list = Place.objects.none()
    return {
        't': name,
        'info_about_result': info_about_result,
        'places': place_list,
    }


#@cache_page(60 * 15)
@render_place_list('place/main_page.html')
def main_page(request):
    categories = PlaceCategory.objects\
                                .select_related().filter(is_published=True)\
                                .order_by('order')
    categories_groups = []
    groups_count = 4
    categories_total = len(categories)
    categories_in_group = int(math.ceil(categories_total / float(groups_count)))
    for i in range(groups_count):
        categories_groups.append(categories[i*categories_in_group:(i+1)*categories_in_group])
    
    place_list_new_promo = Place.objects.published() \
        .filter(promo_is_up=True).order_by('-date_mark_as_new', 'name')[:15]

    (
        place_list_expert_promo,
        place_list_expert_no_promo
    ) = map(
        lambda x: sorted(x, sort_by_name), (
            Place.objects.experted_promouted(),
            Place.objects.experted_no_promouted()
        )
    )

    places_promo_vote = Vote.objects.get_top(Place,
                                    objects=Place.objects.promouted(),
                                    limit=20000)
    places_promo = Indexable(places_promo_vote)[:6]
    place_list_choice_promo = [place for place, vote in places_promo]

    places_no_promo_vote = Vote.objects.get_top(Place,
                                    objects=Place.objects.filter(
                                    promo_is_up=False),
                                    limit=20000)
    places_no_promo = Indexable(places_no_promo_vote)[:20]
    place_list_choice_no_promo = [place for place, vote in places_no_promo]

    place_list_sponsor = Place.objects.sponsored()[:9]

    return {
        'categories' : categories_groups,
        'place_list_new_promo': place_list_new_promo,
        'place_list_expert_promo': place_list_expert_promo,
        'place_list_expert_no_promo': place_list_expert_no_promo,
        'place_list_choice_promo': place_list_choice_promo,
        'place_list_choice_no_promo': place_list_choice_no_promo,
        'place_list_sponsor': place_list_sponsor,
    }


def get_company_in_category(request, slug):
    try:
        category = Tag.objects.get(slug=slug).place_category
    except Tag.DoesNotExist:
        raise Http404

    params = {}
    params['category'] = category
    place_list = category.places.published().order_by('name')

    time_selectors_is_on = bool(int(request.GET.get('tsio', 0)))
    params['time_selectors_is_on'] = time_selectors_is_on
    if time_selectors_is_on:
        params['use_filter'] = True
        all_day = bool(int(request.GET.get('all_day', 0)))
        params['all_day'] = all_day
        if all_day:
            place_list = place_list.filter(address__work_time__all_day=True)
        else:
            try:
                from_time = request.GET.get('from_time', None)
                if from_time:
                    from_time = [int(i) for i in from_time.split(':')]
                    from_time = time(from_time[0], from_time[1], 0)
                    place_list = place_list.filter(address__work_time__from_time__lte=from_time)
                params['from_time'] = from_time
                till_time = request.GET.get('till_time', None)
                if till_time:
                    till_time = [int(i) for i in till_time.split(':')]
                    till_time = time(till_time[0], till_time[1], 0)
                    place_list = place_list.filter(address__work_time__till_time__gte=till_time)
                params['till_time'] = till_time
            except ValueError:
                pass

    if 'tag' in request.GET:
        params['use_filter'] = True
        tags_ids = [int(i) for i in request.GET.getlist('tag')]
        for tag_id in tags_ids:
            place_list = place_list.filter(tagging__id=tag_id)
        params['tags_ids'] = tags_ids

    if 'district' in request.GET:
        params['use_filter'] = True
        districts_keys = request.GET.getlist('district')
        place_list = place_list.filter(address__district__in=districts_keys)
        params['districts_keys'] = districts_keys

    place_ids = [place.pk for place in place_list]
    params['place_list'] = Place.objects.select_related()\
                                        .filter(pk__in=place_ids).all()

    return params


#@cache_page(60 * 15)
@render_place_list('place/company_in_category.html')
def show_category(request, slug):
    params = get_company_in_category(request, slug)
    params['places'], params['paginator'] = get_paginator(request, params['place_list'])
    params.pop('place_list')
    return params


#@cache_page(60 * 15)
@render_place_list('place/company_in_tag.html')
def show_places_by_tag(request, tag_slug):
    try:
        tag = Tag.objects.get(slug=tag_slug)
    except Tag.DoesNotExist:
        raise Http404
    place_list = tag.places.published()

    places, paginator = get_paginator(request, place_list)
    return {
        'tag': tag,
        'places': places,
        'paginator': paginator,
    }


@render_to('place/place_show.html')
def place_show(request, place_pk):
    place = get_object_or_404(Place.objects.select_related(), pk=place_pk)

    session_key = 'visited_place_%s' % place.pk
    if not request.session.get(session_key):
        Place.objects.filter(pk=place.pk).update(hits=F('hits')+1) # avoiding race conditions
        request.session[session_key] = True
        place.hits += 1

    address_list = place.address.select_related().all().order_by('-is_main_office')
    start_day = date.today()
    end_day = start_day + timedelta(days=6)
    datelist = get_events_datelist(
    place.periods.all(), start_day, end_day)
    is_voted = 0
    if request.user.is_authenticated():
        is_voted = list(Vote.objects.filter(user = request.user, object_id = place.id))

    if place.foursquare_show:
        foursquare_photo = list(place.foursquare_photo.filter(is_published=True))
        if settings.UPDATE_FOURSQUARW_WITH_VIEW and settings.USE_RQ:
            queue.enqueue(fs.update_foursquare, place.id)
    else:
        foursquare_photo = None

    denormalize_comments_async(place)

    return {
        'place': place,
        'is_voted': is_voted,
        'address_list': address_list,
        'occurences': place.periods.all(),
        'datelist': datelist,
        'address_count': address_list.count(),
        'YANDEX_MAPS_API_KEY': settings.YANDEX_MAPS_API_KEY,
        'foursquare_photo': foursquare_photo,
    }
