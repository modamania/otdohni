import datetime
from time import strptime
import re

from django import forms
from django.db import models
from django.conf import settings
from django.utils.formats import get_format
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils.dates import MONTHS
from django.forms.util import flatatt
from django.forms.extras.widgets import SelectDateWidget

from south.modelsinspector import add_introspection_rules

SECS_PER_DAY=3600*24

RE_DATE = re.compile(r'(\d{4})-(\d\d?)-(\d\d?)$')
TIME_PATTERN = "([0-9]{,2})([:-])([0-9]{,2})"
TIME_SEPARATOR = "[;,]"


def _parse_date_fmt():
    fmt = get_format('DATE_FORMAT')
    escaped = False
    output = []
    for char in fmt:
        if escaped:
            escaped = False
        elif char == '\\':
            escaped = True
        elif char in 'Yy':
            output.append('year')
            #if not self.first_select: self.first_select = 'year'
        elif char in 'bEFMmNn':
            output.append('month')
            #if not self.first_select: self.first_select = 'month'
        elif char in 'dj':
            output.append('day')
            #if not self.first_select: self.first_select = 'day'
    return output

class TimelistField(models.CharField):

    __metaclass__ = models.SubfieldBase

    def __init__(self, count=48, *args, **kwargs):
        self.count = count      #for south
        kwargs['max_length'] = count * 6
        super(TimelistField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value is None or isinstance(value, list):
            return value

        times_str = re.split(TIME_SEPARATOR, value)

        times = []
        for time_str in times_str:
            #ignore the time in the wrong format
            match = re.match(TIME_PATTERN, time_str.strip())

            if not match:
                continue

            pattern_time = "%H" + match.groups()[1] + "%M"

            time_time = strptime(time_str.strip(), pattern_time)
            time_date = datetime.time(time_time.tm_hour, time_time.tm_min)
            times.append(time_date)
        return times

    def get_prep_value(self, value):
        if not value:
            return None
        if type(value) == str:
            value = self.to_python(value)
        return ",".join(["%02i:%02i" % (t.hour, t.minute) for t in value])

    def formfield(self, *args, **kwargs):
        defaults = {
                'form_class': TimelistFormField
            }
        defaults.update(kwargs)
        return super(TimelistField, self).formfield(*args, **defaults)


class TimelistFormField(forms.CharField):

    errors = {
            "date": "Invalid date format",
            "hour": "Invalid hour format",
            "minute": "Invalid minute format",
            "len": "The maximum number of dates",
        }

    def __init__(self, *args, **kwargs):
        kwargs['widget'] = TimelistWidget
        super(TimelistFormField, self).__init__(*args, **kwargs)

    def clean(self, value):
        if not value:
            return None
        try:
            super(TimelistFormField, self).clean(value)
        except forms.ValidationError:
            raise forms.ValidationError(self.errors['len'])

        time_list = re.split(TIME_SEPARATOR, value)

        for time_to_check in time_list:
            time_match = re.match(TIME_PATTERN, time_to_check.strip())

            if not time_match:
                raise forms.ValidationError(self.errors['date'])

            hour, separator, minute = time_match.groups()

            if not 0 <= int(hour) <= 23:
                raise forms.ValidationError(self.errors['hour'])
            elif not 0 <= int(minute) <= 59:
                raise forms.ValidationError(['minute'])

        return value


class TimelistWidget(forms.Widget):

    input_type = None

    def render(self, name, value, attrs):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value:
            if isinstance(value, list):
                value = ", ".join(["%02i:%02i" % (t.hour, t.minute) for t in value])
            final_attrs['value'] = value
        return mark_safe(u'<input%s />' % flatatt(final_attrs))


class TimedeltaField(models.Field):
    u'''
    Store Python's datetime.timedelta in an integer column.
    Most databasesystems only support 32 Bit integers by default.

    $Id: TimedeltaField.py 1787 2011-04-20 07:09:57Z tguettler $
    $HeadURL: svn+ssh://svnserver/svn/djangotools/trunk/dbfields/TimedeltaField.py $

    # http://djangosnippets.org/snippets/1060/
    '''
    __metaclass__=models.SubfieldBase
    def __init__(self, *args, **kwargs):
        super(TimedeltaField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if (value is None) or isinstance(value, datetime.timedelta):
            return value
        #TODO fix this bug!!
        #TemplateSyntaxError: Caught AssertionError while rendering: (86400L, <type 'long'>)
        value = int(value)
        assert isinstance(value, int), (value, type(value))
        return datetime.timedelta(seconds=value)

    def get_internal_type(self):
        return 'IntegerField'

    def get_db_prep_lookup(self, lookup_type, value, connection=None, prepared=False):
        raise NotImplementedError()  # SQL WHERE

    def get_db_prep_save(self, value, connection=None, prepared=False):
        if (value is None) or isinstance(value, int):
            return value
        return SECS_PER_DAY*value.days+value.seconds

    def formfield(self, *args, **kwargs):
        defaults={'form_class': TimedeltaFormField}
        defaults.update(kwargs)
        return super(TimedeltaField, self).formfield(*args, **defaults)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)


class TimedeltaFormField(forms.Field):
    default_error_messages = {
        'invalid':  _(u'Enter a whole number.'),
        }

    def __init__(self, *args, **kwargs):
        defaults={'widget': TimedeltaWidget}
        defaults.update(kwargs)
        super(TimedeltaFormField, self).__init__(*args, **defaults)

    def clean(self, value):
        # value comes from Timedelta.Widget.value_from_datadict(): tuple of strings
        super(TimedeltaFormField, self).clean(value)
        assert len(value)==len(self.widget.inputs), (value, self.widget.inputs)
        i=0
        for value, multiply in zip(value, self.widget.multiply):
            try:
                i+=int(value)*multiply
            except ValueError, TypeError:
                raise forms.ValidationError(self.error_messages['invalid'])
        return i


class TimedeltaWidget(forms.Widget):
    INPUTS=['days', 'hours', 'minutes', 'seconds']
    MULTIPLY=[60*60*24, 60*60, 60, 1]
    def __init__(self, attrs=None):
        self.widgets=[]
        if not attrs:
            attrs={}
        inputs=attrs.get('inputs', self.INPUTS)
        multiply=[]
        for input in inputs:
            assert input in self.INPUTS, (input, self.INPUT)
            self.widgets.append(forms.TextInput(attrs=attrs))
            multiply.append(self.MULTIPLY[self.INPUTS.index(input)])
        self.inputs=inputs
        self.multiply=multiply
        super(TimedeltaWidget, self).__init__(attrs)

    def render(self, name, value, attrs):
        if value is None:
            values=[0 for i in self.inputs]
        elif isinstance(value, datetime.timedelta):
            values=split_seconds(value.days*SECS_PER_DAY+value.seconds, self.inputs, self.multiply)
        elif isinstance(value, int):
            # initial data from model
            values=split_seconds(value, self.inputs, self.multiply)
        else:
            assert isinstance(value, tuple), (value, type(value))
            assert len(value)==len(self.inputs), (value, self.inputs)
            values=value
        id=attrs.pop('id')
        assert not attrs, attrs
        rendered=[]
        for input, widget, val in zip(self.inputs, self.widgets, values):
            rendered.append(u'%s %s' % (_(input), widget.render('%s_%s' % (name, input), val)))
        return mark_safe('<div id="%s">%s</div>' % (id, ' '.join(rendered)))

    def value_from_datadict(self, data, files, name):
        # Don't throw ValidationError here, just return a tuple of strings.
        ret=[]
        for input, multi in zip(self.inputs, self.multiply):
            ret.append(data.get('%s_%s' % (name, input), 0))
        return tuple(ret)

    def _has_changed(self, initial_value, data_value):
        # data_value comes from value_from_datadict(): A tuple of strings.
        if initial_value is None:
            return bool(set(data_value)!=set([u'0']))
        assert isinstance(initial_value, datetime.timedelta), initial_value
        initial=tuple([unicode(i) for i in split_seconds(initial_value.days*SECS_PER_DAY+initial_value.seconds, self.inputs, self.multiply)])
        assert len(initial)==len(data_value), (initial, data_value)


def split_seconds(secs, inputs=TimedeltaWidget.INPUTS, multiply=TimedeltaWidget.MULTIPLY,
                  with_unit=False, remove_leading_zeros=False):
    ret=[]
    assert len(inputs)<=len(multiply), (inputs, multiply)
    for input, multi in zip(inputs, multiply):
        count, secs = divmod(secs, multi)
        if remove_leading_zeros and not ret and not count:
            continue
        if with_unit:
            ret.append('%s%s' % (count, input))
        else:
            ret.append(count)
    return ret


add_introspection_rules([
    (
        [TimelistField],
        [],
        {},
    ),
], ["^event\.fields\.TimelistField"])
add_introspection_rules([
    (
        [TimedeltaField],
        [],
        {},
    ),
], ["^event\.fields\.TimedeltaField"])


class CustomDateWidget(SelectDateWidget):

    def render(self, name, value, attrs=None):
        try:
            year_val, month_val, day_val = value.year, value.month, value.day
        except AttributeError:
            year_val = month_val = day_val = None
            if isinstance(value, basestring):
                if settings.USE_L10N:
                    try:
                        input_format = get_format('DATE_INPUT_FORMATS')[0]
                        v = datetime.datetime(*(strptime(value, input_format)[0:6]))
                        year_val, month_val, day_val = v.year, v.month, v.day
                    except ValueError:
                        pass
                else:
                    match = RE_DATE.match(value)
                    if match:
                        year_val, month_val, day_val = [int(v) for v in match.groups()]
        year_html =  mark_safe(u'<input%s />' % flatatt({
                                        'id': '%s_year' % attrs['id'],
                                        'name': self.year_field % name,
                                        'value': year_val or '',
                                        'class': 'year_date',
                                        }))
        choices = MONTHS.items()
        month_html = self.create_select(name, self.month_field, value, month_val, choices)
        day_html =  mark_safe(u'<input%s />' % flatatt({
                                        'id': '%s_day' % attrs['id'],
                                        'name': self.day_field % name,
                                        'value': day_val or '',
                                        'class': 'day_date',
                                        }))

        output = []
        for field in _parse_date_fmt():
            if field == 'year':
                output.append(year_html)
            elif field == 'month':
                output.append(month_html)
            elif field == 'day':
                output.append(day_html)
        return mark_safe(u'\n'.join(output))
