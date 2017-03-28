import datetime
from apps.control.widgets import ImageWidget
from apps.elrte.widgets import ElrteTextareaWidget
from apps.tea.models import Interview
from django import forms
from django.utils.translation import ugettext_lazy as _

class InterviewAdminForm(forms.ModelForm):

    full_text = forms.CharField(label=_('Text'), widget=ElrteTextareaWidget())
    image = forms.FileField(required=False, label=_("image"), widget=ImageWidget)
    pub_date = forms.DateTimeField(
        initial=datetime.date.today(),
        widget=forms.TextInput(attrs={'class':'datepicker'}),
        label=_('Pub date'))

    class Meta:
        model = Interview