from specprojects.models import SpecProject
from annoying.decorators import render_to
from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_list
import settings

@render_to('specproject/spec_list.html')
def spec_list(request):
    spec_list = SpecProject.objects.all()

    return {
        'spec_list': spec_list,
        }


@render_to('specproject/spec_detail.html')
def spec_detail(request, spec_slug):
    specproject = get_object_or_404(SpecProject, slug=spec_slug)

    return {
        'specproject': specproject,
        }
