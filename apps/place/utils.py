# -*- coding: utf-8 -*-
from django.conf import settings
from django.template.context import RequestContext
from django.shortcuts import render_to_response

from annoying.decorators import wraps

from core.utils import md5
from event.utils import to_datetime

from os.path import join as os_path_join
from datetime import datetime


def gen_file_name(instance, filename):
    ext_filename = filename.split('.')[1]
    if ext_filename == u'jpeg':
        ext_filename = 'jpg'
    sub_dir = instance.__class__.__name__.lower()
    filename = str(instance.pk) + '_' + md5(filename + str(datetime.now())) + \
        '.' + ext_filename
    return os_path_join(sub_dir, filename)


def multiply_symbol(x):
    if x < 57:
        return x * 1000
    if x >= 97 and x <= 122:
        return x * 100
    else:
        if x == 1105:
            x = 1077
        return x


def sort_by_name(x, y):
    name_x = x.name.lower().strip()
    name_y = y.name.lower().strip()
    length_x = len(name_x) - 1
    length_y = len(name_y) - 1
    if length_x < length_y:
        length = length_x
    else:
        length = length_y

    pos = 0
    while (pos < length and name_x[pos] == name_y[pos]):
        pos = pos + 1

    index_x = multiply_symbol(ord(name_x[pos]))
    index_y = multiply_symbol(ord(name_y[pos]))
    if index_x == index_y:
        if length_x == length_y:
            return 0
        else:
            if length_x < length:
                return -1
            return 1
    else:
        if index_x < index_y:
            return -1
        return 1


def render_place_list(template=None, mimetype=None):
    def renderer(function):
        @wraps(function)
        def wrapper(request, *args, **kwargs):
            output = function(request, *args, **kwargs)
            if not isinstance(output, dict):
                return output
            output['DISTRICT'] = settings.DISTRICT[1:]
            tmpl = output.pop('TEMPLATE', template)
            return render_to_response(tmpl, output,
                        context_instance=RequestContext(request),
                        mimetype=mimetype)
        return wrapper
    return renderer


def get_events_datelist(occurences, start=None, end=None):

    dates = []
    for period in occurences:
        if start and start >= period.start_date:
            start_date = start
        else:
            start_date = period.start_date

        if end and end <= to_datetime(period.end_date, True).date():
            end_date = end
        else:
            end_date = period.end_date

        for date in period.get_start_dates:
            if isinstance(date, datetime):
                date = date
            if start_date <= date.date() <= end_date:
                dates.append(date)
            elif date.date() > end_date:
                break
    datelist = list(set(dates))
    datelist.sort()
    return datelist
