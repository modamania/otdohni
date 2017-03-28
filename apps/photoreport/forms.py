import datetime
from apps.control.widgets import ImageWidget
from apps.elrte.widgets import ElrteTextareaWidget
from apps.photoreport.models import PhotoReport, Photo, PhotoReportUpload
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.models import inlineformset_factory, BaseInlineFormSet


class SendToFriend( forms.Form ):
    name = forms.CharField(label=_("Friend's name"),)
    email = forms.EmailField(label=_("Friend's email"),)


class PhotoreportForm(forms.ModelForm):

    description = forms.CharField(label=_('Text'), widget=ElrteTextareaWidget(),
                                  required=False)
    pub_date = forms.DateTimeField(
        initial=datetime.date.today(),
        widget=forms.TextInput(attrs={'class':'datepicker'}),
        label=_('Pub date'))
    date_event = forms.DateTimeField(
        initial=datetime.date.today(),
        widget=forms.TextInput(attrs={'class':'datepicker'}),
        label=_('date event'))

    class Meta:
        model = PhotoReport
        widgets = {
            'num_photos': forms.HiddenInput()
            }

class PhotoreportPhotoForm(forms.ModelForm):

    caption = forms.CharField(label=_('Text'), widget=ElrteTextareaWidget(), required=False)
    date_added = forms.DateTimeField(
        initial=datetime.date.today(),
        widget=forms.TextInput(attrs={'class':'datepicker'}),
        label=_('date added'))
    image = forms.FileField(required=False, label=_("image"), widget=ImageWidget)

    class Meta:
        model = Photo

class PhotoReportUploadForm(forms.ModelForm):

    class Meta:
        model = PhotoReportUpload
