# -*- coding: utf-8 -*-
import datetime

from place.models import Place, PlaceAddress
from place.async import update_address_geo
        

def update_foursquare(place_id):
    place = Place.default_manager.get(id=place_id)
    addr_list = place.address.all() 
    for addr in addr_list:
        foursquare = None
        if not addr.city or not addr.lat or not addr.lng:
            addr.update_geo()
        if not addr.fsid:
            addr.update_fsid()
        if addr.fsid:
            place.get_fs_photos(addr.fsid)