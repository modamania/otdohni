from django import template
from django.template.loader import render_to_string
from django.contrib import comments
from django.contrib.contenttypes.models import ContentType

from place.models import Place
from event.utils import earliest_date
from event.models import SoonEvent

register = template.Library()


@register.filter
def userpic(profile, size=None):
    try:
        if profile.userpic:
            if size:
                return profile.userpic.extra_thumbnails[size]
            else:
                return profile.userpic.thumbnail
        else:
            if size:
                return '/static/i/no_avatar_%s.png' % size
            else:
                return '/static/i/no_avatar.png'
    except:
        return ''


def get_category(obj):
    if not obj:
        return ''
    if hasattr(obj, 'category'):
        try:
            category = obj.category.all()
        except AttributeError:
            category = (obj.category, )
    else:
        model = ContentType.objects.get_for_model(obj).model_class()
        category = (unicode(model._meta.verbose_name), )
    return category


def get_comments_qs(user):
    filter = {
        'user_id': user.id,
        'is_public': True,
        'is_removed': False,
    }
    comment_model = comments.get_model()
    return comment_model.objects.filter(**filter).order_by('-submit_date')


@register.simple_tag
def count_comments(user):
    qs = get_comments_qs(user)
    return qs.count()


@register.simple_tag
def show_comments(user):
    html = []
    qs = get_comments_qs(user)
    for comment in qs:
        obj = comment.content_object
        if not obj:
            continue
        category = get_category(obj)
        data = {
            'comment' : comment,
            'obj' : obj,
            'category': category,
        }
        html.append(render_to_string('profile/extended/show_comment.html', data))
    return ''.join(html)


@register.simple_tag
def show_votes(user):
    html = []
    for vote in user.votes.all():
        obj = vote.object
        category = get_category(obj)
        data = {
            'vote' : vote,
            'obj' : obj,
            'category' : category,
        }
        html.append(render_to_string('profile/extended/show_vote.html', data))
    return ''.join(html)


def render_events_list(events, template='show_event.html'):
    html = []
    for event in events:
        shedule = event.periods.active()
        place_ids = shedule.values_list('place', flat=True)
        places_list = Place.objects.filter(id__in=place_ids)

        data = {
            'event' : event,
            'places_list' : places_list,
        }
        html.append(render_to_string('profile/extended/%s' % template, data))
    return ''.join(html)
    

@register.simple_tag
def show_soon_events(user):
    events = []
    for event in user.events.all().order_by('-start_date', 'title'):
        if event.is_soon:
            events.append(event)
    return render_events_list(events)


@register.simple_tag
def show_now_events(user):
    events = []
    for event in user.events.all().order_by('-start_date', 'title'):
        if not event.is_soon:
            events.append(event)
    return render_events_list(events)
