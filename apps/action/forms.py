import datetime

from django import forms
from django.utils.translation import ugettext_lazy as _

from action.models import Action, Poll, WorkBidder, Winner

from apps.control.widgets import ImageWidget
from apps.elrte.widgets import ElrteTextareaWidget


class ActionForm(forms.ModelForm):

    short_text = forms.CharField(label=_('short text for description'), widget=ElrteTextareaWidget())
    full_text = forms.CharField(label=_('full text'), widget=ElrteTextareaWidget())
    pub_date = forms.DateTimeField(
        initial=datetime.date.today(),
        widget=forms.TextInput(attrs={'class':'datepicker'}),
        label=_('Pub date'))
    image = forms.FileField(required=False, label=_("image"), widget=ImageWidget)

    class Meta:
        model = Action

class ActionPollForm(forms.ModelForm):

    start_date = forms.DateTimeField(
        initial=datetime.date.today(),
        widget=forms.TextInput(attrs={'class':'datepicker'}),
        label=_('start date'))
    end_date = forms.DateTimeField(
        initial=datetime.date.today(),
        widget=forms.TextInput(attrs={'class':'datepicker'}),
        label=_('end date'))

    class Meta:
        model = Poll

class WorkBidderForm(forms.ModelForm):

    photo = forms.FileField(required=False, label=_("photo"), widget=ImageWidget)
    text = forms.CharField(label=_('text'), widget=ElrteTextareaWidget(), required=False)

    class Meta:
        model = WorkBidder

class WinnerForm(forms.ModelForm):
    photo = forms.FileField(required=False, label=_("photo"), widget=ImageWidget)
    dt = forms.DateTimeField(
        initial=datetime.date.today(),
        widget=forms.TextInput(attrs={'class':'datepicker'}),
        label=_('date'))

    class Meta:
        model = Winner
        exclude = ('action', )
