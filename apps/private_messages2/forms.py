from django import forms
from django.utils.translation import ugettext_lazy as _

from core.forms import LocalModelForm
from fields import CommaSeparatedUserField

from models import Message


class MessageForm(LocalModelForm):
    recipient = CommaSeparatedUserField(label=_(u"Recipient"))
    body = forms.CharField(label=_(u"Body"),
            widget=forms.Textarea(attrs={'rows': '12', 'cols': '42'}))

    class Meta:
        fields = ['recipient', 'body',]
        model = Message


class MessageSimpleForm(forms.ModelForm):

    class Meta:
        fields = ['sender', 'chain', 'body']
        model = Message

        widgets = {
            'sender': forms.HiddenInput(),
            'chain': forms.HiddenInput(),
        }
