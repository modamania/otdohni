# -*- coding: utf-8 -*-
from apps.news.forms import NewsItemAdminForm
from apps.news.models import NewsItem
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
from pytils.translit import slugify

@can_access()
@render_to('control/news_list.html')
def news_list(request):
    if not request.user.has_module_perms('news'):
        return HttpResponseForbidden()
    news_list = NewsItem.objects.select_related().all().order_by('-pub_date')
    if 'q' in request.GET:
        q = request.GET['q']
        news_list = news_list.filter(Q(title__icontains=q))
    else:
        q = ''
    paginator = Paginator(news_list, settings.EVENT_PAGINATION)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        news = paginator.page(page)
    except (EmptyPage, InvalidPage):
        news = paginator.page(paginator.num_pages)

    return {
        'news': news,
        'q': q
    }


@can_access()
@render_to('control/news_show.html')
def news_show(request, news_pk):
    if not request.user.has_module_perms('news'):
        return HttpResponseForbidden()
    news = get_object_or_404(NewsItem, pk=news_pk)
    return {'news': news}


@can_access()
@render_to('control/news_form.html')
def news_form(request, news_pk=None):

    def save_news(form):
        news = form.save()
        if 'tags' in form.cleaned_data:
            for tag in form.cleaned_data['tags']:
                news.tags.add(tag)
        news.save()
        return news

    if not request.user.has_module_perms('news'):
        return HttpResponseForbidden()
    if news_pk:
        news = get_object_or_404(NewsItem, pk=news_pk)
    else:
        news = None

    if request.method == 'POST':
        if not request.POST['slug']:
            slug = slugify(request.POST['title'])
            num_news = len(NewsItem.objects.filter(slug__contains=slug).all())
            if num_news > 0:
                request.POST['slug'] = "%s-%s" % (slugify(request.POST['title']), num_news)
            else:
                request.POST['slug'] = slugify(request.POST['title'])

        form = NewsItemAdminForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            news = save_news(form)
            return HttpResponseRedirect(reverse(news_show,  kwargs={'news_pk': news.pk}))
    else:
        form = NewsItemAdminForm(instance=news)

    return {
        'form': form,
        'news': news
    }
