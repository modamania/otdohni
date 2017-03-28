# -*- coding: utf-8 -*-
import pytils

from django.contrib.sites.models import Site

from place.models import PlaceAddress, PlaceCategory, PaymentSystem, PlaceAddressWorkTime, Place
from city.models import City

from tagging.models import Tag


def update_place(place_object, place):
    city = City.objects.get(site_id=place_object['site_id'])
    for f in ['name', 'url', 'email']:
        if f in place_object:
            setattr(place, f, place_object[f])
    place.identity = place_object['response_url']

    place.category.clear()
    for cat in place_object['category']:
        place.category.add(PlaceCategory.objects.get(id=cat['id']))

    place.tagging.clear()
    for tag in place_object['tagging']:
        place.tagging.add(Tag.objects.get(id=tag['id']))

    place.payments.clear()
    payments = place_object.get('payments')
    if payments:
        payments_list = []
        for p in payments:
            if not p:
                continue
            p_slug = pytils.translit.slugify(p)
            payment, is_created = PaymentSystem.objects.get_or_create(name=p_slug, display=p)
            payments_list.append(payment)
        place.payments.add(*payments_list)

    for adr_object in place_object['adr']:
        try:
            a = '%s, %s' % (city.name, adr_object['address'])
            stupid_adr = PlaceAddress.objects \
                .get(address=a, place = place)
        except PlaceAddress.DoesNotExist:
            pass
        else:
            stupid_adr.delete()

        adr, adr_created = PlaceAddress.objects \
            .get_or_create(address=adr_object['address'], place = place)
        if 'phone' in adr_object:
            adr.phone = adr_object['phone']
        adr.save()

        if 'wt_list' in adr_object:
            adr.work_time.all().delete()
            for wt_dump in adr_object['wt_list']:
                wt = PlaceAddressWorkTime(**wt_dump)
                wt.address = adr
                wt.save()
    place.save()
    return True

def create_place(place_object):
    if not 'name' in place_object:
        create_moderaion(place_object, None)
        return False
    if not place_object['name']:
        create_moderaion(place_object, None)
        return False

    kwargs = {
        'is_published' : True,
        'manual_changed' : False,
        'identity' : place_object['response_url'],
    }
    place = Place(**kwargs)
    for f in ['name', 'url', 'email']:
        if f in place_object:
            setattr(place, f, place_object[f])
    place.save(site=Site.objects.get(id=place_object['site_id']))

    for cat in place_object['category']:
        place.category.add(PlaceCategory.objects.get(id=cat['id']))

    for tag in place_object['tagging']:
        place.tagging.add(Tag.objects.get(id=tag['id']))

    payments = place_object.get('payments')
    if payments:
        payments_list = []
        for p in payments:
            p_slug = pytils.translit.slugify(p)
            payment, is_created = PaymentSystem.objects.get_or_create(name=p_slug, display=p)
            payments_list.append(payment)
        place.payments.add(*payments_list)

    if not place_object['adr']:
        create_moderaion(place_object, place)
        return False

    for adr_object in place_object['adr']:
        adr = PlaceAddress()
        adr.address=adr_object['address']
        if 'phone' in adr_object:
            adr.phone = adr_object['phone']
        adr.place = place
        adr.save()

        if 'wt_list' in adr_object:
            for wt_dump in adr_object['wt_list']:
                wt = PlaceAddressWorkTime(**wt_dump)
                wt.address = adr
                wt.save()

    place.save()
    return True
