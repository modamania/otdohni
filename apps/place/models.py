# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from tagging.models import Tag
from rating.signals import user_voted
from djangosphinx.models import SphinxSearch
from sorl.thumbnail.fields import ImageWithThumbnailsField
from adminsortable.models import Sortable
from common.models import WithSite
from payments.models import PaymentSystem
from city.models import City
from core.utils import get_json
from rating.models import Vote

from place.managers import CategoryRateManager, PlaceManager, GalleryManager
from place.utils import gen_file_name

import Levenshtein


FS_AUTH = {
    'client_id': 'NUTXTLC5QZ55E0AY43FD5GLIFZICBK4GZMWY3LGHNQO0DRIC',
    'client_secret': 'X2TEVOMHIXODF2XWZNPJMOVTWUCKYZ5ENCAK0FMPIBPL1T0M',
    'v': '20131225',
}

#UnicodeDecodeError at /admin/place/placeaddressworktime/
#'ascii' codec can't decode byte 0xd0 in position 0: ordinal not in range(128)

class PlaceCategory(Sortable):
    main_tag = models.OneToOneField(Tag,
                        related_name='place_category',
                        verbose_name=_('main tag'))
    places = models.ManyToManyField('Place',
                        through='RateCategories',
                        blank=True, null=True)
    tagging = models.ManyToManyField(Tag,
                        verbose_name=_('child tags'),
                        null=True, blank=True)
    name = models.CharField(max_length=25,
                        verbose_name=_('used name'),
                        null=True, blank=True,)
    is_published = models.BooleanField(verbose_name=_('is published'),
                        default=False)
    category_mean = models.FloatField(_('category mean rate'),
                        editable=False,
                        default=1.0,
                        blank=True, null=True)
    rating_title = models.CharField(verbose_name=_('top rating title'),
                        max_length=80,
                        blank=True, null=True,)

    objects = CategoryRateManager()

    class Meta(Sortable.Meta):
        verbose_name = _('Place category')
        verbose_name_plural = _('Place categories')


    def __unicode__(self):
        if self.name:
            return self.name
        else:
            return self.main_tag.name

    def save(self, *args, **kwargs):
        super(PlaceCategory, self).save(*args, **kwargs)
        self.category_mean = PlaceCategory.objects.get_category_mean(self)
        super(PlaceCategory, self).save(*args, **kwargs)

    @property
    def slug(self):
        return self.main_tag.slug

    @property
    def is_taxi(self):
        return self.name == u'Такси'

    def get_absolute_url(self):
        return reverse('place_show', args=[self.id,])


