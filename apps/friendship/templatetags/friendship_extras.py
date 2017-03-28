# -*- coding: utf-8 -*-
from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.utils.translation import gettext as _
from django.template.loader import render_to_string
from django.conf import settings

from friendship.models import Friendship

register = template.Library()


@register.filter
def are_friends(from_user, to_user):
    msg = ''
    try:

        friendship = Friendship.objects.none()
        if from_user == to_user:
            return msg
        if from_user.is_anonymous() or to_user.is_anonymous():
            return msg
        try:
            friendship = from_user.friends.get(to_user=to_user)
        except ObjectDoesNotExist:
            pass
        if not friendship:
            try:
                friendship = to_user.friends.get(to_user=from_user)
            except ObjectDoesNotExist:
                pass
        if friendship:
            if friendship.is_confirm:
                tmpl_name = 'break_friendship.html'
            elif friendship.from_user == from_user:
                tmpl_name = 'waiting_confirmation_friendship.html'
            else:
                tmpl_name = 'add_remove.html'
        else:
            tmpl_name = 'offerfriendship.html'
        msg = render_to_string('friendship_tags/%s' % tmpl_name, {'to_user': to_user,})

    except Exception as e:
        if settings.DEBUG:
            raise e

    return msg
