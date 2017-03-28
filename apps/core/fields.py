import datetime
import re
from django.db.models.fields import CharField
from django.forms.fields import RegexField
from django.forms import DateField as djangoDateField, ValidationError
from django.utils.formats import get_format
from django.utils import datetime_safe
from django.conf import settings
from core.widgets import ColorFieldWidget

RGB_REGEX = re.compile('^#?((?:[0-F]{3}){1,2})$', re.IGNORECASE)

class DateField(djangoDateField):
    def clean(self, value):
        y = value['y']
        m = value['m']
        d = value['d']

        if (y == m == d == u'') and not self.required:
            return None

        try:
            y = int(value['y'])
            m = int(value['m'])
            d = int(value['d'])
        except ValueError:
            raise ValidationError(self.error_messages['invalid'])

        if y and m and d:
            if settings.USE_L10N:
                input_format = get_format('DATE_INPUT_FORMATS')[0]
                try:
                    date_value = datetime.date(int(y), int(m), int(d))
                except ValueError:
                    raise ValidationError(self.error_messages['invalid'])
                else:
                    date_value = datetime_safe.new_date(date_value)
                    return self.to_python(date_value.strftime(input_format))
            else:
                return self.to_python('%s-%s-%s' % (y, m, d))
        raise ValidationError(self.error_messages['invalid'])

class RGBColorField(CharField):

    widget = ColorFieldWidget

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 7
        super(RGBColorField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs.update({
            'form_class': RegexField,
            'widget': self.widget,
            'regex': RGB_REGEX
        })
        return super(RGBColorField, self).formfield(**kwargs)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^colorful\.fields\.RGBColorField"])
except ImportError:
    pass