class Place(WithSite):
    category = models.ManyToManyField(PlaceCategory, null=True,
                blank=True, verbose_name=_('category'),
                #related_name='places')
                through='RateCategories')
    name = models.CharField(max_length=255, verbose_name=_('company name'))
    tagging = models.ManyToManyField(Tag, related_name='places', null=True,
                blank=True, verbose_name=_('tagging'))
    description = models.TextField(null=True, blank=True,
                verbose_name=_('description'))
    hits = models.IntegerField(default=0, verbose_name=_('hits'),)
    logotype = ImageWithThumbnailsField(upload_to=gen_file_name,
                thumbnail={'size': (360, 170), 'quality': (100), 'subdir': '_thumb'},
                null=True, blank=True, verbose_name=_('logo of company'))
    logotype_alt = models.CharField(blank=True, null=True,
                verbose_name=_('logotype_alt'), max_length=255)
    photo = ImageWithThumbnailsField(upload_to=gen_file_name,
                thumbnail={'size': (360, 170), 'options': {'crop':',10'}, 'quality': (100), 'subdir': '_thumb'},
                null=True, blank=True, verbose_name=_('photo'))
    photo_alt = models.CharField(blank=True, null=True,
                verbose_name=_('photo_alt'), max_length=255)
    email = models.CharField(max_length=255,
                null=True, blank=True,
                verbose_name=_('email of company'))
    url = models.URLField(verify_exists=False, null=True, blank=True,
                verbose_name=_('web site'))
    url_is_follow = models.BooleanField(_('follow url'), default=False)
    urlhits = models.IntegerField(default=0, verbose_name=_('urlhits'))
    promo_is_up = models.BooleanField(default=False,
                verbose_name=_('promo is published'))
    date_promo_up = models.DateField(null=True, blank=True,
                verbose_name=_('date of pulished promo'))
    date_promo_down = models.DateField(null=True, blank=True,
                verbose_name=_('date of unpublished promo'))
    is_published = models.BooleanField(default=False,
                verbose_name=_('company is published'))
    is_sponsor = models.BooleanField(default=False,
                verbose_name=_('company is the sponsor'))
    sponsor_logo = ImageWithThumbnailsField(upload_to=gen_file_name,
                thumbnail={'size': (200, 45), 'quality': (100), 'subdir': '_thumb'},
                null=True, blank=True, verbose_name=_("sponsor's logo"))
    expert_choice = models.BooleanField(default=False,
                verbose_name=_('expert`s choice'))
    main_address = models.TextField(editable=False,
                verbose_name=_('main address'),
                blank=True, null=True)
    num_comments = models.PositiveIntegerField(_('number of comments'),
                default=0)
    date_modified = models.DateTimeField(auto_now=True, default=datetime.now,
                verbose_name=_('date of change'))
    date_mark_as_new = models.DateTimeField(default=datetime.now,
                verbose_name=_('date of mark as new'), blank=True, null=True)
    priority = models.IntegerField(default=0, verbose_name=_('priority'),)
    kinohod_place_id = models.IntegerField(verbose_name=_('kinohod place id'),
                        default=0, blank=True, null=True)
    can_buy_tiket = models.BooleanField(default=False)
    manual_changed = models.BooleanField(default=True)
    payments = models.ManyToManyField(PaymentSystem, default=None, blank=True, null=True)
    flash3d = models.URLField(default=None, blank=True, null=True,
                verbose_name=_('panorama'))
    identity = models.CharField(max_length=255, default='', blank=True, null=True)
    last_foursquare_update = models.DateTimeField(null=True, blank=True)

    foursquare_show = models.BooleanField(verbose_name=_(u'show foursquare photos'),
                        default=True)

    score = models.FloatField(verbose_name=_(u'Score by votes'), default=0, editable=False)

    search = SphinxSearch(
        index='place_index',
        weights={
            'name': 100,
        },
        mode='SPH_MATCH_ALL',
        rankmode='SPH_RANK_NONE',
    )

    objects = PlaceManager()
    default_manager = models.Manager()

    def save(self, *args, **kwargs):
        self.main_address = self._main_address
        if 'site' in kwargs:
            site = kwargs.pop('site')
        else:
            site = None
        self.score = Vote.objects.get_score(self)['score']
        super(Place, self).save(*args, **kwargs)
        if not self.sites.exists():
            self.sites.add(site or Site.objects.get_current())

    class Meta:
        verbose_name = _('Place')
        verbose_name_plural = _('Places')
        ordering = ['name']

    def __unicode__(self):
        return self.name
        #return u"%s" % self.name

    @models.permalink
    def get_absolute_url(self):
        return ('place_show', [str(self.id)])

    @models.permalink
    def get_edit_url(self):
        return ("control_place_edit", [str(self.pk)])

    @property
    def _main_address(self):
        if self.address.count():
            try:
                address = self.address.filter(
                    is_main_office=True).all()[0].address
            except IndexError:
                address = self.address.all()[0].address
        else:
            address = None
        return address

    def get_main_address(self):
        if self.address.count():
            try:
                return self.address.filter(
                    is_main_office=True).all()[0]
            except IndexError:
                return self.address.all()[0]
        return None

    @property
    def is_taxi(self):
        if self.category.filter(name='Такси').exists():
            return True
        return False

    @property
    def phone(self):
        phones = [
            y.strip()
                for x in self.address.values('phone')
                    for y in x['phone'].split(',')
        ]
        if phones:
            return ', '.join(phones[:2] if len(phones) > 2 else phones)
        return None

    @property
    def has_email(self):
        return bool(self.email.strip())

    @property
    def get_url(self):
        url = self.url
        if url.endswith("/"):
            url = url[:-1]
        if "http://" in url:
            url = url.split('http://')[1]
            return url
        return url

    def dump(self):
        place_object = dict()
        for f in ['name', 'url', 'email']:
            place_object[f] = getattr(self, f, None)

        category = [{
            'id': c.id,
            'name': c.__unicode__(),
        } for c in self.category.all().order_by('name')]
        place_object['category'] = category

        tagging = [{
            'id': c.id,
            'name': c.__unicode__(),
        } for c in self.tagging.all().order_by('name')]
        place_object['tagging'] = tagging

        payments = [p.__unicode__() for p in  self.payments.filter(name__gt='')]
        if payments:
            place_object['payments'] = list(set(payments))
            place_object['payments'].sort()
        else:
            place_object['payments'] = None

        place_object['adr'] = list()
        for adr in self.address.all():
            adr_object = dict()
            adr_object['address'] = adr.address
            adr_object['phone'] = adr.phone
            adr_object['wt_list'] = [wt.dump() for wt in adr.work_time.all()]
            place_object['adr'].append(adr_object)
        return place_object

    def get_fs_photos(self, fsid):
        url = 'https://api.foursquare.com/v2/venues/%s/photos' % fsid
        data = get_json(url, FS_AUTH)
        present_photos = self.foursquare_photo.all().values_list('photo_id', flat=True)
        for k in data['response']['photos']['items']:
            if k['id'] not in present_photos:
                param = {
                    'place': self,
                    'photo_id': k['id'],
                    'prefix': k['prefix'],
                    'suffix': k['suffix'],
                }
                FoursquarePhoto(**param).save()


