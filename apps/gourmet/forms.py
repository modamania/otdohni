from django import forms
from gourmet.models import GourmetItem

class GourmetItemAdminForm(forms.ModelForm):

    class Meta:
        model = GourmetItem
        
    def __init__(self, *args, **kwargs):
        super(GourmetItemAdminForm, self).__init__(*args, **kwargs)
        self.fields['short_text'].widget = forms.Textarea()

