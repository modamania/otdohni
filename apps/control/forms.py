from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from apps.control.widgets import ImageWidget
from core.forms import LocalForm
from profile.models import SEX_CHOICES

class ProfileForm(LocalForm):
    userpic = forms.FileField(required=False, label=_("Userpic"), widget=ImageWidget);
    username = forms.RegexField(regex=r'^\w+$', max_length=30, \
        label=_(u'username'))
    first_name = forms.CharField(max_length=30, required=False, label=_("first_name"));
    last_name = forms.CharField(max_length=30, required=False, label=_("last_name"));
    email = forms.EmailField(required=True, label=_("Email"))
    sex = forms.ChoiceField(choices=SEX_CHOICES, label=_("sex"))
    birthday = forms.DateField(required=False, label=_("birthday"))
    country = forms.CharField(max_length=50, required=False, label=_("country"))
    city = forms.CharField(max_length=50, required=False, label=_("city"))
    web_site = forms.URLField(verify_exists=False, required=False, label=_("web_site"))
    icq = forms.CharField(max_length=15, required=False, label=_("icq"))
    profession = forms.CharField(required=False, label=_("profession"))
    company = forms.CharField(required=False, label=_("company"))
    address = forms.CharField(required=False, label=_("address"))
    phone_number = forms.CharField(max_length=50, required=False, label=_("phone_number"))
    interest = forms.CharField(required=False, label=_(u"interest"))
    about = forms.CharField(required=False, label=_(u"about"))
    is_active = forms.BooleanField(required=False, label=_(u"Is active"))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ProfileForm, self).__init__(*args, **kwargs)


    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        
        """
#        print self.user
        if self.user.username == self.cleaned_data['username']:
            return self.cleaned_data['username']
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_(u'This username is already taken. Please choose another.'))
