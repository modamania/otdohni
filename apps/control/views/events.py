# -*- coding: utf-8 -*-
from apps.common.models import ObjectSubscribe
from django.contrib.contenttypes.models import ContentType
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

from control.utils import can_access


@can_access()
@render_to('control/event_list.html')
def event_list(request):
    if not request.user.has_module_perms('event'):
        return HttpResponseForbidden()
    event_list = Event.objects.select_related().all().order_by('title')
    if 'q' in request.GET:
        q = request.GET['q']
        event_list = event_list.filter(Q(title__icontains=q))
    else:
        q = ''
    paginator = Paginator(event_list, settings.EVENT_PAGINATION)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        events = paginator.page(page)
    except (EmptyPage, InvalidPage):
        events = paginator.page(paginator.num_pages)

    return {
        'events': events,
        'q': q
    }


@can_access()
@render_to('control/event_show.html')
def event_show(request, event_pk):
    if not request.user.has_module_perms('event'):
        return HttpResponseForbidden()
    event = get_object_or_404(Event , pk=event_pk)
    is_subscribed = 0
    if request.user.is_authenticated():
        _content_type_id = ContentType.objects.get(model='event').id
        is_subscribed = len(ObjectSubscribe.objects.filter(user = request.user, object_pk = event_pk, content_type = _content_type_id))
    return {'event': event, 'is_subscribed': is_subscribed,}


@can_access()
@render_to('control/event_form.html')
def event_form(request, event_pk=None):
    if not request.user.has_module_perms('event'):
        return HttpResponseForbidden()
    if event_pk:
        event = get_object_or_404(Event, pk=event_pk)
        periods = event.periods.filter(hide_for_editing=False)
    else:
        event = None
        periods = Occurrence.objects.none()

    if periods:
        extra = 0
    else:
        extra = 1
    OccFormSet = modelformset_factory(Occurrence,
                                      formset=BaseOccurrenceFormSet,
                                      form=OccurrenceForm,
                                      exclude=('id', 'event'),
                                      extra=extra,
                                      can_delete=True,)
    if request.method == 'POST':
        keys = ('director', 'actors', 'country', 'year', 'budget', 'duration', 'trailer', 'cost' )
        add_list = request.POST.lists()
        additional = dict([(k, v) for k, values in add_list if k in keys for v in values if v])
        form = EventForm(request.POST, instance=event)
        formset = OccFormSet(request.POST,
                            queryset=periods)
        if form.is_valid() and formset.is_valid():
            event = form.save(commit=False)
            if 'image' in request.FILES:
                try:
                    event.image.delete()
                except OSError:
                    pass
                event.image = request.FILES['image']
            event.additional = additional
            event.save()
            event.genre.add(*form.cleaned_data['genre'])
            items = formset.save(commit=False)
            idx = [item.id for item in items]
            Occurrence.objects.filter(event=event)\
                                           .exclude(id__in=idx)\
                                           .delete()
            for item in items:
                item.event = event
                item.save()
                item.sites.add(settings.SITE_ID)
            return HttpResponseRedirect(reverse(event_show, args=[event.pk]))
        else:
            print ''
            print form
            print '='*40
            print formset
            print ''
    else:
        form = EventForm(instance=event)
        formset = OccFormSet(queryset=periods)
    return {
        'form': form,
        'event': event,
        'formset': formset,
    }
