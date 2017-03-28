# -*- coding: utf-8 -*-
import time
import random

from place.models import PlaceAddress


def update_address_geo(id):
    time.sleep(random.random() * 10 + 1)
    try:
        address = PlaceAddress.objects.get(id=id)
    except PlaceAddress.DoesNotExist:
        pass
    else:
        address.update_geo()
