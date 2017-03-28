from django.views.generic.list_detail import object_list
from lunch.models import LunchObject

def lunch_list(request, **kwargs):
    """Returns all actual lunches
    Used generic list view
    """
    kwargs['queryset'] = LunchObject.objects.live()
    kwargs['template_object_name']  = "lunch"

    return object_list(request, **kwargs)