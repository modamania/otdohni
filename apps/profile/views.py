# -*- coding: utf-8 -*-
import os

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.comments.models import Comment
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Q

from friendship.models import Friendship
from profile.forms import ProfileEditForm, ProfileUserpicForm
from event.models import Event
from rating.models import Vote

from annoying.decorators import render_to


USERS_PER_PAGE = 50


@render_to('profile/profile_show.html')
def profile_show(request, user_id):
    profile = get_object_or_404(User, pk=user_id).profile
    can_edit = profile.can_edit(request.user)

    confirm_friend_list, not_confirm_friend_list, whait_confirm_friend_list = [], [], []
    
    confirm_friend_list = Friendship.objects.filter(Q(from_user=profile.user,) | Q(to_user=profile.user,), is_confirm=True)

    is_friend = False
    if profile.user == request.user:
        youself = True
        not_confirm_friend_list = Friendship.objects.filter(Q(from_user=request.user,), is_confirm=False)
        whait_confirm_friend_list = Friendship.objects.filter(Q(to_user=request.user,), is_confirm=False)
    else:
        youself = False
        if request.user.id in confirm_friend_list.values_list('from_user_id', flat=True):
            is_friend = True
        elif request.user.id in confirm_friend_list.values_list('to_user_id', flat=True):
            is_friend = True
    data = {
        'profile': profile,
        'can_edit': can_edit,
        'youself': youself,
        'is_friend': is_friend,
        'confirm_friend_list': confirm_friend_list,
        'not_confirm_friend_list': not_confirm_friend_list,
        'whait_confirm_friend_list': whait_confirm_friend_list,
    }

    if confirm_friend_list:
        friends_ids = []
        for f in confirm_friend_list:
            friends_ids.append(f.from_user if f.to_user == profile.user else f.to_user)
        # friend_events_list = Event.objects.filter(members__in=friends_ids)
        # data.update(friend_events_list=friend_events_list)
        
        #submit_date
        friend_actions = [comment for comment in Comment.objects.filter(user__in=friends_ids).order_by('-submit_date')[:10]]
        for vote in Vote.objects.filter(user__in=friends_ids)[:10]:
            friend_actions.append(vote)
        data.update(friend_actions=friend_actions)

    return data


@login_required
@render_to('profile/profile_form.html')
def profile_edit(request):
    profile = request.user.profile
    profile_userpic_form = None
    profile_edit_form = None
    if request.method == 'POST':
        if request.POST['this_form_for'] == 'userpic':
            profile_userpic_form = ProfileUserpicForm(request.POST, request.FILES)
            if profile_userpic_form.is_valid():
                if profile.userpic and \
                    os.path.isfile(profile.userpic.path):
                    profile.userpic.delete()
                profile.userpic = profile_userpic_form.cleaned_data['userpic']
                profile.save()
                return HttpResponseRedirect(reverse('profile.views.profile_show', \
                    args=[request.user.pk]))
        else:
            profile_edit_form = ProfileEditForm(request.POST)
            if profile_edit_form.is_valid():
                # 0_o - WTF ????
                profile.user.first_name = profile_edit_form.cleaned_data['first_name']
                profile.user.last_name = profile_edit_form.cleaned_data['last_name']
                profile.user.email = profile_edit_form.cleaned_data['email']
                profile.sex = profile_edit_form.cleaned_data['sex']
                profile.birthday = profile_edit_form.cleaned_data['birthday']
                profile.country = profile_edit_form.cleaned_data['country']
                profile.city = profile_edit_form.cleaned_data['city']
                profile.web_site = profile_edit_form.cleaned_data['web_site']
                profile.icq = profile_edit_form.cleaned_data['icq']
                profile.profession = profile_edit_form.cleaned_data['profession']
                profile.company = profile_edit_form.cleaned_data['company']
                profile.address = profile_edit_form.cleaned_data['address']
                profile.phone_number = profile_edit_form.cleaned_data['phone_number']
                profile.interest = profile_edit_form.cleaned_data['interest']
                profile.about = profile_edit_form.cleaned_data['about']
                password1 = profile_edit_form.cleaned_data['password1']
                password2 = profile_edit_form.cleaned_data['password2']
                if password1 == password2 and not password1 == '':
                    profile.user.set_password(password1)
                profile.user.save()
                profile.save()
                return HttpResponseRedirect(reverse('profile.views.profile_show', \
                    args=[request.user.pk]))
    if not profile_edit_form:
        data = {
            'first_name': profile.user.first_name,
            'last_name': profile.user.last_name,
            'email' : profile.user.email,
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
        profile_edit_form = ProfileEditForm(initial=data)
    if not profile_userpic_form:
        profile_userpic_form = ProfileUserpicForm({'userpic' : profile.userpic,})

    return {'profile_edit_form': profile_edit_form,
        'profile_userpic_form': profile_userpic_form,}

@login_required
@render_to('profile/user_list.html')
def user_list(request, only_friends=False):
    if only_friends:
        """user_list = request.user.friends.filter(is_confirm=True)\
                                .select_related('to_user__profile')\
                                .select_related('from_user__profile')\
                                .order_by('to_user__username')
        """
        user_list = Friendship.objects.filter(Q(from_user=request.user,) | Q(to_user=request.user,), is_confirm=True)
    else:
        user_list = User.objects.order_by('-last_login')
    if 'q' in request.GET:
        q = request.GET['q']
        if user_list and only_friends:
            user_list = user_list.filter(
                            Q(is_confirm=True),\
                            Q(to_user__username__icontains=q)|\
                            Q(to_user__email__icontains=q))
        elif user_list:
            user_list = user_list.filter(Q(username__icontains=q) | \
                Q(email__icontains=q))
    else:
        q = None
    paginator = Paginator(user_list, USERS_PER_PAGE)
    
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        users = paginator.page(page)
    except (EmptyPage, InvalidPage):
        users = paginator.page(paginator.num_pages)
    output = {
        'only_friends': only_friends,
        'users': users,
        'q': q,
    }
    if only_friends:
        output['TEMPLATE'] = 'profile/friend_list.html'
    return output
