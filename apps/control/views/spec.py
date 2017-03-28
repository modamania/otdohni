# -*- coding: utf-8 -*-
from apps.specprojects.forms import SpecProjectAdminForm
from django.contrib.sites.models import Site
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.forms.models import modelformset_factory
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.conf import settings

from annoying.decorators import render_to

from event.models import Event, Occurrence
from event.forms import EventForm, BaseOccurrenceFormSet, OccurrenceForm
from specprojects.models import SpecProject

from control.utils import can_access
from pytils.translit import slugify


@can_access()
@render_to('control/spec_list.html')
def spec_list(request):
    if not request.user.has_module_perms('specproject'):
        return HttpResponseForbidden()
    spec_list = SpecProject.objects.select_related().all().order_by('top_title')
    if 'q' in request.GET:
        q = request.GET['q']
        spec_list = spec_list.filter(Q(top_title__icontains=q))
    else:
        q = ''
    paginator = Paginator(spec_list, settings.EVENT_PAGINATION)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        specprojects = paginator.page(page)
    except (EmptyPage, InvalidPage):
        specprojects = paginator.page(paginator.num_pages)

    return {
        'specprojects': specprojects,
        'q': q
    }


@can_access()
@render_to('control/spec_show.html')
def spec_show(request, spec_slug):
    if not request.user.has_module_perms('specproject'):
        return HttpResponseForbidden()
    spec = get_object_or_404(SpecProject, slug=spec_slug)
    return {'spec': spec}


@can_access()
@render_to('control/spec_form.html')
def spec_form(request, spec_slug=None):
    if not request.user.has_module_perms('specproject'):
        return HttpResponseForbidden()
    if spec_slug:
        spec = get_object_or_404(SpecProject, slug=spec_slug)
    else:
        spec = None

    if request.method == 'POST':
        if not request.POST['slug']:
            slug = slugify(request.POST['top_title'])
            num_spec = len(SpecProject.objects.filter(slug__contains= slug).all())
            if num_spec > 0:
                request.POST['slug'] = "%s-%s" % (slugify(request.POST['top_title']), num_spec)
            else:
                request.POST['slug'] = slugify(request.POST['top_title'])
        #request.POST['sites'] = Site.objects.get_current().id
        form = SpecProjectAdminForm(request.POST, instance=spec)
        if form.is_valid():
            spec = form.save(commit=False)
            spec.save()
        return HttpResponseRedirect(reverse(spec_show,  kwargs={'spec_slug': spec.slug}))
    else:
        form = SpecProjectAdminForm(instance=spec)
    return {
        'form': form,
        'spec': spec
        }
