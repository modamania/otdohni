#-*- coding: utf-8 -*-
from django import template
from django.template import Node, NodeList, VariableDoesNotExist
from django.utils.translation import ugettext as _

from settings import DISTRICT

import re

register = template.Library()


def get_office(address):
    if not address:
        main_office = address.objects.none()
        add_address = address.objects.none()
    else:
        main_office_qs = address.filter(is_main_office=True)
        if not main_office_qs:
            main_office = address.objects.all()[0]
        else:
            main_office = main_office_qs[0]
    return {
        'main_office': main_office,
        'add_address': add_address,
    }


@register.filter
def generate_onclick(field, num):
    pattern = r"(?<=-\w{4})(?=')"
    if 'onclick' in field.field.widget.attrs:
        attrs = field.field.widget.attrs
        field.field.widget.attrs['onclick'] = attrs['onclick'].replace("&#39;", "'")
        field.field.widget.attrs['onclick'] = re.sub(pattern, "-%d" % num, attrs['onclick'])
    return field


@register.filter
def get_district(num):
    if num == u'0':
        num = None
    return dict(DISTRICT)[num].title()


class IsMainOffice(Node):
    def __init__(self, obj):
        self.obj = obj

    def render(self):
        pass


def ismainoffice(parser, token):
    try:
        tag, address = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError()
    return IsMainOffice(address)


@register.inclusion_tag("control/tags/render_work_time.html")
def render_work_time(instance):
    weekday_name_list = (_(u"mon"), _(u"tue"), _(u"wed"), _(u"thu"), _(u"fri"), _(u"sat"), _(u"sun"))
    weekday_localize = (u"Пн", u"Вт", u"Ср", u"Чт", u"Пт", u"Сб", u"Вс")

    def get_range_or_list(item_dict):
        if not item_dict:
            return ""
        elif len(item_dict) == 1:
            return item_dict.values().pop()

        item_dict_num = item_dict.keys()
        item_dict_num.sort()
        edge_x = min(item_dict_num)
        edge_y = max(item_dict_num)

        if range(edge_x, edge_y+1) == item_dict_num:
            workdays = "-".join([item_dict[edge_x], item_dict[edge_y]])
        else:
            workdays = ", ".join(item_dict.values())

        return workdays

    result = []

    if not instance or not instance.work_time.exists():
        return result

    for work_time in instance.work_time.all():
        workday_dict = {}
        offday_dict = {}
        for number, weekday_name in enumerate(weekday_name_list):
            weekday = getattr(work_time, weekday_name)
            if weekday:
                day_type = workday_dict
            else:
                day_type = offday_dict
            day_type[number] = weekday_localize[number]

        if work_time.day_off:
            time = u"выходной"
        elif work_time.all_day:
            time = u"круглосуточно"
        elif work_time.from_time and work_time.till_time:
            prep = lambda x: x.strftime("%H:%M")
            time = "%s - %s" % (prep(work_time.from_time), prep(work_time.till_time))
        else:
            time = ""
            
        
        result.append({
            "workday": get_range_or_list(workday_dict),
            "offday": get_range_or_list(offday_dict),
            "time": time,
            })

    return {
        "shedule_list": result,
    }

@register.inclusion_tag('control/tags/paginator.html')
def paginator(objects):
    PAGE_MAX_COUNT = 20

    page_current = objects.number
    page_count = objects.paginator.num_pages

    if page_current <= PAGE_MAX_COUNT:
        st = 1
    else:
        st = page_current - PAGE_MAX_COUNT
    if page_current + PAGE_MAX_COUNT > page_count:
        end = page_count
    else:
        if st == 1:
            end = (page_current + PAGE_MAX_COUNT) * 2
        else:
            end = page_current + PAGE_MAX_COUNT
    rn = xrange(st, end + 1)
    return {
        'range': rn,
        'objects': objects,
    }
