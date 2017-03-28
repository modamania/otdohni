#-*- coding: utf-8 -*-
import re
import datetime
from random import sample

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models.aggregates import Min
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager

from djangosphinx.models import SphinxSearch
from threadedcomments.models import  ThreadedComment
from fields import TimelistField
from dateutil.rrule import rrule, DAILY, WEEKLY, weekdays
from dateutil.relativedelta import relativedelta

from tinymce import models as tinymce_models
from place.models import Place
from rating.signals import user_voted
from common.models import WithPublished, WithSite
from taggit.managers import TaggableManager
from core.utils import method_cache

from managers import CategoryManager, OccurrenceManager
from utils import to_datetime


EVENT_DIR = getattr(settings, 'EVENT_DIR', 'events')


EMBED_VIDEO_OBJECT = """<iframe width="%s" height="%s" src="//%s?rel=0" frameborder="0" allowfullscreen></iframe>
"""

VIDEO_URL_PATTERN = re.compile(r'^http://([w]{3}\.)?(youtube.com|vimeo.com)(/watch?/v=|/v/)([-a-z0-9A-Z_]+)')

def make_upload_path(instance, filename):
    """Generates upload path for FileField"""
    return u'%s/%s/%s' % (EVENT_DIR,
                        instance.category.slug, filename)


class EventCategory(models.Model):
    sites = models.ManyToManyField(Site,
                            related_name='events',
                            blank=True, null=True)
    title = models.CharField(_('title'), max_length=80)
    slug = models.SlugField(_('slug'),unique=True)
    category_mean = models.FloatField(_('category mean rate'),
                            default=1.0,
                            editable=False,
                            blank=True,
                            null=True)
    rating_title = models.CharField(max_length=80, blank=True,
                            null=True,verbose_name=_('top rating title'))
    order = models.IntegerField()

    objects = CategoryManager()


    class Meta:
        verbose_name = _('event category')
        verbose_name_plural = _('event categories')
        ordering = ['order']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event_category_list', args=[self.slug])

