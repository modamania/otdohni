from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_list, object_detail
from gourmet.models import GourmetItem
from django.conf import settings
from tagging.models import Tag


def gourmet_list(request, tag_slug=None, **kwargs):
    """ Return live gourmet-item
    Use generic list view with overridden arguments
    tag_slug - default None else return all gourmet with this tag
    """

    queryset = GourmetItem.objects.live().order_by('-pub_date')

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        queryset = queryset.filter(tags=tag)
        kwargs['extra_context'] = { "tag" : tag }

    kwargs['queryset'] = queryset
    kwargs['template_object_name']  = "gourmet"

    return object_list(request, **kwargs)

def gourmet_item(request, tag_slug=None, **kwargs):
    """ Return live gourmet-item
    Use generic list view with overridden arguments
    tag_slug - default None else return all gourmet with this tag
    """

    queryset = GourmetItem.objects.live().order_by('-pub_date')

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        queryset = queryset.filter(tags=tag)
        kwargs['extra_context'] = { "tag" : tag }

    kwargs['queryset'] = queryset
    kwargs['template_object_name']  = "gourmet"

    return object_list(request, **kwargs)

def gourmet_detail(request, slug, **kwargs):
    """ Returns gourmet-item detail page
    Use generic list view with overridden arguments
    """

    kwargs['queryset'] = GourmetItem.objects.live()
    kwargs['slug'] = slug
    
    return object_detail(request, **kwargs)
