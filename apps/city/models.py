# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.sites.models import Site


# Create your models here.
class City(models.Model):
    site = models.OneToOneField(Site, related_name='city')
    name = models.CharField(max_length=40)
    post = models.CharField(max_length=20, null=True, blank=True, default=None)
    name_by_geoip = models.CharField(max_length=20, null=True, blank=True, default=None)
    is_default = models.BooleanField(default=False)
    genitive = models.CharField(u'Родительный падеж (а)', max_length=50, null=True, blank=True, default=None)
    accusative = models.CharField(u'Винительный падеж (е)', max_length=50, null=True, blank=True, default=None)
    foursquare = models.CharField(u'Название на Foursquare', max_length=50, null=True, blank=True, default=None)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name
