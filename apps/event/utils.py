# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_noop as _
from django.db.models import Q
from django.conf import settings

import datetime
import itertools


def to_datetime(dt=None, infinite=False):
    if not dt:
        dt = datetime.datetime(2099, 1, 1)\
            if infinite\
            else datetime.datetime.today()
    if isinstance(dt, datetime.datetime):
        dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        dt = datetime.datetime(dt.year, dt.month, dt.day)
    return dt

def get_datelist_periods(event, start=None, end=None):
    """ Return list of dates in which there is an event
    """
    periods = event.periods.all()
    dates = []
    for period in periods:
        if start and start >= period.start_date:
            start_date = start
        else:
            start_date = period.start_date

        if end and end <= to_datetime(period.end_date, True).date():
            end_date = end
        else:
            end_date = period.end_date

        for date in period.get_start_dates:
            if isinstance(date, datetime.datetime):
                date = date.date()
            if start_date <= date <= end_date:
                dates.append(date)
            elif date > end_date:
                break
    datelist = list(set(dates))
    datelist.sort()
    return datelist

def format_date_or_time(start, end=None):
    today = datetime.date.today()
    if isinstance(start, datetime.time):
        return start.strftime("%H:%M")

    if end and not start == end:
        pattern_end = "по %d %B" if today.year == start.year else "по %d %B %y"
    else:
        pattern_end = ""
    pattern = "с %d %B {0}".format(pattern_end)
    return start.strftime(pattern)

def has_admin_perm(user):
    if not user.is_authenticated()\
            or not (user.is_superuser or\
                    user.profile.access_to_dasboard):
        return False
    return True

def obj_by_perm(model, user, **kwargs):
    if not has_admin_perm(user):
        q = Q(is_published=True)
    else:
        q = Q()
    return model.objects.filter(Q(**kwargs), q)

def widget_earliest_date(date_list):
    today = datetime.datetime.today()
    delta_list = [(date, today-date) for date in date_list]
    delta_list.sort(key=lambda date: abs(date[1].days))

    for date in delta_list:
        if date[0] > today:
            result_date = date[0]
            return result_date
    return 0

def earliest_date(date_list):
    today = datetime.datetime.today()
    delta_list = [(date, today-date) for date in date_list]
    delta_list.sort(key=lambda date: abs(date[1].days))
    try:
        return delta_list[0][0]
    except IndexError:
        return None

def exclude(field, value=True):
    def wrap_method(func):
        def wrap(*args, **kwargs):
            if "DISABLE_EXCLUDE" in kwargs:
                exclude = kwargs.pop('DISABLE_EXCLUDE')
            else:
                exclude = False
            input = func(*args, **kwargs)
            if exclude:
                return input.exclude(**{field: value})
            return input
        return wrap
    return wrap_method


#@func_cache(60 * 15)
def group_periods(obj, day=None, attr='event'):
    day = day or datetime.date.today()
    l = dict()
    for x in obj.periods.daily_occurrences(
                dt=day, DISABLE_EXCLUDE=False
            ).order_by(attr):
        key = getattr(x, attr)
        if not key in l:
            l[key] = []
        l[key].append(x)

    gp = [{
        'grouper': x, 'list': y
    } for x, y in l.items()]

    for g in gp:
        f = {
            attr: g['grouper']
        }
        kh_seances = obj.kh_seances.filter(**f)
        g['kh_seances'] = {s.dt: s for s in kh_seances}

    return gp