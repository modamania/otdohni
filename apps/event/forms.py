#-*- coding: UTF-8 -*-
from django import forms
from django.forms.extras import SelectDateWidget
from django.forms.models import BaseModelFormSet
from django.forms.widgets import  RadioFieldRenderer
from django.forms.extras.widgets import SelectDateWidget

from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.contrib.admin.widgets import FilteredSelectMultiple

from annoying.functions import get_object_or_None
from pytils.translit import slugify
from chosen import forms as chosenforms
from apps.place.models import Place
from apps.elrte.widgets import ElrteTextareaWidget

from apps.event.models import Occurrence,Event
from apps.event.fields import TimelistField, CustomDateWidget

import re


class OccurrenceForm(forms.ModelForm):
    repeat_on = forms.TypedChoiceField(
                        choices=(Occurrence.REPEAT_ON_CHOICES),
                        widget=forms.RadioSelect(),
                        initial=Occurrence.NOREPEAT)
    repeat_every = forms.IntegerField(
                        widget=forms.TextInput(attrs={'size':'4'}),
                        required=False,
                        initial=1)

    repeat_weekday = forms.MultipleChoiceField(
                        choices=Occurrence.CHOICES_WEEKDAY,
                        required=False,
                        widget=forms.CheckboxSelectMultiple(),
                        label=u"По дням недели")
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class':'datepicker'}),
                        label=u"Когда")
    end_date = forms.DateField(
        required=False,
        widget=forms.TextInput(attrs={'class':'datepicker'}),
                        label=u"Дата окончания")

#    place = chosenforms.ChosenChoiceField(
#                        label=u"Где",
#                        overlay=u"Выберете заведение..",
#                        choices=[(i.id, i.name) for i in Place.objects.all()])

    class Meta:
        exclude = ['event']
        model = Occurrence
    #def clean_place(self):
    #    place_id = self.cleaned_data['place']
    #    place = get_object_or_None(Place, id=place_id)
    #    return place

    def clean_repeat_weekday(self):
        days = self.cleaned_data['repeat_weekday']
        if not days and self.cleaned_data['repeat_on'] == Occurrence.WEEKLY:
            raise forms.ValidationError(_('Set the days for repeat')) 
        days = ','.join(days)
        #import ipdb; ipdb.set_trace()
        return days
    
    def clean_repeat_on(self):
        repeat_on  = self.cleaned_data['repeat_on']
        return int(repeat_on)

    def clean_repeat_every(self):
        repeat_every = int(self.cleaned_data['repeat_every'])
        if repeat_every == 0:
            repeat_every = 1
        return repeat_every

    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        start_date = self.cleaned_data['start_date']
        if end_date and end_date < start_date:
            raise forms.ValidationError(_('expiration date can not be less than the start date')) 
        return end_date


class BaseOccurrenceFormSet(BaseModelFormSet):

    pass
    #def clean(self):
        #import ipdb;ipdb.set_trace()
    #    super(BaseOccurrenceFormSet, self).clean()
    #    for form in self.forms:
    #        if form.is_valid():
    #            pass


class EventAdminForm(forms.ModelForm):

    class Meta:
        model = Event


class EventForm(forms.ModelForm):

    is_published = forms.BooleanField(widget=forms.CheckboxInput(),
                required=False,
                label=_(u'is published'))
    description = forms.CharField(widget=ElrteTextareaWidget())
    intro = forms.CharField(required=False,
                widget=forms.Textarea(attrs={'cols': 70, 'rows': 10}))

    class Meta:
        model = Event
        exclude = ['place', 'pub_date', 'members', 'num_comments', 'kinohod_id']
