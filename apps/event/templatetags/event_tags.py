# -*- coding: utf-8 -*-
import time
import datetime

from apps.event.forms import EventForm
from django.db.models import Min, Max, Q
from django import template
from django.utils import formats
from django.utils.dateformat import format
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.conf import settings

from common import htmlcalendar
from event.utils import widget_earliest_date, earliest_date
from apps.event.models import Event, EventCategory
from apps.event.utils import get_datelist_periods, group_periods

from annoying.functions import get_object_or_None


register = template.Library()


############### INCLUSION TAGS

@register.inclusion_tag('event/tags/top_events.html')
def top_events(category, limit=5):
    """Returns template with qs of best rating events in category"""
    DEFAULT_TITLE = _('Best of %s' % category.title)
    return {
            #'top_list': top_list,
            'top_list': EventCategory.objects.get_top(category)[:limit],
            'rating_title': category.rating_title or DEFAULT_TITLE
            }

@register.inclusion_tag('event/tags/today_events.html')
def today_events(category, limit=5):
    event_list = Event.objects.today(category=category)[:limit]
    return {
        'event_list': event_list,
    }

@register.inclusion_tag('event/tags/soon_events.html')
def soon_events(category, limit=5):
    try:
        event_list = Event.objects.soon(category=category,
                add_q=Q(publish_on_main=True)).annotate(
                    start_date=Min('periods__start_date'),\
                    end_date=Max('periods__end_date'),\
                    repeat_on=Max('periods__repeat_on'),
                    repeat_every = Max('periods__repeat_every'))[:limit]
        for event in event_list:
            schedule, today = event.shedule()

            if event.repeat_on == 2:
                event.start_date = widget_earliest_date(schedule.get_start_dates)\
                                    if widget_earliest_date(schedule.get_start_dates)\
                                    else event.end_date
            if event.repeat_on == 1:
                event.start_date = widget_earliest_date(schedule.get_start_dates_daily)
        return {
            'today': datetime.datetime.today(),
            'event_list': event_list,
        }
    except:
        return ''

@register.inclusion_tag('event/tags/calendar_film.html')
def calendar_film(event):
    periods = event.periods.all()
    edges = periods.aggregate(first=Min('start_date'),
                                last=Max('end_date'))
    choice = get_datelist_periods(event)
    calendar = htmlcalendar.HTMLCalendar(choice)
    return {
        "month_html_list": calendar.formatrangemonth(edges['first'], edges['last'], choice)
    }

@register.inclusion_tag('event/tags/calendar_filter.html')
def calendar_filter():
    today = datetime.date.today()
    date = (today.year, today.month)

    choice = htmlcalendar.get_dates_in_month(*date)
    calendar = htmlcalendar.HTMLCalendar(choice, reverse('event_list'))
    html = htmlcalendar.add_navigation(
            calendar.formatmonth(*date),
            reverse('calendar_navigation'),
            *date)
    return {
        "calendar_filter": html,
    }

@register.inclusion_tag('event/tags/shedule_for_event.html')
def shedule_for_event(event, day=None):
    return {
        "day": day,
        "grouped_periods": group_periods(event, day, 'place'),
    }

@register.inclusion_tag('event/tags/shedule_for_place.html')
def shedule_for_place(place, day=None):
    return {
        "day": day,
        "grouped_periods": group_periods(place, day, 'event'),
    }

@register.inclusion_tag('event/tags/extra_info.html')
def extra_info(event):
    shedule, today = event.shedule()
    place = shedule.place if shedule else None
    if not shedule:
        start = None
    else:
        if event.category_id in (23, 24, 26, 27):
            #place, start time
            start = shedule.first_time if today else earliest_date(shedule.get_start_dates)
        elif event.category_id in (25,):
            #place
            start = earliest_date(shedule.get_start_dates)
        else:
            place = None
            if shedule:
                start = (shedule.has_repeat or earliest_date(shedule.get_start_dates)) if not today else None
            else:
                start = None
    if event.category_id in (14, ):
        has_repeat = True
    else:
        has_repeat = event.has_several_occurrences() if start else False
    return {
        "place": place,
        "start": start,
        "has_repeat": has_repeat,
    }

