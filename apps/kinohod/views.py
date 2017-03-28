# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse

from api import get_schedules, get_movie_id
from place.models import Place
from event.models import Event


def schedules(request):
    event_id = request.GET.get('event_id')
    try:
        event = Event.objects.get(id=event_id)
    except Event.objects.DoesNotExist:
        return HttpResponse("{'status': 'error', 'message': 'Event not found'}")

    movie_id = get_movie_id(event.title)

    if movie_id:
        place_id = request.GET.get('place_id')
        try:
            place = Place.objects.get(id=place_id)
        except Place.objects.DoesNotExist:
            return HttpResponse("{'status': 'error', 'message': 'Place not found'}")

        schedules = get_schedules(movie_id, place.kinohod_network)
        return HttpResponse(json.dumps(schedules), content_type='application/json')
    return HttpResponse("{'movie_id': '%s'}" % movie_id)