class RateCategories(models.Model):
    category = models.ForeignKey(PlaceCategory)
    place = models.ForeignKey(Place)
    rate = models.FloatField(max_length=10, default=1,
                            editable=False)
    num_votes = models.PositiveIntegerField(_('number of votes'),
                            default=0, editable=False)

    class Meta:
        verbose_name = _('Place rate category')
        verbose_name_plural = _('Place rate categories')
        db_table = 'place_place_rate_categories'
        auto_created = Place

    def __unicode__(self):
        return u'%s: %s in %s' % (self.rate, self.place, self.category)


class PlaceAddress(models.Model):
    place = models.ForeignKey(Place,
                    related_name='address')
    is_main_office = models.BooleanField(default=0,
                    verbose_name=_('main office'))
    address = models.CharField(verbose_name=_('address'),
                    max_length=255,
                    null=True, blank=True,)
    # geopoint is Deprecated. Use lat and lng
    geopoint = models.CharField(verbose_name=_('geo point by yandex maps'),
                    max_length=50,
                    null=True, blank=True,)
    district = models.CharField(verbose_name=_('district'),
                    max_length=12,
                    choices=settings.DISTRICT,
                    default=None,
                    blank=True, null=True)
    phone = models.CharField(verbose_name=_('phone'),
                    max_length=255,
                    null=True, blank=True,)
    email = models.EmailField(verbose_name=_('email'),
                    null=True, blank=True,)
    city = models.ForeignKey(City, verbose_name=_('city'), default=None,
                    null=True, blank=True)
    lat = models.FloatField(default=None, null=True, blank=True) # Ширина
    lng = models.FloatField(default=None, null=True, blank=True) # Долгота
    fsid = models.CharField(verbose_name=_(u'Foursquare ID'), max_length=255,\
                    default='', null=True, blank=True)


    class Meta:
        verbose_name = _('Place address')
        verbose_name_plural = _('Place addresses')

    def __unicode__(self):
        return "%s" % self.address

    @models.permalink
    def get_absolute_url(self):
        return ("control_address_form", [str(self.pk)])

    def save(self, *args, **kwargs):
        if self.is_main_office:
            #self.place.main_address = self.address
            #main_address set every time when plase save
            self.place.save()
        if self.place.address.count() == 1 and not self.is_main_office:
            self.is_main_office = True
        super(PlaceAddress, self).save(*args, **kwargs)

    def update_geo(self):
        if not self.city:
            self.city = self.place.sites.all()[0].city
        url = 'http://geocode-maps.yandex.ru/1.x/'
        params = {
            'geocode' : self.city.name.encode('utf-8')+', '+self.address.encode('utf-8'),
            'format': 'json',
        }
        data = get_json(url, params)
        pos = data['response']['GeoObjectCollection']['featureMember'][0] \
            ['GeoObject']['Point']['pos'].split(' ')
        self.lng = pos[0]
        self.lat = pos[1]
        self.save()

    def update_fsid(self):
        if not self.city or not self.lat or not self.lng:
            return False
        url = 'https://api.foursquare.com/v2/venues/search'
        params = {
            # 'query': self.place.name.encode('utf-8'),
            # 'near': self.city.name.encode('utf-8'),
            'll': '%s,%s' % (self.lat, self.lng,),
            'radius': 100,
            'intent': 'browse',
        }
        params.update(FS_AUTH)
        data = get_json(url, params)
        if len(data['response']['venues']):

            venues = data['response']['venues']
            nearest = {
                'distance': None,
                'ids' : [],
                'names' : [],
            }
            place_name = self.place.name
            print '---> %s <---' % place_name
            for v in venues:
                d = Levenshtein.distance(place_name, v['name'])
                if nearest['distance'] is None or d < nearest['distance']:
                    nearest['distance'] = d
                    nearest['ids'] = [v['id'],]
                    nearest['names'] = [v['name'],]
                elif d == nearest['distance']:
                    nearest['ids'].append(v['id'])
                    nearest['names'].append(v['name'])

            for n in nearest['names']:
                print n

            max_distance = 5
            if len(place_name) < 5:
                max_distance = len(place_name) / 2

            if len(nearest['ids']) > 1:
                # raise Exception('More ids for addr = %s (%s) in place = %s' 
                 # % (self.address, self.id, self.place.id))
                print '--- More ids. EXIT!!!'
                return
                
            if nearest['distance'] > max_distance:
                print '--- More distance. EXIT!!!'
                return

            self.fsid = nearest['ids'][0]
            self.save()
            print '+++ Set or update FSID'


