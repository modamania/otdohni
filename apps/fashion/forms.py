from django import forms
from fashion.models import FashionItem

class FashionItemAdminForm(forms.ModelForm):

    class Meta:
        model = FashionItem
        
    def __init__(self, *args, **kwargs):
        super(FashionItemAdminForm, self).__init__(*args, **kwargs)
        self.fields['short_text'].widget = forms.Textarea()
