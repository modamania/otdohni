#-*- coding: utf-8 -*-
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
from django.utils.translation import ugettext as _
from django.contrib.sites.models import get_current_site
from django.contrib.flatpages.models import FlatPage
from django.template import Template, Context

from common.forms import FeedbackForm, AddnewForm

from annoying.decorators import render_to
from annoying.functions import  get_object_or_None


ADDNEW_MAIL_TEMPLATE = """
Сообщение по теме "{{ form.display_form_subject }}"


{% for n, v in form.send_fields %}
    {{ n|title }}: {{ v|default:"---" }}
{% endfor %}
"""

# from django.views.decorators.csrf import csrf_exempt
# @csrf_exempt
@render_to('event/addnew.html')
def addnew(request):
    if request.user.is_authenticated():
        initial = {
            'email': request.user.email,
        }
    else:
        initial = {}
    form = AddnewForm(request.POST or None, initial=initial)
    if form.is_valid():
        username = request.user.username\
            if request.user.is_authenticated() else u"Guest"
        subject = u"%s от пользователя '%s'" % (
                form.display_form_subject(),
                username
        )
        t = Template(ADDNEW_MAIL_TEMPLATE)
        c = Context({'form': form})
        msg = t.render(c)
        send_mail(
                subject,
                msg,
                settings.DEFAULT_FROM_EMAIL,
                ('addnew@zaotdih.ru',),
        )
        return redirect('addnew_success')

    return {
        'form': form,
    }

@render_to('event/addnew_succes.html')
def addnew_success(request):
    return {}

@render_to('about.html')
def feedback(request):
    site_id = get_current_site(request).id
    flatpage = get_object_or_None(FlatPage, url__exact='/about/', sites__id__exact=site_id)
    form = FeedbackForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['name']
        title = form.cleaned_data['title']
        subject = u"От пользователя %s. '%s'" % (username, title)
        send_mail(
            subject,
            form.cleaned_data['description'] + "\nEmail: " + form.cleaned_data['email'],
            settings.DEFAULT_FROM_EMAIL,
            settings.CONTENT_MANAGER_MAIL_LIST,
        )
        messages.add_message(request, messages.INFO, _(u"Thanks for feedback."))
        return redirect('about')

    return {
        "form": form,
        "flatpage": flatpage,
    }
