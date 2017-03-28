import random

from django import template
from django.conf import settings
from django.template.loader import get_template

from photoreport.models import PhotoReport, Photo


register = template.Library()


@register.inclusion_tag("photoreport/tags/photoreport_media.html",
                            takes_context=True)
def photoreport_media(context, request):
    return context.update({
        'STATIC_URL': context.get('STATIC_URL', settings.MEDIA_URL),
        'ADMIN_MEDIA_PREFIX': settings.ADMIN_MEDIA_PREFIX,
        'request':request,
    })


class PhotoWidgetNode(template.Node):
    def __init__(self, var_name):
        self.var_name = var_name

    def render(self, context):
        ph = template.resolve_variable(self.var_name, context)
        photos = Photo.objects.select_related().filter(photoreport=ph)
        context['photos'] = photos
        context['photoreport'] = ph
        t = get_template('photoreport/tags/photo_widget.html')
        c = context
        return t.render(c)


@register.tag('photo_widget')
def do_photo_widget(parser, token):
    """
    Syntax::

        {% photo_widget for [object] %}

    Example usage::

        {% photo_widget for photoreport %}

    """
    tokens = token.contents.split()
    tag_name = tokens[0]
    if len(tokens) != 3:
        raise template.TemplateSyntaxError, '%r tag requires 3 arguments' % tag_name
    if tokens[1] != 'for':
        raise template.TemplateSyntaxError, "%r tag's second " \
                                            "argument must be 'for'" % tag_name
    return PhotoWidgetNode(var_name=tokens[2])


@register.inclusion_tag('photoreport/tags/dummy.html')
def display_new_reports(template='photoreport/tags/new_photoreport.html'):
    """Return new photo reports and reports is coming soon"""
    new_reports = list(PhotoReport.objects.active().filter(on_mainpage=True))
    if len(new_reports):
        random.shuffle(new_reports)
        if len(new_reports) < 3:
            extra_count = 3 - len(new_reports)
            extra_new_reports = list(PhotoReport.objects.active()\
                .filter(on_mainpage=False).order_by('-date_event')[:extra_count])
            if extra_count > 1:
                random.shuffle(extra_new_reports)
            new_reports = new_reports + extra_new_reports
        else:
            new_reports = new_reports[:3]
    soon_reports = PhotoReport.objects.soon()
    return {
        'template': template,
        'new_reports': new_reports,
        'soon_reports': soon_reports
    }
