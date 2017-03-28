import datetime
from apps.control.widgets import ImageWidget
from django import forms
from sales.models import Coupon
from django.utils.translation import ugettext_lazy as _

class CouponAdminForm(forms.ModelForm):

    small_image = forms.FileField(required=False, label=_("small image"), widget=ImageWidget)
    image = forms.FileField(required=False, label=_("image"), widget=ImageWidget)
    start_date = forms.DateTimeField(
        widget=forms.TextInput(attrs={'class':'datepicker'}),
        label=_('start date'))
    end_date = forms.DateTimeField(
        required=False,
        widget=forms.TextInput(attrs={'class':'datepicker'}),
        label=_('end date'))
    pub_date = forms.DateTimeField(
        initial=datetime.date.today(),
        widget=forms.TextInput(attrs={'class':'datepicker'}),
        label=_('Pub date'))

    class Meta:
        model = Coupon
        widgets = {
            'views': forms.HiddenInput(),
            }

    def clean(self):
        """ Validates end date period """
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')

        if start_date and end_date:
            if end_date <= start_date:
                msg = _("end date can not be earlier then start date")
                self._errors['end_date'] = self.error_class([msg])

        return self.cleaned_data
