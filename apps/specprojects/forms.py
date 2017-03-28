from apps.elrte.widgets import ElrteTextareaWidget
from django import forms
from specprojects.models import SpecProject
from django.utils.translation import ugettext_lazy as _

class SpecProjectAdminForm(forms.ModelForm):

    description = forms.CharField(widget=ElrteTextareaWidget())

    class Meta:
        model = SpecProject
        #widgets = {
        #    'slug': forms.HiddenInput(),
        #    }