import datetime

from django.core.management.base import BaseCommand
from django.db.models import Q

from place.models import Place
from place import fs

import django_rq

queue = django_rq.get_queue('foursquare')

LIMIT_ONE_PASS = 30


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # fs.update_foursquare(112)
        update_dt = datetime.datetime.now() - datetime.timedelta(days=3)
        filters = Q(last_foursquare_update=None)|Q(last_foursquare_update__lt=update_dt)
        place_list = Place.default_manager.filter(filters).order_by('?')[:LIMIT_ONE_PASS]
        for place in place_list:
            queue.enqueue(fs.update_foursquare, place.id)