class FoursquarePhoto(models.Model):
    place = models.ForeignKey(Place, related_name='foursquare_photo')
    photo_id = models.CharField(max_length=255)
    prefix = models.CharField(max_length=255)
    suffix = models.CharField(max_length=255)
    is_published = models.BooleanField(verbose_name=_('is published'),
                        default=True)

    def __unicode__(self):
        return self.photo_id

    def thumb_url(self):
        return '%s%s%s' % (self.prefix, '300x300', self.suffix)

    def original_url(self):
        return '%s%s%s' % (self.prefix, 'original', self.suffix)


class PlaceAddressWorkTime(models.Model):
    address = models.ForeignKey(PlaceAddress,
                        related_name='work_time')
    mon = models.BooleanField(default=0,
                        verbose_name=_('monday'))
    tue = models.BooleanField(default=0,
                        verbose_name=_('tuesday'))
    wed = models.BooleanField(default=0,
                        verbose_name=_('wednesday'))
    thu = models.BooleanField(default=0,
                        verbose_name=_('thursday'))
    fri = models.BooleanField(default=0,
                        verbose_name=_('friday'))
    sat = models.BooleanField(default=0,
                        verbose_name=_('saturday'))
    sun = models.BooleanField(default=0,
                        verbose_name=_('sunday'))
    from_time = models.TimeField(null=True, blank=True)
    till_time = models.TimeField(null=True, blank=True)
    all_day = models.BooleanField(default=0)
    day_off = models.BooleanField(default=0)

    class Meta:
        verbose_name = _('Place adderess work time')
        verbose_name_plural = _('Place address work times')
        ordering = ['id']

    def __unicode__(self):
        return "%s -- %s" % (self.address.__unicode__(),
                            self.address.place.__unicode__())

    def save(self, *args, **kwargs):
        # if self.all_day:
            # :(
            # self.mon =\
            # self.tue =\
            # self.wed =\
            # self.thu =\
            # self.fri =\
            # self.sat =\
            # self.sun = True

        super(PlaceAddressWorkTime, self).save(*args, **kwargs)

    def work_time(self):
        txt = u''
        insert = False
        count = False
        comma = False
        last_day = ''
        week_localy = {
            'mon': u'пн',
            'tue': u'вт',
            'wed': u'ср',
            'thu': u'чт',
            'fri': u'пт',
            'sat': u'сб',
            'sun': u'вс',
        }
        week = (
            'mon',
            'tue',
            'wed',
            'thu',
            'fri',
            'sat',
            'sun',
        )

        for day in week:
            is_checked_day = getattr(self, day)
            if is_checked_day:     # if day is work
                if not insert:
                    if comma:
                        txt = txt + u','
                    insert = True
                    txt = txt + week_localy[day]
                else:
                    if not count:
                        count = True
                    last_day = week_localy[day]

            if not is_checked_day or day == 'sun':
                if insert:
                    if count:
                        if len(last_day):
                            txt = txt + u'-' + last_day
                        count = False
                    comma = True
                insert = False

        if self.day_off:
            txt = txt + u' выходной'
        elif self.all_day:
            txt = txt + u' круглосуточно'
        else:
            if self.from_time is None: from_time = ''
	    else: from_time = self.from_time.strftime('%k:%M').strip()
            if self.till_time is None: till_time = u'до последнего клиента'
	    else: till_time = self.till_time.strftime('%k:%M').strip()
	    txt = txt + ' %s-%s' % (
                from_time,#self.from_time.strftime('%k:%M').strip(),
                till_time#self.till_time.strftime('%k:%M').strip()
            )
        return unicode(txt)


    def dump(self):
        j = dict()
        for f in self._meta.fields:
            if not f == self._meta.pk and not f.name == 'address':
                j[f.name] = getattr(self, f.name)
        return j


