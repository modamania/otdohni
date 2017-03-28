# -*- coding: utf-8 -*-
from annoying.decorators import render_to
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import get_object_or_404
from functools import wraps
from django.utils.decorators import available_attrs
from django.core.urlresolvers import reverse
from django.db.models import Q

from django.conf import settings
from profile.models import Profile
from apps.control.forms import *


def can_access():
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if user.is_authenticated() and user.profile.access_to_dasboard:
                return view_func(request, *args, **kwargs)
            if user.is_authenticated() and user.is_superuser:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden()
        return wraps(view_func, assigned=available_attrs(view_func)) \
            (_wrapped_view)
    return decorator

@can_access()
@render_to('control/dashboard.html')
def dashboard(request):
    return {}


@can_access()
@render_to('control/user_list.html')
def user_list(request):
    if not request.user.has_module_perms('auth'):
        return HttpResponseForbidden()
    user_list = User.objects.all().order_by('username')
    if 'q' in request.GET:
        q = request.GET['q']
        user_list = user_list.filter(Q(username__icontains=q) | \
            Q(email__icontains=q))
    else:
        q = None
    paginator = Paginator(user_list, settings.USERS_PER_PAGE)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        users = paginator.page(page)
    except (EmptyPage, InvalidPage):
        users = paginator.page(paginator.num_pages)

    return {'users': users, 'q': q}


@can_access()
@render_to('control/user_form.html')
def user_edit(request, user_pk):
    if not request.user.has_perm('auth.change_user'):
        return HttpResponseForbidden()
    profile = get_object_or_404(Profile, pk=user_pk)
    if request.method == 'POST':
        form = ProfileForm(profile.user, request.POST)
        if form.is_valid():
            profile.user.username = form.cleaned_data['username']
            profile.user.first_name = form.cleaned_data['first_name']
            profile.user.last_name = form.cleaned_data['last_name']
            profile.user.email = form.cleaned_data['email']
            profile.user.is_active = form.cleaned_data['is_active']
            if 'userpic' in request.FILES:
                profile.userpic.delete()
                profile.userpic = request.FILES['userpic']
            profile.sex = form.cleaned_data['sex']
            profile.birthday = form.cleaned_data['birthday']
            profile.country = form.cleaned_data['country']
            profile.city = form.cleaned_data['city']
            profile.web_site = form.cleaned_data['web_site']
            profile.icq = form.cleaned_data['icq']
            profile.profession = form.cleaned_data['profession']
            profile.company = form.cleaned_data['company']
            profile.address = form.cleaned_data['address']
            profile.phone_number = form.cleaned_data['phone_number']
            profile.interest = form.cleaned_data['interest']
            profile.about = form.cleaned_data['about']
            profile.user.save()
            profile.save()

            return HttpResponseRedirect(reverse('control.views.user_list'))
    else:
        data = {
            'username': profile.user.username,
            'first_name': profile.user.first_name,
            'last_name': profile.user.last_name,
            'email' : profile.user.email,
            'is_active' : profile.user.is_active,
            'userpic' : profile.userpic,
            'sex' : profile.sex,
            'birthday' : profile.birthday,
            'country' : profile.country,
            'city' : profile.city,
            'web_site' : profile.web_site,
            'icq' : profile.icq,
            'profession' : profile.profession,
            'company' : profile.company,
            'address' : profile.address,
            'phone_number' : profile.phone_number,
            'interest' : profile.interest,
            'about' : profile.about,
        }
        form = ProfileForm(profile.user, initial=data)
    return {'form': form, 'profile': profile}
