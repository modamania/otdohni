# -*- coding: utf-8 -*-
from django.contrib.sites.models import Site
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.conf import settings

from apps.blog.forms import PostAdminForm
from apps.blog.models import Post

from event.models import Event, Occurrence
from event.forms import EventForm, BaseOccurrenceFormSet, OccurrenceForm
from specprojects.models import SpecProject
from control.utils import can_access

from annoying.decorators import render_to
from pytils.translit import slugify

@can_access()
@render_to('control/blog_list.html')
def blog_list(request):
    if not request.user.has_module_perms('post'):
        return HttpResponseForbidden()
    post_list = Post.objects.select_related().all().order_by('-pub_date')
    if 'q' in request.GET:
        q = request.GET['q']
        post_list = post_list.filter(Q(title__icontains=q))
    else:
        q = ''
    paginator = Paginator(post_list, settings.EVENT_PAGINATION)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        page = paginator.page(page)
    except (EmptyPage, InvalidPage):
        page = paginator.page(paginator.num_pages)
    return {
        'page': page,
        'q': q
    }


@can_access()
@render_to('control/blog_show.html')
def blog_show(request, post_pk):
    if not request.user.has_module_perms('post'):
        return HttpResponseForbidden()
    post = get_object_or_404(Post, pk=post_pk)
    return {'post': post}


@can_access()
@render_to('control/blog_form.html')
def blog_form(request, post_pk=None):

    def save_post(form):
        post = form.save()
        if 'tags' in form.cleaned_data:
            for tag in form.cleaned_data['tags']:
                post.tags.add(tag)
        post.save()
        return post

    if not request.user.has_module_perms('post'):
        return HttpResponseForbidden()
    if post_pk:
        post = get_object_or_404(Post, pk=post_pk)
    else:
        post = None

    if request.method == 'POST':
        if not request.POST['slug']:
            slug = slugify(request.POST['title'])
            num_posts = len(Post.objects.filter(slug__contains=slug).all())
            if num_posts > 0:
                request.POST['slug'] = "%s-%s" % (slugify(request.POST['title']), num_posts)
            else:
                request.POST['slug'] = slugify(request.POST['title'])

        form = PostAdminForm(request.POST, instance=post)
        if form.is_valid():
            post = save_post(form)
            return HttpResponseRedirect(reverse(blog_show,  kwargs={'post_pk': post.pk}))
    else:
        form = PostAdminForm(instance=post)

    return {
        'form': form,
        'post': post
    }
