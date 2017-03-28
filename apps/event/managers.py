from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager

from annoying.functions import get_object_or_None

from rating.models import Vote

from event.utils import exclude
from core.utils import method_cache

import datetime

class OccurrenceManager(CurrentSiteManager):

    use_for_related_fields = True

    @exclude('event__is_published', False)
    def active(self):
        today = datetime.date.today()
        return self.filter(
            models.Q(
                start_date = today,
                repeat_on = 0,
            ) |
            models.Q(
                end_date__gte=today,
            ) |
            models.Q(
                end_date__isnull=True,
                repeat_on__in=[1,2,],
            )
        ).order_by('start_date')

    @exclude('event__is_published', False)
    def soon(self):
        today = datetime.date.today()
        return self.filter(
            start_date__gt=today
        ).order_by('start_date')

    @exclude('event__is_published', False)
    def daily_occurrences(self, dt=None, event=None, category=None):
        '''
        Returns a queryset of for instances that have any overlap with a
        particular day.

        * ``dt`` may be either a datetime.datetime, datetime.date object, or
          ``None``. If ``None``, default to the current day.

        * ``event`` can be an ``Event`` instance for further filtering.
        '''
        dt = dt or datetime.datetime.now()
        start = datetime.datetime(dt.year, dt.month, dt.day)
        end = start.replace(hour=23, minute=59, second=59)
        qs = self.select_related().filter(
            models.Q(
                start_date__gte=start,
                start_date__lte=end,
            ) |
            models.Q(
                end_date__gte=start,
                end_date__lte=end,
                repeat_on__in=[1,2]
            ) |
            models.Q(
                start_date__lt=start,
                end_date__gt=end,
                repeat_on__in=[1,2]
            ) |
            models.Q(
                end_date__isnull=True,
                start_date__lte=start,
                repeat_on__in=[1,2]
            )
        ).order_by('place')
        for period in qs.filter(repeat_on__in=[1,2]):
            try:
                if not period.has_repeat_on_day(dt):
                    qs = qs.exclude(id=period.id)
            except AttributeError:
                continue

        if event:
            qs = qs.filter(event=event)
        return qs.filter(event__category=category) if category else qs

    @exclude('event__is_published', False)
    def week_occurrences(self, dt=None, event=None, category=None):
        '''
        Returns a queryset of for instances that have any overlap with a
        particular week.

        * ``dt`` may be either a datetime.datetime, datetime.date object, or
          ``None``. If ``None``, default to the current day.

        * ``event`` can be an ``Event`` instance for further filtering.

        * ``category`` can be an ``EventCategory`` instance for filtering.
        '''
        dt = dt or datetime.datetime.now()
        start = datetime.datetime(dt.year, dt.month, dt.day)
        end = start + datetime.timedelta(days=6)
        end = end.replace(hour=23, minute=59, second=59)
        qs = self.select_related().filter(
            models.Q(
                start_date__gte=start,
                start_date__lte=end,
            ) |
            models.Q(
                end_date__gte=start,
                end_date__lte=end,
            ) |
            models.Q(
                start_date__lt=start,
                end_date__gt=end
            )
        ).order_by('place')

        qs = qs.filter(event=event) if event else qs
        qs = qs.filter(event__category=category) if category else qs
        return qs


class CategoryManager(models.Manager):

    def get_top(self, category):
        events= category.events.filter(num_votes__gte=settings.CHART_VOTE_MIN, is_published=1).order_by('-rate')
        today = datetime.date.today()
        events= events.select_related().filter(
            models.Q(
                periods__start_date__gte=today,
            ) |
            models.Q(
                periods__start_date__lt=today,
                periods__end_date__gte=today,
                periods__repeat_on__gt=0,
            ) |
            models.Q(
                periods__start_date__lt=today,
                periods__end_date__isnull=True,
                periods__repeat_on__gt=0,
            )).distinct()

        return events

    def get_category_mean(self, category):
        events = category.events.all()
        total_score = 0
        total_items = 0
        for event in events:
            rated_obj = Vote.objects.get_score(event)
            total_score += rated_obj['score']
            if rated_obj['num_votes']:
                total_items += 1
        try:
            mean = total_score / total_items
        except ZeroDivisionError:
            return 1
        return '%.2f' % mean

    def get_event_rating(self, event, category):
        rated_object = Vote.objects.get_score(event)
        num_votes = float(rated_object['num_votes'])
        score = float(rated_object['score'])
        vote_min = float(settings.CHART_VOTE_MIN)

        #calculated self rating for all place categories
        category_mean = float(category.category_mean)
        rate_event = (num_votes/(num_votes+vote_min))*score+(vote_min/(num_votes+vote_min))*category_mean
        return ('%.2f' % rate_event, int(num_votes))


    def active_today(self, **kwargs):
        from event.models import TodayEvent
        event_ids = set(TodayEvent.on_site.all().values_list('event', flat=True))
        qs = self.filter(events__in=event_ids).distinct()
        return qs


    # @method_cache(60 * 5)
    def active_soon(self, id=None):
        from event.models import SoonEvent
        event_ids = set(SoonEvent.on_site.all().values_list('event', flat=True))
        qs = self.select_related().filter(events__in=event_ids).distinct()
        return qs

