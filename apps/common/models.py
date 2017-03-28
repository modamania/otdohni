#-*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.comments.models import BaseCommentAbstractModel
from django.utils.translation import ugettext_lazy as _

from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager

from django.db import models
from django.conf import settings
from yandex_maps import api


class FakeUser(object):
    def __init__(self, name=u'ОтдохниОмск.ру', url='/about/'):
        self.name = name
        self.url = url

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return self.url

class WithAuthors(models.Model):
    """ABSTRACT - model with authors should inherit it"""
    user = models.ForeignKey('auth.User', null=True, blank=True, verbose_name=_('user'))
    ext_authors = models.CharField(_('external authors'), max_length=255, null=True, blank=True)
    ext_authors_link = models.URLField(_('external authors link'), verify_exists=False, null=True, blank=True,
                                        help_text=_('link where user will get after licking on authors'))

    class Meta:
        abstract = True

    def author(self):
        "Return user or FakseUser"
        if self.user:
            return self.user.get_profile()
        if self.ext_authors:
            return FakeUser(self.ext_authors, self.ext_authors_link)
        return FakeUser()



class WithPublished(models.Model):
    PUBLISHED_CHOICES = (
        (True, _('Published')),
        (False, _('Not published')),
    )

    is_published = models.BooleanField(_('is published'), choices=PUBLISHED_CHOICES, default=True)
    pub_date = models.DateTimeField(default=datetime.now)

    class Meta:
        abstract = True


YANDEX_KEY = getattr(settings, 'YANDEX_MAPS_API_KEY', None)

class WithMapAndAddress(models.Model):
    address = models.CharField(u'Адрес', max_length=255)
    longtitude = models.FloatField(u'Долгота', null=True, blank=True)
    latitude = models.FloatField(u'Широта', null=True, blank=True)

    class Meta:
        abstract = True

    def get_detail_level(self):
        return 5

    def get_map_url(self, width=None, height=None, detail_level = 5):
        w = int(width) if width else settings.YANDEX_MAPS_W
        h = int(height) if height else settings.YANDEX_MAPS_H
        detail_level = int(detail_level) or self.get_detail_level()

        if YANDEX_KEY is not None:
            return api.get_map_url(YANDEX_KEY, self.longtitude, self.latitude, detail_level, w, h)
        else:
            return ''

    def fill_geocode_data(self):
        if YANDEX_KEY is not None:
            longtitude, latitude = api.geocode(settings.YANDEX_MAPS_API_KEY, self.address)
            if self.pk and longtitude and latitude or not self.pk:
                self.longtitude, self.latitude = longtitude, latitude

    def save(self, *args, **kwargs):
        # fill geocode data if it is unknown
        if self.pk or (self.longtitude is None) or (self.latitude is None):
            self.fill_geocode_data()
        super(WithMapAndAddress, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.address


class WithSite(models.Model):
    """ Add many-to-many Site field to app model for manage on different sites
    """
    sites = models.ManyToManyField(Site,
            verbose_name=_('sites publication'),
            blank=True, null=True)

    on_site = CurrentSiteManager()

    class Meta:
        abstract = True

class SeparatedValuesField(models.TextField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop('token', ',')
        super(SeparatedValuesField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value: return
        if isinstance(value, list):
            return value
        return value.split(self.token)

    def get_db_prep_value(self, value):
        if not value: return
        assert(isinstance(value, list) or isinstance(value, tuple))
        return self.token.join([unicode(s) for s in value])

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

class ObjectSubscribe(BaseCommentAbstractModel):
    user = models.ForeignKey(User, verbose_name=_('User'))