# -*- coding: utf-8 -*-
import pytils
import pickle

from django.db import models

from place.models import PlaceCategory, Place, PlaceAddress, PlaceAddressWorkTime
from payments.models import PaymentSystem
from tagging.models import Tag
from city.models import City
from django.contrib.sites.models import Site

from graber.utils import update_place, create_place


UPDATE_STATUS = (
    ('new', 'new'),
    ('approved', 'approved'),
    ('rejected', 'rejected'),
)


class HeroCategory(models.Model):
    category = models.ForeignKey(PlaceCategory, related_name='hero_category')
    hero_name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.hero_name

    def save(self, *args, **kwargs):
        self.hero_name = self.hero_name.lower()
        super(HeroCategory, self).save(*args, **kwargs)


class HeroTagging(models.Model):
    tag = models.ForeignKey(Tag)
    hero_name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.hero_name

    def save(self, *args, **kwargs):
        self.hero_name = self.hero_name.lower()
        super(HeroTagging, self).save(*args, **kwargs)


class MultiplePlace(models.Model):
    place = models.ManyToManyField(Place)


    def __unicode__(self):
        return self.place.all()[0].__unicode__()


class PlaceUpdate(models.Model):
    status = models.CharField(choices=UPDATE_STATUS, default='new', max_length=8)
    response_url = models.CharField(max_length=255)
    place = models.ForeignKey(Place, related_name='updates', blank=True, null=True)
    place_object = models.TextField()
    # city = models.ForeignKey(City)


    def __unicode__(self):
        if self.place:
            return self.place.__unicode__()
        else:
            place_object = self.get_place_object()
            if place_object:
                return place_object['name']
            else:
                return u'Название не известно'
            

    def approve(self):
        if self.place:
            return self.update_place()
        else:
            return self.create_place()


    def update_place(self):
        place_object = pickle.loads(self.place_object)
        return update_place(place_object, self.place)


    def create_place(self):
        place_object = pickle.loads(self.place_object)
        return create_place(place_object)

    def get_place_object(self):
        try:
            place_object = pickle.loads(self.place_object)
        except Exception as e:
            print e
        else:
            return place_object
        return None

