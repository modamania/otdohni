import datetime

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.db.models import Min
from django.views.generic.date_based import object_detail
from django.views.decorators.cache import cache_page
from django.http import Http404
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_list, object_detail
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _

from common.htmlcalendar import get_dates_in_month, HTMLCalendar, add_navigation
from event.models import Event, EventCategory
from event.utils import obj_by_perm
from common.models import ObjectSubscribe
from rating.models import Vote
from core.utils import denormalize_comments_async

from annoying.decorators import render_to, ajax_request


#@cache_page(60 * 15)
def event_list(request, *args, **kwargs):
    kwargs['queryset'] = Event.objects.today().order_by('category')
    kwargs['template_object_name']  = 'event'
    kwargs['template_name'] = 'event/event_list_today.html'
    kwargs['extra_context'] = {'today': datetime.date.today()}
    if request.is_ajax():
        kwargs['template_name'] = 'event/ajax/event_list_ajax.html'
    return object_list(request, **kwargs)


#@cache_page(60 * 15)
@render_to("event/event_list_on_week.html")
def event_on_week(request, category_slug=None):
    if category_slug:
        category = get_object_or_404(EventCategory, slug=category_slug)
    else:
        category = None
    event_list =  Event.objects.on_week(category=category)
    return {'event_list' : event_list, 'category': category}


#@cache_page(60 * 15)
def event_soon(request, category_slug=None, *args, **kwargs):
    event_list = Event.objects.soon() \
        .annotate(ext_start_date=Min('periods__start_date')) \
        .order_by('category', 'ext_start_date')
    category = None
    if category_slug:
        category = get_object_or_404(EventCategory, slug=category_slug)
        event_list = event_list.filter(category=category)
    kwargs['queryset'] = event_list
    kwargs['extra_context'] = {'event_list' : event_list, 'category': category}
    kwargs['template_name'] = 'event/event_list_soon.html'

    return object_list(request, **kwargs)


#@cache_page(60 * 15)
def event_category_list(request, category_slug, *args, **kwargs):
    category = get_object_or_404(EventCategory, slug=category_slug)
    queryset = Event.objects.today().filter(category = category)
    kwargs['queryset'] = queryset
    kwargs['template_object_name'] = 'event'
    kwargs['template_name'] = 'event/event_list_by_category.html'
    kwargs['extra_context'] = {
        'category': category,
        'day': datetime.date.today()
    }
    return object_list(request, **kwargs)


class EventOnDay(ListView):
    model = Event
    context_object_name = 'event_list'
    template_name = 'event/event_list_day.html'

    #@method_decorator(cache_page(60 * 15))
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def get_date(self, year, month, day):
        try:
            date = datetime.date(*map(lambda x: int(x), (year, month, day)))
        except ValueError:
            raise Http404
        return date

    def get_queryset(self):
        self.date = self.get_date(*[self.kwargs[key]
                                    for key in ('year', 'month', 'day')])
        slug = self.kwargs['category_slug']
        if slug and slug != u'all':
            self.category = get_object_or_404(EventCategory, slug=slug)
        else:
            self.category = None
        return self.model.objects.on_day(dt=self.date, category=self.category)

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context.update({
            'day': self.date,
            'category': self.category,
        })
        return context


def event_detail(request, category_slug, event_id, *args, **kwargs):
    if request.user.is_authenticated() and request.user.events.filter(id=event_id).exists():
        event_visit_state = 'active'
    else:
        event_visit_state = 'inactive'
    category = get_object_or_404(EventCategory, slug=category_slug)
    kwargs['queryset'] = obj_by_perm(Event, request.user, category=category)
    kwargs['object_id'] = event_id
    kwargs['template_object_name'] = 'event'
    is_voted = 0
    if request.user.is_authenticated():
        is_voted = list(Vote.objects.filter(user = request.user, object_id = event_id))

    is_subscribed = 0
    content_type = ContentType.objects.get(model='event')
    if request.user.is_authenticated():
        is_subscribed = len(ObjectSubscribe.objects.filter(user = request.user, object_pk = event_id, content_type = content_type.id))

    kwargs['extra_context'] = {'event_visit_state': event_visit_state, 'is_voted': is_voted, 'is_subscribed': is_subscribed,}

    denormalize_comments_async({'content_type':content_type, 'id':event_id})

    return object_detail(request, **kwargs)


def event_visit(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if event in request.user.events.all():
        request.user.events.remove(event)
    else:
        request.user.events.add(event)
    return HttpResponseRedirect(event.get_absolute_url())


@ajax_request
@render_to('event/calendar_filter.html')
def calendar_navigation(request, year, month):
    choice = get_dates_in_month(int(year), int(month))
    calendar = HTMLCalendar(choice, reverse('event_list'))
    html = add_navigation(
            calendar.formatmonth(int(year), int(month)),
            reverse('calendar_navigation'),
            int(year), int(month))
    return {"calendar_filter": html}

def event_comment_subscribe(request, category_slug, event_id, **kwargs):
    _content_type_id = ContentType.objects.get(model='event').id
    _site_id = Site.objects.get_current().id
    new_subscribe = ObjectSubscribe(user=request.user, object_pk=event_id, site_id=_site_id, content_type_id=_content_type_id)
    new_subscribe.save()
    messages.success(request, _("You will be sent the e-mail notification about new comments!"))

    return HttpResponseRedirect(reverse('event_detail', kwargs={'event_id': event_id,'category_slug': category_slug,}) + '#comments')

def event_comment_unsubscribe(request, category_slug, event_id, **kwargs):
    _content_type_id = ContentType.objects.get(model='event').id
    subscribe = get_object_or_404(ObjectSubscribe, user=request.user, object_pk=event_id, content_type = _content_type_id)
    subscribe.delete()
    messages.success(request, _("You will no longer receive the notification about new comments!"))

    return HttpResponseRedirect(reverse('event_detail', kwargs={'event_id': event_id,'category_slug': category_slug,}) + '#comments')