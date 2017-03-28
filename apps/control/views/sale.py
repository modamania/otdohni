# -*- coding: utf-8 -*-
from apps.sales.forms import CouponAdminForm
from apps.sales.models import Coupon
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
@render_to('control/sale_list.html')
def sale_list(request):
    if not request.user.has_module_perms('coupon'):
        return HttpResponseForbidden()
    sale_list = Coupon.objects.select_related().all().order_by('start_date')
    if 'q' in request.GET:
        q = request.GET['q']
        sale_list = sale_list.filter(Q(title__icontains=q))
    else:
        q = ''
    paginator = Paginator(sale_list, settings.EVENT_PAGINATION)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        sales = paginator.page(page)
    except (EmptyPage, InvalidPage):
        sales = paginator.page(paginator.num_pages)

    return {
        'sales': sales,
        'q': q
    }


@can_access()
@render_to('control/sale_show.html')
def sale_show(request, sale_pk):
    if not request.user.has_module_perms('coupon'):
        return HttpResponseForbidden()
    sale = get_object_or_404(Coupon, pk=sale_pk)
    return {'sale': sale}


@can_access()
@render_to('control/sale_form.html')
def sale_form(request, sale_pk=None):
    if not request.user.has_module_perms('coupon'):
        return HttpResponseForbidden()
    if sale_pk:
        sale = get_object_or_404(Coupon, pk=sale_pk)
    else:
        sale = None

    if request.method == 'POST':
        request.POST['sites'] = Site.objects.get_current().id
        form = CouponAdminForm(request.POST, request.FILES, instance=sale)
        if form.is_valid():
            sale = form.save()
        return HttpResponseRedirect(reverse(sale_show,  kwargs={'sale_pk': sale.pk}))
    else:
        form = CouponAdminForm(instance=sale)
    return {
        'form': form,
        'sale': sale
        }

@can_access()
def sale_delete(request, sale_pk):
    if not request.user.has_module_perms('coupon'):
        return HttpResponseForbidden()
    sale = get_object_or_404(Coupon, pk=sale_pk)
    sale.delete()
    return HttpResponseRedirect(reverse(sale_list))
