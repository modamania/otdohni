#-*- coding: UTF-8 -*-

import datetime
from urlparse import urljoin

import calendar as old_calendar

old_calendar.month_name = ['', 'Январь','Февраль','Март','Апрель','Май','Июнь','Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь']
old_calendar.day_abbr = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

COUNT_MONTH = 3

def get_dates_in_month(year, month):
    c = old_calendar.Calendar()
    return (date for date in c.itermonthdates(year, month)\
                if date.year == year and date.month == month)

def get_dates_in_week(day=None):
    date = day or datetime.date.today()
    return (date + datetime.timedelta(days=i) for i in xrange(7))

def add_navigation(calendar, href=None, year=None, month=None):
    if href and year and month:
        date = datetime.date(year, month, 15)
        prev_date = date - datetime.timedelta(days=30)
        prev_href = urljoin(href, "%d/%d/" % (prev_date.year, prev_date.month))

        next_date = date + datetime.timedelta(days=30)
        next_href = urljoin(href, "%d/%d/" % (next_date.year, next_date.month))
    else:
        prev_href = next_href = ''
    return "<a href='%s' id='calendar_prev_month' class='prev_month'></a>\
            <a href='%s' id='calendar_next_month' class='next_month'></a>\
            %s" % (prev_href, next_href, calendar)


class Month(object):
    def __init__(self, month):
         if not 1 <= month <= 12:
             raise ValueError, month
         self.month = month

    def __sub__(self, value):
        if not isinstance(value, self.__class__):
            raise TypeError, value
        sub = self.month - value.month
        if sub == 0:
            return self.__class__(self.month)
        elif sub < 0:
            month = 12 + sub
            return self.__class__(month)
        return self.month - value.month

    def __add__(self, value):
        add = self.month + value
        if add > 12:
            return 1
        return add


class HTMLCalendar(old_calendar.HTMLCalendar):
    def __init__(self, choices_day=None, href=None, *args, **kwargs):
        self.choices_day = choices_day or []
        self.href = href
        super(HTMLCalendar, self).__init__(*args, **kwargs)

    def _get_href(self, year, month, day):
        if not self.href:
            return '#'
        if isinstance(self.href, str):
            return urljoin(self.href, "%d/%d/%d" % ( year, month, day))
        elif type(self.href) == 'function':
            return self.href(year, month, day)
        assert TypeError, self.href

    def formatrangemonth(self, first, last, count=None):
        count = count or COUNT_MONTH

        if first.year == last.year and first.month == last.month:
            rnge = 1
        else:
            rnge = Month(last.month) - Month(first.month)
            rnge = rnge + 1

        if rnge > count:
            rnge = count

        month_date_list = [(
                (first + datetime.timedelta(days=x*30)).year,
                (first + datetime.timedelta(days=x*30)).month
                ) for x in xrange(rnge)]

        return [self.formatmonth(*dt) for dt in month_date_list]

    def formatmonthname(self, theyear, themonth, withyear=True):
        if withyear:
            s = '%s %s' % (old_calendar.month_name[themonth], theyear)
        else:
            s = '%s' % old_calendar.month_name[themonth]
        return '<span class="current_month">%s</span>' % s

    def formatmonth(self, theyear, themonth, withyear=True):
        v = []
        a = v.append
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('<span class="daynames-bg"></span>')
        a('<table class="month">')
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week, theyear, themonth))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)

    def formatday(self, day, weekday, year=None, month=None):
        if day == 0:
            return '<td class="noday">&nbsp;</td>'
        if year and month:
            for ds in self.choices_day:
                if datetime.date(year, month, day) == ds:
                    href = self._get_href(year, month, day)
                    return "<td class='%s'>\
                                <a href='%s'>%d</a>\
                            </td>" % (self.cssclasses[weekday], href, day)
        return "<td class='%s'>%d</td>" % (self.cssclasses[weekday], day)

    def formatweek(self, theweek, theyear, themonth):
        s = ''.join(self.formatday(d, wd, theyear, themonth) for (d, wd) in theweek)
        return '<tr>%s</tr>' % s
