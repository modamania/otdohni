from django.http import HttpResponse
from django.utils import simplejson

from event.models import Event
from core.utils import as_json

import datetime


@as_json
def event_on_day(request):
    try:
        date_list = map(
            lambda x: int(x),
            [request.POST[y] for y in ('year', 'month', 'day')]
        )
    except ValueError:
        raise Http404
    events = Event.objects.on_day(
                dt=datetime.date(*date_list))
    events_json = [{
        'id': x.id,
        'title': x.title,
    } for x in events]

    return events_json


@as_json
def place_for_event(request):
    try:
        event_id = int(request.POST['event_id'])
        event = Event.objects.get(id=event_id)
    except (ValueError, Event.DoesNotExists):
        raise Http404
    places = event.place.all()
    places_json = [{
        'id': x.id,
        'title': x.name,
    } for x in places]

    return places_json
