# -*- coding: utf-8 -*-
from annoying.decorators import render_to
from apps.control.utils import can_access
from apps.seo.models import Metadata
from django.contrib.sites.models import Site
from django.http import HttpResponseRedirect
from rollyourown.seo.admin import get_path_form
from rollyourown.seo.base import create_metadata_instance
from django.shortcuts import get_object_or_404

@can_access()
@render_to('control/seo_form.html')
def seo_form(request):
    site = Site.objects.get_current()
    url = request.GET['url']
    model_class = Metadata._meta.get_model('path')

    if request.method == 'POST':
        metadata, md_created = model_class.objects.get_or_create(_path=url, _site=Site.objects.get_current())
        metadata.title = request.POST['title']
        metadata.heading = request.POST['heading']
        metadata.keywords = request.POST['keywords']
        metadata.description = request.POST['description']
        metadata.tooltip = request.POST['tooltip']
        metadata.paginator = request.POST['paginator']
        metadata._site_id = Site.objects.get_current().id
        metadata.save()
        return HttpResponseRedirect(request.POST['_path'])
    else:
        form = get_path_form(Metadata)
        try:
            metadata = model_class.objects.get(_path=url, _site=Site.objects.get_current())
        except model_class.DoesNotExist:
            metadata = None
    return {
        'form': form,
        'site': site,
        'url': url,
        'obj':metadata
    }
