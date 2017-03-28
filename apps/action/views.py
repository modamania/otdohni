# encoding: utf-8
from datetime import date

from django import http
from django.core.urlresolvers import reverse
from django.db.models.expressions import F
from django.views.generic.list_detail import object_list, object_detail
from django.template import Template, RequestContext
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import  csrf_exempt

from action.models import Action, Poll, WorkBidder, WorkBidderVote, Winner

from loginza import signals, models
from annoying.functions import get_object_or_None


LIKE_TEMPLATE = Template("{% include 'action/likes.html' with total_likes=work.total_likes user=user poll=poll %}")


def action_list(request, status='', *args, **kwargs):
    #status = request.GET.get('status', None)
    if not status or status == 'current':
        queryset = Action.objects.current()
        active = 'current'
    elif status == 'complete':
        queryset = Action.objects.completed()
        active = 'complete'
    kwargs['extra_context'] = {'active' : active}
    kwargs['queryset'] = queryset
    kwargs['template_object_name']  = 'action'
    return object_list(request, **kwargs)


def winners_list(request, *args, **kwargs):
    queryset = Winner.objects.all()
    kwargs['queryset'] = queryset
    kwargs['template_object_name']  = 'action'
    return object_list(request, **kwargs)


def action_detail(request, action_slug, *args, **kwargs):
    kwargs['queryset'] = Action.objects.all()
    kwargs['slug'] = action_slug
    kwargs['extra_context'] = {'now' : date.today()}
    return object_detail(request, **kwargs)


def poll_list(request, *args, **kwargs):
    status = request.GET.get('status', None)
    if not status or status == 'current':
        queryset = Poll.objects.current()
        status = 'current'
    elif status == 'soon':
        queryset = Poll.objects.soon()
    elif status == 'suspend':
        queryset = Poll.objects.suspend()
    elif status == 'complete':
        queryset = Poll.objects.completed()
    kwargs['extra_context'] = {'active' : status}
    kwargs['queryset'] = queryset
    kwargs['template_object_name'] = 'poll'
    kwargs['template_name'] = 'action/poll_list.html'
    return object_list(request, **kwargs)


# --- DEPRICATED !!! ---
def poll_detail(request, poll_id, *args, **kwargs):
    #action = get_object_or_404(Action, slug=action_slug)
    kwargs['queryset'] = Poll.objects.all()
    kwargs['object_id'] = poll_id
    kwargs['template_object_name'] = 'poll'
    user_votes = []
    if not request.user.is_anonymous():
        user_votes = WorkBidder.objects.filter(work_votes__user=request.user, poll__id=poll_id).distinct()
    kwargs['extra_context'] = {'now' : date.today(), 'user_votes' : user_votes}
    return object_detail(request, **kwargs)
# ---------------------


@csrf_exempt
def liked_work(request, poll_id, work_id):
    work = get_object_or_404(WorkBidder, id=work_id)
    poll = get_object_or_404(Poll, id=poll_id)
    if request.user.is_authenticated():
        # Где, блять, проверка может ли этот пользователь голосовать.
        if poll.can_add_like(request.user, work):
            print "CAN VOTE"
            Poll.objects.add_like(request.user, work)
            wb_vote = WorkBidderVote(user=request.user, workbidder=work)
            wb_vote.save()
        else:
            print 'NO Can Vote'
    if request.is_ajax():
        user_votes = []
        if not request.user.is_anonymous():
            user_votes = WorkBidder.objects.filter(work_votes__user=request.user, poll__id=poll_id).distinct()
        context = RequestContext(request, {'work': work,
                                'poll': poll,
                                'now': date.today(),
                                'user': request.user,
                                'user_votes' : user_votes,
                                })
        return http.HttpResponse(LIKE_TEMPLATE.render(context))

    # А здесь мы ищем куда бы перенапрвить пользователя.
    # Почему, блять, не сделать функцию которая будет это делать?
    # И не пихать такой код везде
    next = request.REQUEST.get('next', None)
    if not next:
        next = request.META.get('HTTP_REFERER', None)
    if not next:
        if hasattr(poll, 'get_absolute_url'):
            if callable(getattr(poll, 'get_absolute_url')):
                next = poll.get_absolute_url()
            else:
                next = poll.get_absolute_url
    if not next:
        next = '/'
    return http.HttpResponseRedirect(next)


def loginza_error_handler(sender, error, **kwargs):
    messages.error(sender, error.message)

signals.error.connect(loginza_error_handler)


def loginza_auth_handler(sender, user, identity, **kwargs):
    poll_id = kwargs.get('poll', None)
    work_id = kwargs.get('work', None)
    work = get_object_or_None(WorkBidder, id=work_id)
    poll = get_object_or_None(Poll, id=poll_id)

    next = sender.REQUEST.get('next', None)

    if poll_id:
        if not next:
            next = poll.get_absolute_url()

        try:
        # it's enough to have single identity verified to treat user as verified
            models.UserMap.objects.get(user=user, verified=True)
            Poll.objects.add_like(user, work)
        except models.UserMap.DoesNotExist:
            sender.session['users_complete_reg_id'] = identity.id
    else:
        next = reverse('main')

    return http.HttpResponseRedirect(next)

signals.authenticated.connect(loginza_auth_handler)


def loginza_login_required(sender, **kwargs):
    messages.warning(sender, u'Функция доступна только авторизованным пользователям.')

signals.login_required.connect(loginza_login_required)
