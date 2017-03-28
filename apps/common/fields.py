from django.utils.translation import ugettext as _
from django.core.validators import email_re
from django import forms

import re

email_separator_re = re.compile(r'[,;:]+')


class EmailsListField(forms.CharField):

    @staticmethod
    def _is_valid_email(email):    
        return email_re.match(email)

    def clean(self, value):
        super(EmailsListField, self).clean(value)

        if not value and not self.required:
            return ''

        emails = email_separator_re.split(value)

        if not emails:
            raise forms.ValidationError(_(u'Enter at least one e-mail address.'))

        for email in emails:
            if not self._is_valid_email(email.strip()):
                raise forms.ValidationError(_('%s is not a valid e-mail address.') % email)

        return ', '.join(emails)
