import datetime
from apps.elrte.widgets import ElrteTextareaWidget
from django import forms
from blog.models import Post
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class PostAdminForm(forms.ModelForm):

    user = forms.ModelChoiceField(queryset=User.objects.order_by('username'), label=_('user'), required=False)
    full_text = forms.CharField(label=_('Text'), widget=ElrteTextareaWidget())
    pub_date = forms.DateTimeField(
        initial=datetime.date.today(),
        widget=forms.TextInput(attrs={'class':'datepicker'}),
        label=_('Pub date'))

    class Meta:
        model = Post
        
    def __init__(self, *args, **kwargs):
        super(PostAdminForm, self).__init__(*args, **kwargs)
        self.fields['short_text'].widget = forms.Textarea()
