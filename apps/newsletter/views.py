import logging
from datetime import date
from apps.newsletter.forms import SubscribeRequestForm, UnsubscribeRequestForm, UpdateForm
from apps.newsletter.models import Subscription, Newsletter

from django.contrib.contenttypes.models import ContentType
#from django.conf import settings
from django.http import Http404
from django.template.context import RequestContext
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from annoying.decorators import render_to, ajax_request

from apps.event.models import EventCategory, Event
from newsletter.models import *
from newsletter.forms import *

logger = logging.getLogger(__name__)

@login_required
@render_to('newsletter/subscription_subscribe_user.html')
def subscribe_user(request, confirm=False):

    already_subscribed = False
    instance, created = Subscription.objects.get_or_create(user=request.user)

    if instance.subscribed:
        already_subscribed = True
    elif confirm:
        instance.subscribed = True
        instance.save()

        messages.success(request,
            _('You have been subscribed to newsletter.'))
        logger.debug(_('User %(rs)s subscribed to %(my_newsletter)s.'),
                     {"rs":request.user, "my_newsletter": 'my_newsletter'})

    if already_subscribed:
        messages.info(request, _('You are already subscribed to newsletter.'))

    return {'action': 'subscribe',}


@login_required
@render_to('newsletter/subscription_unsubscribe_user.html')
def unsubscribe_user(request, confirm=False):

    not_subscribed = False

    try:
        instance = Subscription.objects.get(user=request.user)
        if not instance.subscribed:
            not_subscribed = True
        elif confirm:
            instance.subscribed=False
            instance.save()

            messages.success(request,
                _('You have been unsubscribed from newsletter.') )
            logger.debug(_('User %(rs)s unsubscribed from %(my_newsletter)s.'),
                         {"rs":request.user,
                          'my_newsletter':'my_newsletter'})

    except Subscription.DoesNotExist:
        not_subscribed = True

    if not_subscribed:
        messages.info(request,
            _('You are not subscribed to newsletter.'))

    return {'action': 'unsubscribe'}


@render_to('newsletter/subscription_subscribe.html')
def subscribe_request(request, confirm=False):
    if request.user.is_authenticated() or confirm:
        return subscribe_user(request, confirm)

    error = None
    if request.POST:
        new_data = request.POST.copy()
        new_data['ip'] = request.META.get('REMOTE_ADDR')
        form = SubscribeRequestForm(new_data)

        if form.is_valid():
            instance = form.save()

            try:
                instance.send_activation_email(action='subscribe')
            except Exception, e:
                logger.exception('Error %s while submitting email to %s.', e, instance.email)
                error = True
    else:
        form = SubscribeRequestForm(initial={'ip':request.META.get('REMOTE_ADDR')})

    return { 'form' : form,
            'error' : error,
            'action' :'subscribe' }



@render_to('newsletter/subscription_unsubscribe.html')
def unsubscribe_request(request, confirm=False):
    if request.user.is_authenticated() or confirm:
        return unsubscribe_user(request, confirm)

    error = None
    if request.POST:
        form = UnsubscribeRequestForm(request.POST)
        if form.is_valid():
            instance = form.instance
            try:
                instance.send_activation_email(action='unsubscribe')
            except Exception, e:
                logger.exception('Error %s while submitting email to %s.', e, instance.email)
                error = True
    else:
        form = UnsubscribeRequestForm()

    return {'form' : form,
            'error' : error,
            'action' :'unsubscribe'}


@render_to('newsletter/subscription_activate.html')
def update_subscription(request, email, action, activation_code=None):
    if not action in ['subscribe', 'unsubscribe']:
        raise Http404

    my_subscription = get_object_or_404(Subscription,
                                    email_field__exact=email)

    if activation_code:
        my_initial = {'user_activation_code' : activation_code, 'email_field' : my_subscription.email_field, 'ip' : request.META.get('REMOTE_ADDR')}
    else:
        my_initial = None

    print my_initial

    if request.POST:
        form = UpdateForm(request.POST, instance=my_subscription,
                          initial=my_initial)
        if form.is_valid():
            # Get our instance, but do not save yet
            subscription = form.save(commit=False)

            # If a new subscription or update, make sure it is subscribed
            # Else, unsubscribe
            if action == 'subscribe':
                subscription.subscribed=True
            else:
                subscription.unsubscribed=True

            logger.debug(_(u'Updated subscription %(subscription)s through the web.'), {'subscription':subscription})
            subscription.save()
    else:
        form = UpdateForm(instance=my_subscription, initial=my_initial)

        print form.is_valid()

        # If we are activating and activation code is valid and not already subscribed, activate straight away
        if action == 'subscribe' and form.is_valid() and not my_subscription.subscribed:
             subscription = form.save(commit=False)
             subscription.subscribed = True
             subscription.save()
        #
             logger.debug(_(u'Activated subscription %(subscription)s through the web.') % {'subscription':subscription})

    return {'form' : form,
            'action' : action }

