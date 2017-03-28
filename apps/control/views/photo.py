# -*- coding: utf-8 -*-
from django.contrib.sites.models import Site
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import simplejson

from django.conf import settings

from annoying.decorators import render_to

from apps.photoreport.models import PhotoReport, Photo, PhotoReportUpload
from apps.photoreport.forms import PhotoreportForm, PhotoreportPhotoForm, PhotoReportUploadForm

from pytils.translit import slugify
from sorl.thumbnail.main import DjangoThumbnail

from control.utils import can_access
PHOTO_PAGINATION = int(getattr(settings, 'PHOTO_PAGINATION', '50'))

@can_access()
@render_to('control/photoreport_list.html')
def photoreport_list(request):
    if not request.user.has_module_perms('photoreport'):
        return HttpResponseForbidden()
    photoreport_list = PhotoReport.default_manager.all().order_by('-date_event')
    if 'q' in request.GET:
        q = request.GET['q']
        photoreport_list = photoreport_list.filter(Q(title__icontains=q))
    else:
        q = ''
    paginator = Paginator(photoreport_list, settings.EVENT_PAGINATION)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        photoreports = paginator.page(page)
    except (EmptyPage, InvalidPage):
        photoreports = paginator.page(paginator.num_pages)

    return {
        'photoreports': photoreports,
        'q': q
    }


@can_access()
@render_to('control/photoreport_show.html')
def photoreport_show(request, photoreport_pk):
    if not request.user.has_module_perms('photoreport'):
        return HttpResponseForbidden()
    photoreport = get_object_or_404(PhotoReport.default_manager.select_related(), pk=photoreport_pk)
    return {
        'photoreport': photoreport
        }

@can_access()
@render_to('control/photoreport_form.html')
def photoreport_form(request, photoreport_pk=None):

    def save_photoreport(form):
        photoreport = form.save()
        if 'tags' in form.cleaned_data:
            for tag in form.cleaned_data['tags']:
                photoreport.tags.add(tag)
        photoreport.save()
        return photoreport

    if not request.user.has_module_perms('photoreport'):
        return HttpResponseForbidden()
    if photoreport_pk:
        photoreport = get_object_or_404(PhotoReport.default_manager.select_related(), pk=photoreport_pk)
    else:
        photoreport = None

    if request.method == 'POST':
        if not request.POST['slug']:
            slug = slugify(request.POST['title'])
            num_reports = len(PhotoReport.default_manager.filter(slug__contains=slug).all())
            if num_reports > 0:
                request.POST['slug'] = "%s-%s" % (slugify(request.POST['title']), num_reports)
            else:
                request.POST['slug'] = slugify(request.POST['title'])
        else:
            slug = None
        #request.POST['sites'] = Site.objects.get_current().id
        form = PhotoreportForm(request.POST, request.FILES, instance=photoreport)

        if form.is_valid():
            # photoreport = save_photoreport(form)
            photoreport = form.save()
            photoreport.save()
            print photoreport

            if slug:
                return HttpResponseRedirect(reverse(photoreport_form,  kwargs={'photoreport_pk': photoreport.pk}))
            else:
                HttpResponseRedirect(reverse(photoreport_show,  kwargs={'photoreport_pk': photoreport.pk}))
    else:
        form = PhotoreportForm(instance=photoreport)

    if photoreport:
        photo_list = photoreport.photos.all()
        photo_upload_form = PhotoReportUploadForm(instance=photoreport)
    else:
        photo_list = None
        photo_upload_form = None

    return {
        'photoreport': photoreport,
        'photo_list': photo_list,
        'form': form,
        'upload_form': photo_upload_form
        }

@can_access()
@render_to('control/photoreport_photo_form.html')
def photoreport_photo_form(request, photoreport_pk, photo_pk=None):

    def save_photo(form):
        photo = form.save()
        photo.save()
        return photo

    if not request.user.has_module_perms('photoreport'):
        return HttpResponseForbidden()
    if photo_pk:
        photo = get_object_or_404(Photo, pk=photo_pk)
    else:
        photo = None

    if photoreport_pk:
        photoreport = get_object_or_404(PhotoReport.default_manager, pk=photoreport_pk)
    else:
        photoreport = None

    if request.method == 'POST':
        if not request.POST['slug']:
            slug = slugify(request.POST['title'])
            num_photos = len(Photo.objects.filter(slug__icontains=slug).all())
            if num_photos > 0:
                request.POST['slug'] = "%s-%s" % (slugify(request.POST['title']), num_photos)
            else:
                request.POST['slug'] = slugify(request.POST['title'])

        request.POST['photoreport'] = photoreport_pk

        form = PhotoreportPhotoForm(request.POST, request.FILES, instance=photo)

        if form.is_valid():
            photo = form.save()
            return HttpResponseRedirect(reverse(photoreport_show,  kwargs={'photoreport_pk': photoreport_pk}))
    else:
        form = PhotoreportPhotoForm(instance=photo)

    return {
        'photo': photo,
        'photoreport': photoreport,
        'form': form
    }

def photoreport_upload(request, photoreport_pk):

    if photoreport_pk:
        photoreport = get_object_or_404(PhotoReport.default_manager, pk=photoreport_pk)
    else:
        photoreport = None

    try:
        key = request.FILES['file']
        if key:
            upload = PhotoReportUpload(zip_file = request.FILES['file'],
                photoreport = photoreport, title = photoreport.title)
            photo = upload.save()
            f = photo.image
            thumb = DjangoThumbnail(f, (100, 100))
            data = [{
                'name': f.name,
                'url': f.url,
                'thumbnail_url': thumb.absolute_url,
                # 'thumbnail_url': settings.MEDIA_URL + "pictures/" + f.name.replace(" ", "_"),
                'delete_url': "reverse('upload-delete', args=[self.object.id])",
                'delete_type': "DELETE"
            }]
            response = JSONResponse(data, {}, response_mimetype(request))
            response['Content-Disposition'] = 'inline; filename=files.json'
            return response
    except KeyError, E:
        if settings.DEBUG:
            raise(E)
        else:
            pass
    return HttpResponse('error')


class JSONResponse(HttpResponse):
    """JSON response class."""
    def __init__(self,obj='',json_opts={},mimetype="application/json",*args,**kwargs):
        content = simplejson.dumps(obj,**json_opts)
        super(JSONResponse,self).__init__(content,mimetype,*args,**kwargs)

def response_mimetype(request):
    if "application/json" in request.META['HTTP_ACCEPT']:
        return "application/json"
    else:
        return "text/plain"