from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_list, object_detail
from fashion.models import FashionItem
from django.conf import settings
from tagging.models import Tag

def fashion_list(request, tag_slug=None, **kwargs):
    """ Return live fashion
    Use generic list view with overridden arguments
    tag_slug - default None else return all fashion with this tag
    """

    queryset = FashionItem.objects.live().order_by('-pub_date')

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        queryset = queryset.filter(tags=tag)
        kwargs['extra_context'] = { "tag" : tag }

    kwargs['queryset'] = queryset
    kwargs['template_object_name']  = "fashion"

    return object_list(request, **kwargs)

def fashion_detail(request, slug, **kwargs):
    """ Returns fashion detail page
    Use generic list view with overridden arguments
    """

    kwargs['queryset'] = FashionItem.objects.live()
    kwargs['slug'] = slug
    
    return object_detail(request, **kwargs)
