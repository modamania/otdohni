#coding: utf-8
import mimetypes
from PIL import Image
import StringIO
import os


from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.servers.basehttp import FileWrapper
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.utils.encoding import smart_str
from django.views.generic.list_detail import object_detail, object_list
from django.views.decorators.cache import cache_page
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


from tagging.models import Tag
from tagging.utils import calculate_tag_cloud
from core import load_related_m2m
from watermarker.utils import watermark, determine_position
from watermarker.models import Watermark
from apps.common.models import ObjectSubscribe
from apps.photoreport.forms import SendToFriend


from models import PhotoReport, Photo


if 'mailer' in settings.INSTALLED_APPS:
    from mailer import send_mail
else:
    from django.core.mail import send_mail

#@cache_page(60 * 15)
def photoreport_list(request, tag_slug=None, **kwargs):
    queryset = PhotoReport.objects.active().select_related()

    tags = Tag.objects.filter(photoreports__is_published=True,
            ).distinct().annotate(total=Count('photoreports'))
    tags = calculate_tag_cloud(tags)
    kwargs['extra_context'] = {'tags': tags}

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        queryset = queryset.filter(tags=tag)
        kwargs['extra_context'] = {
                'tag': tag,
                'tags': tags,
        }

    load_related_m2m(queryset, 'tags')
    kwargs['queryset'] = queryset
    kwargs['template_object_name']  = "photoreport"

    return object_list(request, **kwargs)


def photoreport_detail(request, report_slug, **kwargs):
    photoreport = get_object_or_404(PhotoReport.objects.all(), slug=report_slug)
    kwargs['queryset'] = PhotoReport.objects.published()
    kwargs['slug'] = report_slug
    kwargs['template_object_name'] = 'photoreport'
    kwargs['extra_context'] = {'photos': photoreport.photos.all()}

    return object_detail(request, **kwargs)


def photo_detail(request, report_slug, photo_id, **kwargs):
    photo = get_object_or_404(Photo.objects.select_related().all(), pk=photo_id)

    if request.method == 'POST':
        form = SendToFriend(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            subject = _('The picture from your friend')

            d = {
                'name':data['name'],
                'friend': request.user.username,
                'friend_mail': request.user.email,
                'img_url': request.build_absolute_uri(),
                }
            content = _('%(name)s, %(friend)s (%(friend_mail)s) recommends you this picture %(img_url)s.') %  d

            from_email, to = settings.DEFAULT_FROM_EMAIL, data['email']
            send_mail(subject, content, from_email, [to])
            messages.success(request, _("Message is send!"))

    friend_form = SendToFriend()
    is_subscribed = 0
    if request.user.is_authenticated():
        _content_type_id = ContentType.objects.get(model='photo').id
        is_subscribed = list(ObjectSubscribe.objects.filter(user = request.user, object_pk = photo_id, content_type = _content_type_id))

    kwargs['queryset'] = Photo.objects.select_related().all()
    kwargs['object_id'] = photo_id
    kwargs['template_object_name'] = 'photo'
    kwargs['extra_context'] = {'photoreport': photo.photoreport, 'friend_form': friend_form, 'is_subscribed': is_subscribed, }

    return object_detail(request, **kwargs)

def photo_dwnl(request, photo_id, **kwargs):
    photo = get_object_or_404(Photo.objects.all(), pk=photo_id)
    path = photo.image.path # Get file path
    if not os.path.isfile(path):
        raise Http404
    content_type = mimetypes.guess_type(path)[0]

    try:
        wm = Watermark.objects.get(name='main', is_active=True)
    except Watermark.DoesNotExist:
        file = open(path,'r')
        length = os.path.getsize( path )  # not FileField instance
    else:
        try:
            target = Image.open(photo.image.path)
            mark = Image.open(wm.image.path)
        except IOError:
            file = open(path,'r')
            length = os.path.getsize( path )  # not FileField instance
        else:
            pos = determine_position('br', target, mark)
            file = StringIO.StringIO()
            target = watermark(target, mark, pos, opacity=1)
            target.save(file, format='JPEG')
            file.read = file.getvalue
            length = file.len

    response = HttpResponse(content=file.read(), content_type = content_type, mimetype='application/force-download')
    response['Content-Length'] = length
    response['Content-Disposition'] = 'attachment; filename=%s' %\
                                      smart_str(os.path.basename(path)) # same here

    return response

def photo_subscribe(request, report_slug, photo_id, **kwargs):
    _content_type_id = ContentType.objects.get(model='photo').id
    _site_id = Site.objects.get_current().id
    new_subscribe = ObjectSubscribe(user=request.user, object_pk=photo_id, site_id=_site_id, content_type_id=_content_type_id)
    new_subscribe.save()
    messages.success(request, _("You will be sent the e-mail notification about new comments!"))

    return HttpResponseRedirect(reverse('photo_detail', kwargs={'photo_id': photo_id,'report_slug': report_slug,}))

def photo_unsubscribe(request, report_slug, photo_id, **kwargs):
    _content_type_id = ContentType.objects.get(model='photo').id
    subscribe = get_object_or_404(ObjectSubscribe, user=request.user, object_pk=photo_id, content_type_id=_content_type_id)
    subscribe.delete()
    messages.success(request, _("You will no longer receive the notification about new comments!"))

    return HttpResponseRedirect(reverse('photo_detail', kwargs={'photo_id': photo_id,'report_slug': report_slug,}))
