# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from place.models import PlaceCategory

from captcha.fields import CaptchaField


class FeedbackForm(forms.Form):
    name = forms.CharField(max_length=300,
            label=_(u'Name'))
    email = forms.EmailField(
            label=_(u'Email'))
    title = forms.CharField(max_length=300,
            label=_(u'title_alt'))
    description = forms.CharField(max_length=5000,
            label=_(u'description'),
            widget=forms.Textarea())

class AddnewForm(forms.Form):
    TYPE_CHOICES = (
            ('event', _('addEvent')),
            ('place', _('addPlace')),
            ('news', _('addNews')),
            ('bug', _('bugReport')),
    )
    EVENT_TYPE_CHOICE = (
        ('kino', _('kino')),
        ('concerts', _('concerts')),
        ('club', _('club')),
        ('show', _('show')),
        ('exibit', _('exibit')),
        ('sport', _('sport')),
        ('other', _('other')),
    )
    fields_for_send = {
        'event' : ['title', 'event_type', 'address', 'date', 'event_description', 'i_event_owner', 'email', 'user_phone',],
        'place' : ['title', 'address', 'phone', 'worktime', 'place_email',
                    'url', 'category', 'place_description', 'i_place_owner', 'email', 'user_phone',],
        'news'  : ['subject', 'news_description', 'email', 'user_phone',],
        'bug'   : ['bug_url', 'bug_description', 'email', 'user_phone',],
    }

    feedback_type = forms.ChoiceField(
                        choices=TYPE_CHOICES,
                        label=_(u'Feedback subject'),
                        widget = forms.widgets.Select(attrs={'class': 'zf',},)
                        )
    email = forms.EmailField(
            label=_(u'Email'))
    user_phone = forms.CharField(
            label=_('Your phone'),
            required=False)
    title = forms.CharField(
            required=False,
            max_length=300,
            label=_(u'title_alt'))
    event_type = forms.ChoiceField(

            choices=EVENT_TYPE_CHOICE,
            required=False,
            label=_(u'Event type'),
            )
    category = forms.ChoiceField(
            choices=PlaceCategory.objects.filter(is_published=True).values_list('id', 'name'),
            required=False,
            label=_(u'Place category')
            )
    address = forms.CharField(
            widget=forms.widgets.TextInput(attrs={'class': 'form-input__input zf'}),
            max_length=200,
            required=False,
            label=_(u'Address')
            )
    phone = forms.CharField(
            widget=forms.widgets.TextInput(attrs={'class': 'form-input__input zf'}),
            max_length=200,
            required=False,
            label=_(u'Phone')
            )
    worktime = forms.CharField(
            widget=forms.widgets.TextInput(attrs={'class': 'form-input__input zf'}),
            max_length=200,
            required=False,
            label=_(u'Work time')
            )
    place_email = forms.CharField(
            widget=forms.widgets.TextInput(attrs={'class': 'form-input__input zf'}),
            max_length=200,
            required=False,
            label=_(u'Place email')
            )
    url = forms.CharField(
            widget=forms.widgets.TextInput(attrs={'class': 'form-input__input zf'}),
            max_length=200,
            required=False,
            label=_(u'Web url')
            )
    bug_url = forms.CharField(
            widget=forms.widgets.TextInput(attrs={'class': 'form-input__input zf'}),
            max_length=200,
            required=False,
            label=_(u'Bug url')
            )
    subject = forms.CharField(
            widget=forms.widgets.TextInput(attrs={'class': 'form-input__input zf'}),
            max_length=200,
            required=False,
            label=_(u'Subject')
            )
    date = forms.CharField(
            widget=forms.widgets.TextInput(attrs={
                'class': 'form-input__input zf',
            }),
            max_length=50,
            required=False,
            label=_(u'Date')
            )
    email = forms.EmailField(
            required=False,
            label=_(u'Email'))
    i_event_owner = forms.BooleanField(
            label=_(u'I event owner'),
            required=False
            )
    i_place_owner = forms.BooleanField(
            label=_(u'I place owner'),
            required=False
            )
    event_description = forms.CharField(max_length=5000,
            required=False,
            label=_(u'description'),
            widget=forms.Textarea())
    place_description = forms.CharField(max_length=5000,
            required=False,
            label=_(u'description'),
            widget=forms.Textarea())
    news_description = forms.CharField(max_length=5000,
            required=False,
            label=_(u'fulltext'),
            widget=forms.Textarea())
    bug_description = forms.CharField(max_length=5000,
            required=False,
            label=_(u'description'),
            widget=forms.Textarea())
    captcha = CaptchaField(label=_(u'Captcha'))


    def display_form_subject(self):
        return unicode(dict(self.TYPE_CHOICES)[self.cleaned_data['feedback_type']])


    def send_fields(self):
        form_type = self.cleaned_data['feedback_type']
        # for name in self.cleaned_data:
        for name in self.fields_for_send[form_type]:
            # if name in self.fields_for_send[form_type]:
            if name in self.cleaned_data:
                field = self.fields[name]
                display_name = field.label
                if type(field) is forms.fields.ChoiceField:
                    try:
                        value = dict(field.choices)[self.cleaned_data[name]]
                    except KeyError:
                        # Maybe keys is integer?
                        value = dict(field.choices)[int(self.cleaned_data[name])]
                elif type(field) is forms.fields.BooleanField:
                    if self.cleaned_data[name]:
                        value = _(u'Yes')
                    else:
                        value = _(u'No')
                else:
                    value = self.cleaned_data[name]
                yield display_name, value
