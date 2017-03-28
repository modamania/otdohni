from annoying.decorators import render_to
from django.views.decorators.cache import cache_page
from django.views.generic.list_detail import object_list, object_detail
from tea.models import Interview

@render_to('tea/overview.html')
def overview(request):
    """Returns actual interview and others"""

    try:
        interview = Interview.objects.live().order_by('-pub_date')[0]
    except IndexError:
        interview = None

    return {
        "interview": interview,
    }

#@cache_page(60 * 15)
def interview_list(request, **kwargs):
    """Returns all actual interviews
    Used generic list view
    """
    kwargs['queryset'] = Interview.objects.live().order_by('-pub_date')
    kwargs['template_object_name']  = "interviews"

    return object_list(request, **kwargs)


def interview_detail(request, interview_id, **kwargs):
    """ Returns interview detail page
    Use generic list view with overridden arguments
    """

    kwargs['queryset'] = Interview.objects.live()
    kwargs['object_id'] = interview_id

    return object_detail(request, **kwargs)
