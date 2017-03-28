# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse

from friendship.models import Friendship
from core.utils import get_return_link

@login_required
def add_friendship(request, friend_pk):
    friend = get_object_or_404(User, pk=friend_pk)

    if request.user == friend:
        return HttpResponseRedirect(get_return_link(request))
    Friendship.objects.friendship_create(request.user, friend)

    return HttpResponseRedirect(reverse('profile_show', args=[friend.pk]))


@login_required
def remove_friendship(request, friend_pk):
    friend = get_object_or_404(User, pk=friend_pk)
    Friendship.objects.friendship_delete(request.user, friend)

    return HttpResponseRedirect(reverse('profile_show', args=[friend.pk]))
