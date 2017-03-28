# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.flatpages.models import FlatPage
from django.core.xheaders import populate_xheaders
from django.http import Http404, HttpResponse, HttpResponsePermanentRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.template import loader, RequestContext, Template
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_protect
from django.contrib.sites.models import Site, get_current_site
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from annoying.decorators import render_to
from annoying.functions import get_object_or_None

from event.models import Event, EventCategory


DEFAULT_TEMPLATE = 'flatpages/default.html'
EVENTS_TEMPLATE = Template('{% load event_tags %}{% events_random events today %} <div class="show-all-link"><a href="{{ sel_category_url }}">Все {{ sel_category.title|lower }} {% if today %}сегодня{% else %}скоро{% endif %}</a></div>')


def forbidden(request, template_name='403.html'):
    """
    return forbidden template with 403 http code
    """
    t = loader.get_template(template_name)

    return HttpResponseForbidden(t.render(RequestContext(request)))


@render_to('index.html')
def index(request):
    if request.is_ajax():
        ct = request.GET.get('ct', None)
        cs = request.GET.get('cs', None)
        if cs:
            if cs == 'all':
                events = Event.objects.soon().filter(publish_on_main=True)\
                    .order_by('?')
                sel_category = None
                sel_category_url = reverse('event_tab_soon')
            else:
                sel_category = get_object_or_None(EventCategory, id=cs)
                events = Event.objects.random_soon(sel_category)
                sel_category_url = reverse('event_soon', kwargs={'category_slug': sel_category.slug})
            today = False
        elif ct:
            if ct == 'all':
                events = Event.objects.today().filter(publish_on_main=True)\
                    .order_by('?')
                sel_category = None
                sel_category_url = reverse('event_list')
            else:
                sel_category = get_object_or_None(EventCategory, id=ct)
                events = Event.objects.random_today(sel_category)
                sel_category_url = reverse('event_category_list', kwargs={'category_slug': sel_category.slug})
            today = True

        context = RequestContext(request, {'events': events, "today": today, "sel_category":sel_category, "sel_category_url":sel_category_url})
        return HttpResponse(EVENTS_TEMPLATE.render(context))

# Это непонятный гемор связанный с городами
    #if request.META['GEOIP_CITY'] != '' and request.META['HTTP_HOST'] == 'zaotdih.ru':
 #    if request.META['HTTP_HOST'] == 'zaotdih.ru':
 #        city_id = 1
	# """
 #        if request.META['GEOIP_CITY'] == 'Omsk':
 #            city_id = 1
 #        if request.META['GEOIP_CITY'] == 'Novosibirsk':
 #            city_id = 2
	# """
 #        if city_id:
 #            redirect_domain = Site.objects.get(id = city_id).domain
 #            current_domain = request.META['HTTP_HOST']
 #            if redirect_domain != current_domain:
 #                return redirect('http://%s' % redirect_domain)
# Здесь гемор заканчивается

    category_today = EventCategory.objects.active_today(events__publish_on_main=True).order_by('order')
    category_soon = EventCategory.objects.active_soon().filter(events__isnull=False, events__publish_on_main=True).order_by('order')

    return {
            "category_today": category_today,
            "category_soon": category_soon,
            "qs_today": Event.objects.today().filter(publish_on_main=True).prefetch_related('category', 'members').order_by('?')[:7],
            "qs_soon": Event.objects.soon().filter(publish_on_main=True).prefetch_related('category', 'members').order_by('?')[:7],
    }


def flatpage(request, url):
    """
    Public interface to the flat page view.

    Models: `flatpages.flatpages`
    Templates: Uses the template defined by the ``template_name`` field,
        or :template:`flatpages/default.html` if template_name is not defined.
    Context:
        flatpage
            `flatpages.flatpages` object
    """
    if not url.startswith('/'):
        url = '/' + url
    site_id = get_current_site(request).id
    try:
        f = get_object_or_404(FlatPage,
            url__exact=url, sites__id__exact=site_id)
    except Http404:
        if not url.endswith('/') and settings.APPEND_SLASH:
            url += '/'
            f = get_object_or_404(FlatPage,
                url__exact=url, sites__id__exact=site_id)
            return HttpResponsePermanentRedirect('%s/' % request.path)
        else:
            raise
    return render_flatpage(request, f)

@csrf_protect
def render_flatpage(request, f):
    """
    Internal interface to the flat page view.
    """
    # If registration is required for accessing this page, and the user isn't
    # logged in, redirect to the login page.
    if f.registration_required and not request.user.is_authenticated():
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(request.path)
    if f.template_name:
        t = loader.select_template((f.template_name, DEFAULT_TEMPLATE))
    else:
        t = loader.get_template(DEFAULT_TEMPLATE)

    # To avoid having to always use the "|safe" filter in flatpage templates,
    # mark the title and content as already safe (since they are raw HTML
    # content in the first place).
    f.title = mark_safe(f.title)
    #TinyMCE add '/admin/flatpages/flatpage/add/' to all urls
    #startswith '{'. Next line fix this bug.
    f.content = f.content.replace('/admin/flatpages/flatpage/add/', '')
    f.content = Template(f.content).render(RequestContext(request))

    c = RequestContext(request, {
        'flatpage': f,
    })
    response = HttpResponse(t.render(c))
    populate_xheaders(request, response, FlatPage, f.id)
    return response