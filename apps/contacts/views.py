#coding: utf-8
from django.shortcuts import redirect
from django.conf import settings

from django.utils.translation import ugettext_lazy as _

from annoying.decorators import render_to

if 'mailer' in settings.INSTALLED_APPS:
    from mailer import send_mail
else:
    from django.core.mail import send_mail

from forms import ContactForm


@render_to('contacts/contacts.html')
def submit(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            d = {
                    'title':data['title'],
                    'email': data['email'],
            }
            subject = _('%(title)s from %(email)s.') % d
            from_email, to = data['email'], settings.DEFAULT_FROM_EMAIL
            content = data['text']
            send_mail(subject, content, from_email, [to])
            return redirect('contact_tnx')
    else:
        form = ContactForm()
    return {
        'form': form,
    }
