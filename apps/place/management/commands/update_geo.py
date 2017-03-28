import datetime

from django.core.management.base import BaseCommand
from django.db.models import Q

from place.models import PlaceAddress
from place.async import update_address_geo

import django_rq

queue = django_rq.get_queue('default')

LIMIT_ONE_PASS = 30


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        filters = Q(city=None)|Q(lat=None)|Q(lng=None)
        adr_list = PlaceAddress.objects.filter(filters)[:LIMIT_ONE_PASS]
        for adr in adr_list:
            queue.enqueue(update_address_geo, adr.id)