class PlaceGallery(models.Model):
    place = models.ForeignKey(Place,
                    related_name='gallery',
                    verbose_name=_(u'place'))
    image = ImageWithThumbnailsField(verbose_name=_(u'photo'),
                    upload_to=gen_file_name,
                    thumbnail={u'size': (300, 300), u'subdir': u'_thumb'},
                    blank=True, null=True)
    title = models.CharField(_(u'title'),
                    max_length=300,
                    blank=True, null=True)
    order = models.IntegerField(verbose_name=_('order'))

    objects = GalleryManager()

    class Meta:
        verbose_name_plural = _(u'Place galleries')

    def __unicode__(self):
        return u"%s %s" % (self.place.name, self.order)


class TempGallery(models.Model):
    gallery = models.ForeignKey(PlaceGallery,
                        related_name='temps')
    image = ImageWithThumbnailsField(upload_to=gen_file_name,
                        thumbnail={'size': (150, 150), 'subdir': '_thumb'},
                        verbose_name=_('photo'),
                        blank=True, null=True)
    time = models.DateTimeField(auto_now=True)


def recalculate_category_mean(sender, user, voted_item, **kwargs):
    if isinstance(voted_item, Place):
        for category in voted_item.category.all():
            category.category_mean = PlaceCategory.objects.\
                                                    get_category_mean(category)
            category.save()
            #update_rate_categories(category)
#updated all places in all voted_item categories


def update_rate_categories(category, **kwargs):
    for place in category.places.all():
        place_rate, created = RateCategories.objects.get_or_create(
                                                place=place, category=category)
        rate, num_votes = PlaceCategory.objects.get_place_rating(place,
                                                                    category)
        place_rate.rate = rate
        place_rate.num_votes = num_votes
        place_rate.save()
user_voted.connect(recalculate_category_mean)
