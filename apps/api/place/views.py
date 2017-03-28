# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.utils.html import strip_tags
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, Http404
from django.conf import settings

from annoying.functions import  get_object_or_None
from api.utils import json

from event.models import Event
from photoreport.models import PhotoReport
from action.models import Action
from place.models import Place, PlaceCategory
from place.views import get_company_in_category, sort_place_list
from place.views import get_paginator as company_paginator
from place.async import update_address_geo
from tagging.models import Tag

import django_rq

queue = django_rq.get_queue('asap')


# В модели Place есть свой метод дампа, но он завязан с киноходом
# Сечас сделаю другой метод дампа, но нужо всё перенести в модель Place
# И протестировать совместно с киноходом.
def place_dump(place):
    place_fields = [
        'id',
        'name',
        'url',
        'email',
        'promo_is_up',
        'photo',
        'num_comments',
    ]

    place_object = dict()
    for f in place_fields:
        place_object[f] = unicode(getattr(place, f, None))

    place_object['rating'] = int(place.score / 5 * 100)

    place_object['adr'] = list()
    for adr in place.address.all():
        adr_object = dict()
        for f in adr._meta.fields:
            if not f == adr._meta.pk and \
                not f.name in ('place', 'city', 'lat', 'lng'):
                adr_object[f.name] = unicode(getattr(adr, f.name))
        if adr.geopoint:
            lng, lat = adr.geopoint.split(',')
            adr_object['lng'] = lng
            adr_object['lat'] = lat
        else:
            if adr.lng and adr.lat:
                adr_object['lng'] = adr.lng
                adr_object['lat'] = adr.lat
            else:
                adr_object['lng'] = u''
                adr_object['lat'] = u''
                if settings.USE_RQ:
                    queue.enqueue(update_address_geo, adr.id)

        adr_object['city_id'] = adr.city_id
        adr_object['wt_list'] = [wt_dump(wt) for wt in adr.work_time.all()]
        place_object['adr'].append(adr_object)

    place_object['tagging'] = list()
    for tag in place.tagging.all():
        tag_object = dict()
        for f in tag._meta.fields:
            if not f == tag._meta.pk:
                tag_object[f.name] = unicode(getattr(tag, f.name))
        tag_object['url'] = reverse('show_places_by_tag', args=[tag.slug])
        place_object['tagging'].append(tag_object)

    return place_object


def wt_dump(wt):
    j = dict()
    for f in wt._meta.fields:
        if not f == wt._meta.pk and not f.name == 'address':
            j[f.name] = unicode(getattr(wt, f.name))
    return j


@json
def count_place_in_category(request, slug):
    params = get_company_in_category(request, slug)
    response = {'count': str(len(params['place_list']))}
    return response

@json
def place_list_by_url(request, slug=None, tag=None):
    if not tag and not slug:
        raise Http404
    if tag:
        tag = get_object_or_404(Tag, slug=tag)
        place_list = tag.places.published()
    else:
        params = get_company_in_category(request, slug)
        place_list = params['place_list']

    if 'page' in request.GET:
        place_list, paginator = company_paginator(request, place_list)
    else:
        offset = int(request.GET.get('offset', 0))
        length = int(request.GET.get('length', settings.COMPANY_PER_PAGE))
        place_list = sort_place_list(request, place_list)[offset:offset+length]

    response = [place_dump(p) for p in place_list]
    return response

@json
def search_by_name(request):
    name = request.GET.get('t', '')
    path = request.GET.get('path', None)
    results = Place.search.query('*'+name+'*')
    if path:
        slug = path.strip('/').split('/')
        if slug:
            cat = get_object_or_None(PlaceCategory, main_tag__slug=slug[-1])
            if cat:
                results = Place.search.query('*'+name+'*').filter(category=cat.id)
    names = []
    if len(name) >= 1:
        if results:
            for item in results:
                names.append({
                    'label': item.name,
                    'value': reverse('place.views.place_show', \
                        args=[item.id])
                })
    return {'names': names}


def search_all(request):
    name = request.GET.get('t', '')
    a = request.GET.get('a', None)
    place_result = Place.search.query('*'+name+'*')
    event_result = Event.search.query('*'+name+'*')
    photo_result = PhotoReport.search.query('*'+name+'*')
    action_result = Action.search.query('*'+name+'*')
    total_count = place_result.count() + event_result.count() + photo_result.count() + action_result.count()

    place_list = [{
        'title':item.name,
        'url':item.get_absolute_url(),
        'desc': '; '.join([addr.address+' - '+addr.phone for addr in item.address.all()]),
        'tags': ', '.join([tag.name for tag in item.tagging.all()]),
    } for item in place_result]

    event_list = [{
        'title':item.title,
        'url':item.get_absolute_url(),
        'desc': strip_tags(item.description)[:250],
        'tags': item.category.title,
    } for item in event_result]

    photo_list = [{
        'title':item.title,
        'url':item.get_absolute_url(),
        'desc': '%s - %s' % (item.date_event.strftime('%d.%m.%Y'), (item.place_event and item.place_event.name) or ''),
#        'tags': ', '.join([tag.name for tag in item.tags.all()])
        'tags':u'Фотоотчеты'
    } for item in photo_result]

    action_list = [{
        'title':item.title,
        'url':item.get_absolute_url(),
        'desc': strip_tags(item.full_text)[:250],
        'tags': u'Конкурсы'
    } for item in action_result]

    if place_result:
        place_dict = {
            'title': u'Заведения',
            'count': place_result.count(),
            'item_list': place_list,
        }
    else:
        place_dict = None

    if event_result:
        event_dict = {
            'title': u'События',
            'count': event_result.count(),
            'item_list': event_list,
        }
    else:
        event_dict = None

    if photo_result:
        photo_dict = {
            'title': u'Фотоотчеты',
            'count': photo_result.count(),
            'item_list': photo_list,
        }
    else:
        photo_dict = None

    if action_result:
        action_dict = {
            'title': u'Конкурсы',
            'count': action_result.count(),
            'item_list': action_list,
        }
    else:
        action_dict = None

    container_list = [place_dict, event_dict, photo_dict, action_dict]
    container_list = filter(None, container_list)

    data = {
        'searchword': name,
        'item_length': total_count,
        'container_list': container_list,
    }

    if a:
        return HttpResponse(simplejson.dumps(data),
                            mimetype='application/javascript')
    else:
        data['container_list'] = list(place_list) + list(event_list) + list(photo_list) + list(action_list)
        return render(request, 'search/search_list.html', data)
