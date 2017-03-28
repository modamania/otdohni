# -*- coding: utf-8 -*-
import datetime

from django.contrib.sites.models import Site
from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned

from event.models import Event, EventCategory, Occurrence
from event.utils import group_periods
from place.models import Place
from place.utils import get_events_datelist

from kinohod.api import get_schedules, get_movie_id, get_city_schedule, get_image
from kinohod.models import KinohodSeance


class KinohodUtils(object):
    city_id = None
    site_id = None
    def __init__(self):
        self.movie_category = EventCategory.objects.get(slug='kino')
        self.place_list = Place.default_manager.filter(kinohod_place_id__gt=0)


    def commit_schedule(self, event, place, schedule):
        s_id = int(schedule['id'])
        data = {
            'event': event,
            'place': place,
        }
        dt = datetime.datetime.strptime(schedule['startTime'].split('+')[0], \
             '%Y-%m-%dT%H:%M:%S')
        if dt.hour < settings.HOUR_CHANGE_DATES:
            dt = dt - datetime.timedelta(days=1)
        if place.can_buy_tiket:
            try:
                kinohod_seance = KinohodSeance.objects.get(seance_id=s_id)
            except KinohodSeance.DoesNotExist:
                kinohod_seance = KinohodSeance(seance_id=s_id)
            kinohod_seance.event = event
            kinohod_seance.place = place
            kinohod_seance.seance_id = s_id
            kinohod_seance.dt = dt
            kinohod_seance.save()

        data.update({
                    'hide_for_editing' : True,
                    'start_date': dt,
                    'start_times': dt.strftime('%H:%M;,'),
                    })
        occurrence, is_create = Occurrence.default_manager.get_or_create(**data)
        if is_create:
            occurrence.sites = place.sites.all()
        return occurrence

    def remove_stupid_occurance(self, ids):
        # Удаляем из нашей БД сеансы от кинохода которые в будущем,
        # но о них информация не подтвердилась от кинохода
        today = datetime.date.today()
        now = datetime.datetime.now()
        now = datetime.time(now.hour, now.minute)
        for o in Occurrence.default_manager.filter(id__in=ids):
            if o.start_date > today:
                o.delete()
            elif o.start_date == today and o.start_times[0] > now:
                o.delete()


    def fill_schedules(self, event, movie_id):
        for day_delta in xrange(7):
            dt = datetime.date.today() + datetime.timedelta(days=day_delta)
            schedules = get_schedules(movie_id, self.city_id, date=dt.strftime('%d%m%Y'))
            for s in schedules:
                try:
                    place = Place.default_manager.get(kinohod_place_id=s['cinema']['id'])
                except Place.DoesNotExist:
                    pass
                else:
                    o_list = set(Occurrence.default_manager.filter(place=place, event=event, start_date=dt, hide_for_editing=True).values_list('id', flat=True))
                    for schedule in s['schedules']:
                        o = self.commit_schedule(event, place, schedule)
                        if o.id in o_list:
                            o_list.remove(o.id)
                    self.remove_stupid_occurance(o_list)



    def get_or_create_event(self, data):
        try:
            filter = {
                'title' : data['title'],
                # 'original_title' : data['originalTitle'],
                'category' : self.movie_category,
            }
            return Event.default_manager.get_or_create(**filter)
        except MultipleObjectsReturned:
            filter = {
                'title' : data['title'],
                'original_title' : data['originalTitle'],
                'category' : self.movie_category,
            }
            return Event.default_manager.get_or_create(**filter)



    def commit_event(self, data):
        # site = Site.objects.get(id=self.site_id)
        try:
            event, is_create = self.get_or_create_event(data)
        except MultipleObjectsReturned:
            return None
        else:
            event.sites.add(self.site_id)
            if not event.intro:
                event.intro = data['annotationShort']
            if not event.description:
                event.description = data['annotationFull']
            if not event.original_title:
                event.original_title = data['originalTitle']
            if not event.genre:
                event.genre =  ', '.join(data['genres'])
            if not event.image:
                if data['images']:
                    image = get_image(data['images'][0])
                else:
                    image = get_image(data['poster'])
                if image:
                    event.image = image
            event.kinohod_id = data['id']
            event.save()
            return event, is_create


    def update_city(self):
        today = datetime.date.today()
        KinohodSeance.objects.filter(dt__lt=today).delete()
        Occurrence.default_manager.filter(start_date__lt=today, hide_for_editing=True).delete()
        for city in settings.KINOHOD_CITY_IDS:
            self.city_id = city['city_id']
            self.site_id = city['site_id']
            data = get_city_schedule(self.city_id)
            for d in data:
                event, event_is_create = self.commit_event(d)
                if event:
                    self.fill_schedules(event, d['id'])
                    if event_is_create:
                        event.start_date = event.get_start_date()
                        event.save()