@register.simple_tag
def info_sport(event):
    # sport, klubyi, spektakli, kontsertyi
    try:
        shedule, today = event.shedule()
        data = {
            "place": shedule.place,
            "start_date": earliest_date(shedule.get_start_dates) if not today else None,
            "start_time": shedule.first_time,
        }
        return render_to_string('event/tags/extra/info_sport.html', data)

    except:
        return ''

@register.inclusion_tag('event/tags/extra/info_exposure.html')
def info_exposure(event):
    one_time = event.has_several_occurrences() < 2
    shedule, today = event.shedule()
    if not shedule:
        return {}
    return {
        "one_time": one_time,
        "place": shedule.place,
        "start_date": earliest_date(shedule.get_start_dates),
        "end_date": shedule.end_date,
    }

@register.inclusion_tag('event/tags/extra/info_movie.html')
def info_movie(event):
    shedule, today = event.shedule()
    one_time = event.has_several_occurrences() < 2
    if one_time:
        place = None
        start_time = None
        if shedule:
            start_date = earliest_date(shedule.get_start_dates)
        else:
            start_date = None
    else:
        place = shedule.place
        start_time = shedule.first_time
        start_date = earliest_date(shedule.get_start_dates)
    if today and one_time:
        place = start_time = start_date = None
    return {
        "one_time": one_time,
        "today": today,
        "place": place,
        "start_time": start_time,
        "start_date": start_date,
    }

@register.inclusion_tag('event/tags/events_random.html', takes_context=True)
def events_random(context, qs, today=True):
    context.update({
        "today": bool(today),
        "events": qs,
        'STATIC_URL': settings.STATIC_URL,
    })
    return context

@register.inclusion_tag('event/tags/dummy.html', takes_context=True)
def display_event_categories(context, template='event/tags/event_categories.html'):
    """Return links to event categories"""
    """
    if cache.has_key('categories'):
        categories = cache.get('categories')
    else:
        categories = EventCategory.objects.select_related().all().order_by("order")
        cache.set('categories', categories, 500)
    """
    categories = EventCategory.objects.select_related().all().order_by("order")
    request = context['request']
    path = request.path.strip('/').split('/')
    path = tuple(path[-3:])
    if len(path) != 3:
        path = (None,None,None)
    try:
        tt = time.strptime('%s-%s-%s' % path,
                           '%s-%s-%s' % ('%Y', '%m', '%d'))
        date = datetime.date(*tt[:3])
    except ValueError:
        date = None

    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    context.update({'template': template,
            'categories': categories,
            'day': date,
            'today': today,
            'tomorrow': tomorrow,
            })
    return context

@register.inclusion_tag('event/tags/dummy.html', takes_context=True)
def display_tabs(context, event, user, is_subscribed, messages, template='event/tags/tabs_for_event.html'):
    """Return template with tabs  for event"""
    event =  get_object_or_None(
                    Event.objects.annotate(
                        start=Min('periods__start_date')), id=event.id)
    start_day = datetime.date.today()
    end_day = start_day + datetime.timedelta(days=6)
    datelist = get_datelist_periods(event, start_day, end_day)
    form = EventForm(instance=event)

    context.update({
        'template': template,
        'datelist' : datelist,
        'event' : event,
        'user' : user,
        'is_subscribed' : is_subscribed,
        'messages' : messages,
        'REQUEST_PATH': context['REQUEST_PATH'],
        'form':form
    })
    return context

@register.inclusion_tag('event/tags/calendar_week.html')
def dispay_week_calendar(category=None):
    slug = category.slug if isinstance(category, EventCategory) else 'all'
    days = []
    for date in htmlcalendar.get_dates_in_week():
        day = date.day
        url = reverse('event_all_on_day', args = (slug, date.year, date.month, day))
        days.append({
            'day': day,
            'weekday': htmlcalendar.old_calendar.day_abbr[date.weekday()],
            'holidays': date.weekday() in (5, 6),
            'url': url,
        })
    return {
        "days": days
    }

