from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from elrte.widgets import ElrteTextareaWidget
from expert.models import ExpertComment

class ExpertForm(forms.ModelForm):

    class Meta:
        model = ExpertComment
        exclude = ['author']
        widgets ={
            "comment" : ElrteTextareaWidget(),
            "is_published" : forms.CheckboxInput(),
        }
