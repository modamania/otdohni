from django import forms
from django.utils.translation import ugettext_lazy as _


class ContactForm( forms.Form ):
    name = forms.CharField(label=_('Your name'), max_length=80)
    email = forms.EmailField(label=_("Your email"), max_length=80)
    title = forms.CharField(label=_("Title"), max_length=80)
    text = forms.CharField(label=_("Your message"), widget=forms.Textarea)