@ajax_request
def filter_items(request):
    response = {}
    if request.is_ajax():
        if request.method == 'POST':
            #get date to filter item
            date_from = request.POST['from']
            date_to = request.POST['to']
            date_from=date_from.split('-')
            date_to=date_to.split('-')
            date_from = [int(i) for i in date_from ]
            date_to = [int(i) for i in date_to ]
            date_from=date(date_from[2],date_from[1],date_from[0])#year,month,day
            date_to=date(date_to[2],date_to[1],date_to[0])#year,month,day

            #get model and app to find current Model
            app = request.POST['app']
            model = request.POST['model']
            object_type = ContentType.objects.get(app_label=app, model=model)
            object_model = object_type.model_class()

            #list with items for period
            for_period = object_model.objects.filter(pub_date__range=(date_from, date_to))

            try:
                #while the newsletter editing we should exclude already chosen material

                id = int(request.POST['id'])
                newsletter = Newsletter.objects.get(id=id)
                chosen = object_model.objects.filter(newsletters__id = newsletter.id)
                for_period = for_period.exclude(id__in = chosen)
            except ValueError:
                chosen = []

            try:
                for_period = render_to_string('newsletter/admin/filtred_items.html',
                        {
                            'items':for_period,
                        },
                        context_instance = RequestContext(request))

                chosen = render_to_string('newsletter/admin/chosen_items.html',
                        {
                            'items':chosen,
                        },
                        context_instance = RequestContext(request))

                response =  {'succeed': 1,'for_period':for_period, 'chosen':chosen}
            except Exception, e:
                response = {'succeed': 0}
        else:
            response = {'succeed': 0}
    else:
        response = {'succeed': 0}
    return response

@ajax_request
def filter_events(request):
    response = {}
    if request.is_ajax():
        if request.method == 'POST':
            #get date to filter item
            date_from = request.POST['from']
            date_to = request.POST['to']
            date_from=date_from.split('-')
            date_to=date_to.split('-')
            date_from = [int(i) for i in date_from ]
            date_to = [int(i) for i in date_to ]
            date_from=date(date_from[2],date_from[1],date_from[0]) #year,month,day
            date_to=date(date_to[2],date_to[1],date_to[0]) #year,month,day

            #handle_category
            for_period = Event.objects.filter(pub_date__range=(date_from, date_to))
            category = []
            all_categories = []

            try:
                id = int(request.POST.get('category_id')) if request.POST.get('category_id') != 'null' else EventCategory.objects.all()[0].id
                category = EventCategory.objects.filter(id=id)
                for_period = for_period.filter(category__in=category)
                all_categories = EventCategory.objects.all()
                all_categories=all_categories.exclude(id__in=category)
            except EventCategory.DoesNotExist:
                for_period=[]

            #received saved chosen items with new chosen items to prevent hiding them from the select widget
            try:
                chosen_list = request.POST.getlist('chosen_list[]')
                chosen_list = [int(x) for x in chosen_list]
            except ValueError:
                pass

            try:
                #while editing the newsletter we should exclude already chosen material
                id = int(request.POST['id'])
                newsletter = Newsletter.objects.get(id=id)
                chosen = newsletter.events.all()
                for_period = for_period.exclude(id__in = (chosen_list if chosen_list else chosen))
            except ValueError:
                chosen = []

            try:
                current_category = render_to_string('newsletter/admin/chosen_items.html',
                        {
                        'items':category,
                        },
                        context_instance = RequestContext(request))

                all_categories = render_to_string('newsletter/admin/filtred_items.html',
                        {
                        'items':all_categories,
                        },
                        context_instance = RequestContext(request))

                for_period = render_to_string('newsletter/admin/filtred_items.html',
                        {
                        'items':for_period,
                        },
                        context_instance = RequestContext(request))

                chosen = render_to_string('newsletter/admin/chosen_items.html',
                        {
                        'items':chosen,
                        },
                        context_instance = RequestContext(request))

                response =  {
                    'succeed': 1,
                    'for_period':for_period,
                    'chosen':chosen,
                    'categories':all_categories,
                    'current_category':current_category
                }

            except Exception, e:
                response = {'succeed': 0, 'error': e}
        else:
            response = {'succeed': 0}
    else:
        response = {'succeed': 0}
    return response
