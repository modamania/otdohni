# -*- coding: utf-8 -*-
from apps.tea.forms import InterviewAdminForm
from apps.tea.models import Interview
from django.contrib.sites.models import Site
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.conf import settings

from annoying.decorators import render_to

from event.models import Event, Occurrence
from event.forms import EventForm, BaseOccurrenceFormSet, OccurrenceForm
from specprojects.models import SpecProject

from control.utils import can_access

@can_access()
@render_to('control/tea_list.html')
def tea_list(request):
    if not request.user.has_module_perms('tea'):
        return HttpResponseForbidden()
    tea_list = Interview.objects.select_related().all().order_by('-pub_date')
    if 'q' in request.GET:
        q = request.GET['q']
        tea_list = tea_list.filter(Q(title__icontains=q))
    else:
        q = ''
    paginator = Paginator(tea_list, settings.EVENT_PAGINATION)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        tea_stars = paginator.page(page)
    except (EmptyPage, InvalidPage):
        tea_stars = paginator.page(paginator.num_pages)

    return {
        'tea_stars': tea_stars,
        'q': q
    }


@can_access()
@render_to('control/tea_show.html')
def tea_show(request, tea_pk):
    if not request.user.has_module_perms('coupon'):
        return HttpResponseForbidden()
    tea = get_object_or_404(Interview, pk=tea_pk)
    return {'tea': tea}


@can_access()
@render_to('control/tea_form.html')
def tea_form(request, tea_pk=None):
    if not request.user.has_module_perms('coupon'):
        return HttpResponseForbidden()
    if tea_pk:
        tea = get_object_or_404(Interview, pk=tea_pk)
    else:
        tea = None

    if request.method == 'POST':
        #request.POST['sites'] = Site.objects.get_current().id
        form = InterviewAdminForm(request.POST, request.FILES, instance=tea)
        if form.is_valid():
            tea = form.save()
        return HttpResponseRedirect(reverse(tea_show,  kwargs={'tea_pk': tea.pk}))
    else:
        form = InterviewAdminForm(instance=tea)
    return {
        'form': form,
        'tea': tea
    }
