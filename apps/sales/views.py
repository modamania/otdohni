from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_list, object_detail
from annoying.decorators import render_to
from sales.models import Coupon

def coupon_list(request, **kwargs):
    """Returns all actual coupons
    Used generic list view
    """
    kwargs['queryset'] = Coupon.objects.live()
    kwargs['template_object_name']  = "coupons"

    return object_list(request, **kwargs)


@render_to('sales/coupon_detail.html')
def coupon_detail(request, coupon_id, **kwargs):
    """ Returns coupon detail page """

    coupon = get_object_or_404(Coupon.objects.live(), id=coupon_id)
    coupon.update_views()

    return {
        "object" : coupon
    }



