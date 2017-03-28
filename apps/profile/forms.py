from django.utils.translation import ugettext_lazy as _
from django import forms

from core.forms import LocalForm
from core.widgets import SelectDateWidget
from core.fields import DateField
from models import *


import settings

from django.core import exceptions
from django.template.defaultfilters import filesizeformat


def image_size_validator(value):
    max_size = settings.MAX_USERPIC_SIZE
    if value.size > max_size:
        raise exceptions.ValidationError(
            _('must be size  %(size)s. real size %(real_size)s.') %
            {'size' : filesizeformat(max_size),
            'real_size': filesizeformat(value.size)})

class ProfileEditForm(LocalForm):
    first_name = forms.CharField(max_length=30, required=False, \
        label=_('first_name'));
    last_name = forms.CharField(max_length=30, required=False, \
        label=_('last_name'));
    email = forms.EmailField(required=True, label=_('Email'))
    sex = forms.ChoiceField(choices=SEX_CHOICES, label=_('sex'))
    birthday = DateField(required=False, label=_('birthday'), \
        widget=SelectDateWidget(required=False))
    country = forms.CharField(max_length=50, required=False, label=_('country'))
    city = forms.CharField(max_length=50, required=False, label=_('city'))
    web_site = forms.URLField(verify_exists=False, required=False, \
        label=_('web_site'))
    icq = forms.CharField(max_length=15, required=False, label=_('icq'))
    profession = forms.CharField(required=False, label=_('profession'))
    company = forms.CharField(required=False, label=_('company'))
    address = forms.CharField(required=False, label=_('address'))
    phone_number = forms.CharField(max_length=50, required=False, \
        label=_('phone_number'))
    interest = forms.CharField(required=False, label=_('interest'), \
        widget=forms.Textarea(attrs={'rows': '6', 'cols':'40'}))
    about = forms.CharField(required=False, label=_('about'), \
        widget=forms.Textarea(attrs={'rows': '6', 'cols':'40'}))
    password1 = forms.CharField(widget=forms.PasswordInput(render_value=False),
        label=_(u'new password'), required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(render_value=False),
        label=_(u'new password (again)'), required=False,
        help_text=_('RegistrationForm_password_helptext'))

    def clean_password2(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.

        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_(u'You must type the same password each time'))
        return self.cleaned_data['password2']


class ProfileUserpicForm(LocalForm):
    userpic = forms.ImageField(label=_('Userpic'), validators=[image_size_validator]);

