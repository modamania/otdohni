from django import forms
from lunch.models import LunchObject
from django.utils.translation import ugettext_lazy as _

class LunchObjectAdminForm(forms.ModelForm):

    class Meta:
        model = LunchObject

    def clean(self):
        """ Validates end date period """
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')

        if start_date and end_date:
            if end_date <= start_date:
                msg = _("end date can not be earlier then start date")
                self._errors['end_date'] = self.error_class([msg])

        return self.cleaned_data