class EventManager(CurrentSiteManager):

    #@method_cache(60 * 15)
    def on_day_ids(self, dt=None, category=None, add_q=None, site_id=settings.SITE_ID):
        add_q = add_q or models.Q()
        dt = dt or datetime.datetime.now()
        start = datetime.datetime(dt.year, dt.month, dt.day)
        end = start.replace(hour=23, minute=59, second=59)

        if not site_id is None:
            filter = {
                'sites': site_id,
            }
        else:
            filter = {}
        pr = set(Occurrence.default_manager.values_list('event_id', flat=True).filter(
            models.Q(
                event__is_published=True,
            ) ,
            models.Q(
                start_date__gte=start,
                start_date__lte=end,
            ) |
            models.Q(
                end_date__gte=start,
                end_date__lte=end,
            ) |
            models.Q(
                start_date__lte=start,
                end_date__gte=end
            ) |
            models.Q(
                end_date__isnull=True,
                start_date__lte=start
            ) ,
            # additional q-object
            add_q,
            **filter
        ))
        if category:
            pr = set(self.filter(id__in=pr, category=category).values_list('id', flat=True))

        periods = Occurrence.objects.select_related('event').filter(event__in=pr)

        l = dict()
        for p in periods:
            if not p.event.pk in l:
                l[p.event.pk] = []
            l[p.event.pk].append(True if p.has_repeat_on_day(dt) else False)

        pr = list(pr - set([x for x, y in l.items() if not any(y)]))
        return pr

    def on_day(self, dt=None, category=None, add_q=None):
        pr = self.on_day_ids(dt, category, add_q)
        qs = self.select_related().filter(id__in=pr).distinct().order_by('category', 'title')
        return qs


    #@method_cache(60 * 15)
    def today(self, *args, **kwargs):
        ids = set(TodayEvent.on_site.all().values_list('event', flat=True))
        return Event.objects.filter(id__in=ids, **kwargs)


    def random_today(self, category):
        return self.today(category=category, publish_on_main=True).order_by('?')[:4]


    #@method_cache(60 * 15)
    def on_week(self, category=None):
        today = datetime.date.today()
        datelist = [today + datetime.timedelta(days=x) for x in range(0,7)]
        result = []
        for d  in datelist:
            f = self.on_day(d, category)
            if f:
                result.append({'date': d,"events" : list(f)})

        return result

    #@method_cache(60 * 15)
    def soon_ids(self, category=None, add_q=None, site_id=settings.SITE_ID):
        add_q = add_q or models.Q()
        today = datetime.date.today()
        earlier_3month = today + relativedelta(months=-3)
        #print earlier_3month

        not_fit_instances = self.filter(
            models.Q(
                periods__start_date__gt=earlier_3month
            ),
            models.Q(
                periods__start_date__lt=today
            )
        )
        if category:
            not_fit_instances = not_fit_instances.filter(category=category)

        if not site_id is None:
            filter = {
                'sites': site_id,
            }
        else:
            filter = {}
        qs = self.select_related().filter(
            models.Q(
                is_published=True,
                periods__start_date__gt=today,
            ) ,
            models.Q(
                periods__end_date__gt=today,
            ) |
            models.Q(
                periods__end_date__isnull=True,
            ) ,
            ~models.Q(id__in=set(o.id for o in not_fit_instances)),
            # additional q-object
            add_q,
            **filter
        ).distinct()

        if category:
            qs = qs.filter(category=category)
            if category.id == 14:
                qs = qs.filter(periods__start_date__gt=today)
        return qs.exclude(periods__start_date__lte=today).order_by('periods__start_date')

    def soon(self, *args, **kwargs):
        ids = set(SoonEvent.on_site.all().values_list('event', flat=True))
        return Event.objects.filter(id__in=ids, **kwargs)


    def random_soon(self, category):
        return self.soon(category=category, publish_on_main=True).order_by('?')[:4]


