"""
Extra HTML Widget classes
"""

import time
import datetime
import re

from django.forms.widgets import Widget, Select, DateInput, TextInput
from django.utils import datetime_safe
from django.utils.safestring import mark_safe, SafeUnicode
from django.utils.formats import get_format
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from settings import MONTHS


__all__ = ('SelectDateWidget',)

RE_DATE = re.compile(r'(\d{4})-(\d\d?)-(\d\d?)$')

class SelectDateWidget(Widget):
    """
    A Widget that splits date input into three <select> boxes.

    This also serves as an example of a Widget that has more than one HTML
    element and hence implements value_from_datadict.
    """
    none_value = ('', _('none month'))
    month_field = '%s_month'
    day_field = '%s_day'
    year_field = '%s_year'

    def __init__(self, attrs=None, years=None, required=True):
        self.attrs = attrs or {}
        self.required = required

    def render(self, name, value, attrs=None):

        try:
            year_val, month_val, day_val = value['y'], value['m'], value['d']
        except TypeError:
            try:
                year_val, month_val, day_val = value.year, value.month, value.day
            except AttributeError:
                year_val = month_val = day_val = None
                if isinstance(value, basestring):
                    if settings.USE_L10N:
                        try:
                            input_format = get_format('DATE_INPUT_FORMATS')[0]
                            # Python 2.4 compatibility:
                            #     v = datetime.datetime.strptime(value, input_format)
                            # would be clearer, but datetime.strptime was added in 
                            # Python 2.5
                            v = datetime.datetime(*(time.strptime(value, input_format)[0:6]))
                            year_val, month_val, day_val = v.year, v.month, v.day
                        except ValueError:
                            pass
                    else:
                        match = RE_DATE.match(value)
                        if match:
                            year_val, month_val, day_val = [int(v) for v in match.groups()]

        year_html = self.create_textinput(name, self.year_field, value, \
            year_val, extra_attrs={'class': 'year', 'maxlength': '4'})
        choices = MONTHS.items()
        month_html = self.create_select(name, self.month_field, value, \
            month_val, choices, extra_attrs={'class': 'month'})
        day_html = self.create_textinput(name, self.day_field, value, day_val, \
            extra_attrs={'class': 'day', 'maxlength': '2'})

        format = get_format('DATE_FORMAT')
        escaped = False
        output = []
        for char in format:
            if escaped:
                escaped = False
            elif char == '\\':
                escaped = True
        #    elif char in 'Yy':
        #        output.append(year_html)
        #    elif char in 'bFMmNn':
        #        output.append(month_html)
        #    elif char in 'dj':
        #        output.append(day_html)

        output.append(day_html)
        output.append(month_html)
        output.append(year_html)

        return mark_safe(u'\n'.join(output))

    def id_for_label(self, id_):
        return '%s_month' % id_
    id_for_label = classmethod(id_for_label)

    def value_from_datadict(self, data, files, name):
        y = data.get(self.year_field % name)
        m = data.get(self.month_field % name)
        d = data.get(self.day_field % name)
        return {'y': y, 'm': m, 'd': d}

    def create_select(self, name, field, value, val, choices, extra_attrs=None):
        if 'id' in self.attrs:
            id_ = self.attrs['id']
        else:
            id_ = 'id_%s' % name
        if not (self.required and val):
            choices.insert(0, self.none_value)
        local_attrs = self.build_attrs(extra_attrs, id=field % id_)
        s = Select(choices=choices)
        select_html = s.render(field % name, val, local_attrs)
        return select_html

    def create_textinput(self, name, field, value, val, extra_attrs=None):
        if 'id' in self.attrs:
            id_ = self.attrs['id']
        else:
            id_ = 'id_%s' % name
        local_attrs = self.build_attrs(extra_attrs, id=field % id_)
        s = DateInput()
        select_html = s.render(field % name, val, local_attrs)
        return select_html

try:
    url = settings.STATIC_URL
except AttributeError:
    try:
        url = settings.MEDIA_URL
    except AttributeError:
        url = ''

class ColorFieldWidget(TextInput):
    class Media:
        css = {
            'all': ("%scolorful/colorPicker.css" % url,)
        }
        js  = ("%scolorful/jQuery.colorPicker.js" % url,)

    input_type = 'color'

    def render_script(self, id):
        return u'''<script type="text/javascript">
                    (function($){
                        $(document).ready(function(){
                            $('#%s').each(function(i, elm){
                                // Make sure html5 color element is not replaced
                                if (elm.type != 'color') $(elm).colorPicker();
                            });
                        });
                    })('django' in window ? django.jQuery: jQuery);
                </script>
                ''' % id

    def render(self, name, value, attrs={}):
        if not 'id' in attrs:
            attrs['id'] = "#id_%s" % name
        render = super(ColorFieldWidget, self).render(name, value, attrs)
        return SafeUnicode(u"%s%s" % (render, self.render_script(attrs['id'])))