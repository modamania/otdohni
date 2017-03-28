# -*- coding: utf-8 -*-
from datetime import date

from django.contrib.sites.models import Site
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.conf import settings

from action.models import Action, Poll, WorkBidder, Winner
from action.forms import ActionForm, ActionPollForm, WorkBidderForm, WinnerForm

from annoying.decorators import render_to
from pytils.translit import slugify

from control.utils import crop_image, can_access
PHOTO_PAGINATION = int(getattr(settings, 'PHOTO_PAGINATION', '50'))

@can_access()
@render_to('control/action_list.html')
def action_list(request):
    if not request.user.has_module_perms('action'):
        return HttpResponseForbidden()
    action_list = Action.objects.filter(sites=Site.objects.get_current().id).order_by('-pub_date')
    if 'q' in request.GET:
        q = request.GET['q']
        action_list = action_list.filter(Q(title__icontains=q))
    else:
        q = ''
    paginator = Paginator(action_list, settings.EVENT_PAGINATION)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        actions = paginator.page(page)
    except (EmptyPage, InvalidPage):
        actions = paginator.page(paginator.num_pages)

    return {
        'actions': actions,
        'q': q
    }

@can_access()
@render_to('control/action_show.html')
def action_show(request, action_pk):
    if not request.user.has_module_perms('action'):
        return HttpResponseForbidden()
    action = get_object_or_404(Action.objects.select_related(), pk=action_pk)
    return {
        'action': action,
        'now': date.today()
    }

@can_access()
@render_to('control/action_form.html')
def action_form(request, action_pk=None):

    if not request.user.has_module_perms('action'):
        return HttpResponseForbidden()
    if action_pk:
        action = get_object_or_404(Action, pk=action_pk)
    else:
        action = None

    if request.method == 'POST':
        if not request.POST['slug']:
            slug = slugify(request.POST['title'])
            num_actions = len(Action.objects.filter(slug__contains=slug).all())
            if num_actions > 0:
                request.POST['slug'] = "%s-%s" % (slugify(request.POST['title']), num_actions)
            else:
                request.POST['slug'] = slugify(request.POST['title'])
        else:
            slug = None
        #request.POST['sites'] = Site.objects.get_current().id
        form = ActionForm(request.POST, request.FILES, instance=action)

        if form.is_valid():
            action = form.save()

        if slug:
            return HttpResponseRedirect(reverse(action_form,  kwargs={'action_pk': action.pk}))
        else:
            return HttpResponseRedirect(reverse(action_show,  kwargs={'action_pk': action.pk}))
    else:
        form = ActionForm(instance=action)

    if action:
        poll_list = action.polls.all()
    else:
        poll_list = None

    return {
        'action': action,
        'poll_list': poll_list,
        'form': form
    }

@can_access()
@render_to('control/action_poll_form.html')
def action_poll_form(request, action_pk, poll_pk=None):

    if not request.user.has_module_perms('action'):
        return HttpResponseForbidden()

    if poll_pk:
        poll = get_object_or_404(Poll, pk=poll_pk)
    else:
        poll = None

    if action_pk:
        action = get_object_or_404(Action, pk=action_pk)
    else:
        action = None

    if request.method == 'POST':
        request.POST['action'] = action_pk
        form = ActionPollForm(request.POST, instance=poll)

        if form.is_valid():
            poll = form.save()
            return HttpResponseRedirect(reverse(action_show,  kwargs={'action_pk': action_pk}))
    else:
        form = ActionPollForm(instance=poll)

    if poll:
        workbidder_list = poll.workbidders.all()
    else:
        workbidder_list = None

    return {
        'poll': poll,
        'action': action,
        'workbidder_list': workbidder_list,
        'form': form
    }

@can_access()
@render_to('control/workbidder_form.html')
def workbidder_form(request, action_pk, poll_pk, work_pk=None):

    if not request.user.has_module_perms('action'):
        return HttpResponseForbidden()

    if work_pk:
        work = get_object_or_404(WorkBidder, pk=work_pk)
    else:
        work = None

    if poll_pk:
        poll = get_object_or_404(Poll, pk=poll_pk)
    else:
        poll = None

    if action_pk:
        action = get_object_or_404(Action, pk=action_pk)
    else:
        action = None

    if request.method == 'POST':

        request.POST['poll'] = poll_pk

        form = WorkBidderForm(request.POST, request.FILES, instance=work)

        if form.is_valid():
            work = form.save()
            return HttpResponseRedirect(reverse(action_poll_form,  kwargs={'action_pk': action_pk, 'poll_pk': poll_pk}))
    else:
        form = WorkBidderForm(instance=work)

    if action:
        workbidder_list = poll.workbidders.all()
    else:
        workbidder_list = None

    return {
        'poll': poll,
        'action': action,
        'workbidder_list': workbidder_list,
        'form': form
    }

@can_access()
@render_to('control/action_winner_form.html')
def action_winner_form(request, action_pk, winner_pk=None):

    if not request.user.has_module_perms('action'):
        return HttpResponseForbidden()

    action = get_object_or_404(Action, pk=action_pk)

    if winner_pk:
        winner = get_object_or_404(Winner, pk=winner_pk)
    else:
        winner = None

    if request.method == 'POST':
        form = WinnerForm(request.POST, request.FILES, instance=winner)

        if form.is_valid():
            winner = form.save(commit=False)
            winner.action = action
            winner.save()
            return HttpResponseRedirect(reverse(action_show,  kwargs={'action_pk': action_pk}))
    else:
        form = WinnerForm(instance=winner)

    return {
        'winner': winner,
        'action': action,
        'form': form
    }