def concate_kh_seances(occurence, kh_seances, day):
    try:
        if not occurence.start_times:
            # return occurence
            return []
        if not day:
            day = datetime.date.today()
        start_times = []
        for st in occurence.start_times:
            work_day = day
            dt = datetime.datetime(work_day.year, work_day.month, work_day.day, st.hour, st.minute)
            if dt in kh_seances:
                kh_seance_id = kh_seances[dt].seance_id
            else:
                kh_seance_id = None
            start_times.append({
                'time': st,
                'kh_seance_id': kh_seance_id,
            })
        # occurence.start_times = start_times
        # return occurence
        return start_times
    except:
        return []

def time_list_sort(st):
    ret = '{:%H%M}'.format(st['time'])
    if st['time'].hour <= settings.HOUR_CHANGE_DATES:
        ret = '111'+ret
    return int(ret)

@register.simple_tag
def display_times_list(obj, day):
    kh_seances = obj['kh_seances']
    # print ''
    # print '='*40
    # print obj
    # print obj['list']
    # print ''
    # print kh_seances
    # print '-'*40
    times_list = []
    for i in [concate_kh_seances(l, kh_seances, day) for l in obj['list']]:
        for ii in i:
            times_list.append(ii)
    times_list.sort(key=time_list_sort)

    data = {
        'times_list': times_list,
        'day': day,
    }
    return render_to_string('event/tags/time_list.html', data)


############### FILTERS
@register.filter
def lttoday(date):
    return date < datetime.date.today()

@register.filter
def lttime(ts, day=None):
    day = day or datetime.datetime.now()
    now = datetime.datetime.now()
    cur_day = day.day

    ts = datetime.datetime(year=day.year, month=day.month,\
                            day=cur_day, hour=ts.hour, minute=ts.minute)
    if ts.hour < settings.HOUR_CHANGE_DATES:
        ts = ts + datetime.timedelta(days=1)

    return ts < now

@register.filter
def lttimekinohod(ts, day=None):
    day = day or datetime.datetime.now()
    now = datetime.datetime.now()
    cur_day = day.day

    ts = datetime.datetime(year=day.year, month=day.month,\
        day=cur_day, hour=ts.hour, minute=ts.minute)
    if ts.hour < settings.HOUR_CHANGE_DATES:
        ts = ts + datetime.timedelta(days=1)
    ts = ts + datetime.timedelta(minutes=-30)

    return ts < now

@register.filter
def istoday(date):
    return date == datetime.date.today()

@register.filter
def old(date):
    return False\
            if not date\
            else date < datetime.date.today()

@register.filter
def istime(date):
    return isinstance(date, datetime.time)

@register.filter
def as_text(field, name):
    if not field or not field.value():
        return ''
    try:
        data = eval(field.value())
    except TypeError:
        return ''
    try:
        return data[name]
    except KeyError:
        return ''

@register.filter
def get_time_for_event(period, day=None):
    return sorted([ts for ts in period.start_times])

@register.filter
def check_event(periods, day=None):
    day = day or datetime.datetime.today()
    return [p for p in periods if day in p.get_start_dates]

@register.filter
def get_time(periods, day=None):
    day = day or datetime.datetime.today()
    """
    return sorted(
        [ts for period in periods\
        if period.start_times and period.has_repeat_on_day(day)\
        for ts in period.start_times])
    """
    return [ts for period in periods\
            if period.start_times and period.has_repeat_on_day(day)\
            for ts in period.start_times]

@register.filter
def get_date(value, arg='j F Y'):
    now_year = datetime.date.today().year
    if not value:
        return ''
    event_year = value.year
    if now_year == event_year:
        arg = 'j F'
    if not value:
        return u''
    try:
        return formats.date_format(value, arg)
    except AttributeError:
        try:
            return format(value, arg)
        except AttributeError:
            return ''