class Event(WithPublished, WithSite):
    title = models.CharField(_('title'), max_length=300)
    original_title = models.CharField(_('origin title'), max_length=300, null=True, blank=True)
    category = models.ForeignKey(EventCategory, related_name='events',
                            verbose_name=_('category'))
    image = models.ImageField(_('image'),
                            upload_to=make_upload_path,
                            null=True,
                            blank=True)
    genre = TaggableManager(blank=True, verbose_name=_('genres'))
    place = models.ManyToManyField(Place, through='Occurrence',
                            related_name='events',
                            verbose_name=_('place'))
    description = tinymce_models.HTMLField(_('description'), default='')
    additional = models.TextField(_('Additional Field'),
                            blank=True,
                            null=True)
    intro = models.TextField(_('intro'), blank=True, null=True)
    trailer = models.URLField(
        _('video URL'),
        help_text=_('Put the URL of the YouTube video. Example: '
                    'http://www.youtube.com/watch?v=wuzgCwKElm4 '
                    'or http://vimeo.com/3465465'),
        blank=True,
        null=True
    )
    rate = models.FloatField(max_length=10,default=1,
                            editable=False)
    num_votes = models.PositiveIntegerField(_('number of votes'),
                            default=0, editable=False)
    members = models.ManyToManyField(User, related_name='events',
                            blank=True,
                            null=True)
    num_comments = models.PositiveIntegerField(_('number of comments'),
                            default=0)
    publish_on_main = models.BooleanField(_('event publish on the main page'),
                            default=True)

    start_date = models.DateField(_('start date for displaying'), default=None,
                            blank=True, null=True)
    start_time = models.TimeField(_('start time for displaying'), default=None,
                            blank=True, null=True)

    kinohod_id = models.IntegerField(_('Kinohod id movie'), default=0)

    search = SphinxSearch(
        index='event_index',
        weights={
            'title': 100,
        },
        mode='SPH_MATCH_ALL',
        rankmode='SPH_RANK_NONE',
    )

    objects = EventManager()
    default_manager = models.Manager()

    class Meta:
        ordering = ['title', 'category', 'id']
        verbose_name = _('event')
        verbose_name_plural = _('events')

    def save(self, *args, **kwargs):
        super(Event, self).save(*args, **kwargs)
        if not self.sites.exists():
            self.sites.add(Site.objects.get_current())
        self.start_date = self.get_start_date()
        self.save_base()
        super(Event, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    @property
    def get_video_id(self):
        if not self.trailer:
            return None
        match = re.match(VIDEO_URL_PATTERN, self.trailer)
#        print self.trailer
        if match :
            if 'vimeo' in match.groups()[1]:
                return 'www.' + match.groups()[1] + '/moogaloop.swf?clip_id=' + match.groups()[3]
            if 'youtube' in match.groups()[1]:
#                print 'www.' + match.groups()[1] + '/v/' + match.groups()[3] + '&fs=1'
                return 'www.' + match.groups()[1] + '/v/' + match.groups()[3]
        return None

    def get_thumbnail_url(self):
        return 'http://i.ytimg.com/vi/%s/default.jpg' % self.get_video_id()

    def get_start_date(self):
        periods = self.periods.all()
        if periods:
            return periods[0].start_date
        return None

    @property
    def get_embed_video_object(self):
        video_id = self.get_video_id
        if video_id:
            return EMBED_VIDEO_OBJECT % ('100%', '100%', video_id)
        else:
            return None

    @property
    def is_movie(self):
        if self.category.id == 14:
            return True
        else:
            return False

    @property
    def has_movie(self):
        if self.is_movie and self.trailer:
            return True
        return False

    @property
    def is_exposure(self):
        return self.category.id == 25

    @property
    def is_sport(self):
        return self.category.id in (23, 24, 26, 27, 28)

    @property
    def has_passed(self):
        today = datetime.date.today()
        date = self.periods.aggregate(end=models.Max('end_date'))
        if date['end'] < today:
            return True
        return False


    @property
    def is_soon(self):
        today = datetime.date.today()
        try:
            if self.soon_flag:
                return True
        except SoonEvent.DoesNotExist:
            pass

        try:
            start_date = self.periods.all().order_by('start_date')[0]
            if  start_date.start_date > today:
                return True
        except IndexError:
            pass

        return False

    def get_absolute_url(self):
        return reverse('event_detail', args=[self.category.slug, self.id])

    def has_recurring_occurrences(self):
        return self.periods.exclude(repeat_on=0).exists()

    def has_several_occurrences(self):
        return self.periods.all().count() > 1 or self.has_recurring_occurrences()

    def is_today(self):
        return any((period.has_repeat_on_day() for period in self.periods.active()))

    def shedule(self, today=None):
        today = today or self.is_today()
        try:
            if today:
                period = self.periods.daily_occurrences()[0]
            else:
                period = self.periods.soon()[0]
        except IndexError:
            try:
                period = self.periods.order_by('-end_date')[0]
            except IndexError:
                period = self.periods.none()
        return (period, today)


class TodayEvent(WithSite):
    event = models.OneToOneField(Event, related_name='today_flag')
    default_manager = models.Manager()


class SoonEvent(WithSite):
    event = models.OneToOneField(Event, related_name='soon_flag')
    default_manager = models.Manager()


class Occurrence(WithSite):

    NOREPEAT, DAILY, WEEKLY = range(0,3)
    MO, TU, WE, TH, FR, SA, SU = range(0,7)

    REPEAT_ON_CHOICES = (
        (NOREPEAT, _('No repeat')),
        (DAILY, _('Daily')),
        (WEEKLY, _('Weekly')),
    )

    CHOICES_WEEKDAY = (
        (MO, _('Mo')),
        (TU, _('Tu')),
        (WE, _('We')),
        (TH, _('Th')),
        (FR, _('Fr')),
        (SA, _('Sa')),
        (SU, _('Su'))
    )
    event = models.ForeignKey(Event, related_name='periods',
                                verbose_name=_('Event'))
    place = models.ForeignKey(Place, related_name='periods',
                                verbose_name=_('place'))
    start_date = models.DateField(_('date start event'))
    start_times = TimelistField(verbose_name=_('start times'),
                                blank=True,
                                null=True)
    repeat_on = models.IntegerField(choices=REPEAT_ON_CHOICES,
                                default=NOREPEAT)
    repeat_every = models.IntegerField(_('Repeat every'),
                                blank=True,
                                null=True,
                                default=1)
    repeat_weekday = models.CommaSeparatedIntegerField(_('on weekday'),
                                max_length=20,
                                blank=True,
                                null=True)
    end_date = models.DateField(_('date end event'),
                                blank=True,
                                null=True)
    repeat_number = models.IntegerField(_('maximum number of repeats'),
                                blank=True,
                                null=True)
    hide_for_editing = models.BooleanField(_('No show in admin and control interface'),
                                default=False)

    objects = OccurrenceManager()
    default_manager = models.Manager()

    class Meta:
        verbose_name = _('occurrence')
        verbose_name_plural = _('occurrencies')
        ordering = ['start_date']

    def __unicode__(self):
        msg = u'%s - %s' % (self.place, self.event)
        if self.has_repeat:
            msg = msg + ". Repeat: %s" % str((self.repeat_every or self.repeat_on))
        return msg

    def _get_repeats(self):
        end_date = self.end_date if self.end_date\
                                else datetime.date(datetime.date.today().year+1, 1, 1)
        count = None if self.repeat_number == 1 else self.repeat_number
        if self.repeat_on == self.DAILY:
            return rrule(DAILY,
                         dtstart=self.start_date,
                         interval=self.repeat_every,
                         count=count,
                         until=end_date)
        elif self.repeat_on == self.WEEKLY:
            byweekdays = [y for x, y in enumerate(weekdays)\
                            if x in [int(i) for i in self.repeat_weekday.split(',')]]
            return rrule(WEEKLY,
                        dtstart=self.start_date,
                        until=end_date,
                        byweekday=byweekdays,
                        count=count,
                        interval=self.repeat_every)
        elif self.repeat_on == self.NOREPEAT:
            return None

    @property
    def get_start_dates(self):
        # TODO: movie to _get_repeats
        if self.has_repeat:
            return self._get_repeats()
        return (to_datetime(self.start_date),)

    @property
    def get_start_dates_daily(self):

        end_date = self.end_date if self.end_date\
            else datetime.date(datetime.date.today().year+1, 1, 1)

        if self.repeat_on == self.DAILY:
            return rrule(DAILY,
                dtstart=self.start_date,
                interval=self.repeat_every,
                until=end_date)
        return (to_datetime(self.start_date),)

    @property
    def has_repeat(self):
        return self.repeat_on in (self.WEEKLY, self.DAILY)

    @property
    def first_time(self):
        st = self.start_times
        if st:
            return min(st)
        return None

    def has_repeat_on_day(self, dt=None):
        return to_datetime(dt) in self.get_start_dates


#recalcilated category rating mean value
def recalculate_category_mean(sender, user, voted_item, **kwargs):
    if isinstance(voted_item, Event):
        voted_item.category.category_mean = EventCategory.objects.get_category_mean(voted_item.category)
        voted_item.category.save()
        #update_rate_categories(voted_item.category)

#updated all events in all voted_item categories
def update_rate_categories(category, **kwargs):
    for event in category.events.all():
        rate, num_votes = EventCategory.objects.get_event_rating(event,category)
        event.rate = rate
        event.num_votes = num_votes
        event.save()

user_voted.connect(recalculate_category_mean)
