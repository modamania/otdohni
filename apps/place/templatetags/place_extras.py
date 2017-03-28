# -*- coding: utf-8 -*-
import datetime

from django import template
from django.template import Context, loader, Template
from django.utils.translation import ugettext as _
from django.contrib.sites.models import Site
from django.conf import settings
from django.template.loader import render_to_string

from core import load_related_m2m
from place.models import PlaceCategory, Place


register = template.Library()


@register.filter
def render_places_with_promo(place_list, seo):
    try:
        return render_places_with_template(place_list, seo,
                                'place/extended/places_list.html')
    except:
        return ''


@register.filter
def render_places_without_promo(place_list, seo):
    return render_places_with_template(place_list, seo,
                                'place/extended/places_list.html')


@register.filter
def render_places_as_sponsor(place_list, seo):
    try:
        return render_places_with_template(place_list, seo,
            'place/extended/place_list__as_sponsor.html')
    except:
        return ''


@register.filter
def render_places(place_list, seo):
    t = ''
    try:
        sort_place_list = []
        for place in place_list:
            if place.promo_is_up:
                sort_place_list.append(place)

        if sort_place_list:
            t += render_places_with_template(sort_place_list, seo,
                                'place/extended/places_list.html')

        sort_place_list = []

        for place in place_list:
            if not place.promo_is_up:
                sort_place_list.append(place)
        if sort_place_list:
            t += render_places_with_template(sort_place_list, seo,
                                'place/extended/places_list.html')
    except Exception as e:
        if settings.TEMPLATE_DEBUG:
            raise e

    return Template(t).render(Context({}))


def render_places_with_template(place_list, seo, tmpl):
    if place_list:
        current_site = Site.objects.get_current()
        load_related_m2m(place_list, 'tagging')
        t = loader.get_template(tmpl)
        c = Context({
            'place_list': place_list,
            'current_site': current_site,
            'seo': seo,
        })
        return t.render(c)
    return ''


@register.filter
def work_time(address):
    result = []
    work_time_list = address.work_time.all()

    for wt in work_time_list:
        result.append(wt.work_time())
    if not result:
        return ''
    return ', '.join(result)


@register.inclusion_tag('place/place_categories.html', takes_context=True)
def display_place_categories(context):
    """Return links to place categories"""
    categories = PlaceCategory.objects\
                                .select_related().filter(is_published=True)\
                                .order_by('order')
    request = context['request']
    current_site = Site.objects.get_current()
    context.update({
        'categories': categories,
    })
    return context


class GetTopRatingNode(template.Node):
    def __init__(self, object_name, limit):
        self.object_name, self.limit = object_name, limit

    def render(self, context):
        category_id = template.resolve_variable(self.object_name, context)

        top_list_exist = False
        top_list = None

        try:
            category = PlaceCategory.objects.get(id=category_id)
        except PlaceCategory.DoesNotExist:
            DEFAULT_TITLE = ''
            top_data = {
                'top_list_exist': top_list_exist,
                'rating_title': DEFAULT_TITLE,
            }
        else:
            top_category = PlaceCategory.objects.get_top(category)
            if top_category:
                top_list_exist = True
                top_list = top_category[:self.limit]

            DEFAULT_TITLE = _('Best of %s' % category.main_tag.name)
            top_data = {
                'top_list': top_list,
                'top_list_exist': top_list_exist,
                'rating_title': category.rating_title or DEFAULT_TITLE,
            }
        context.update(top_data)
        return loader.get_template('place/top_places.html').render(context)


@register.tag('top_places')
def do_get_top_rating(parser, token):
    """
    Syntax::

        {% top_places [object_id] [limit_objects] %}

    Example usage::

        {% top_places 1 5 %}

    """
    tokens = token.contents.split()
    tag_name = tokens[0]

    if len(tokens) != 3:
        raise template.TemplateSyntaxError(
                '%r tag requires 3 arguments' % tag_name)
    return GetTopRatingNode(object_name=tokens[1], limit=tokens[2])


@register.simple_tag
def new_place_widget():
    dt = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    dt = dt - datetime.timedelta(days=7)
    place_list = list(Place.objects.published() \
        .filter(promo_is_up=True, date_mark_as_new__gte=dt) \
        .order_by('-date_mark_as_new', 'name')[:10])
    if len(place_list) < 3:
        length = 3-len(place_list)
        place_list = place_list + list(Place.objects.published() \
        .filter(promo_is_up=True).exclude(id__in=[p.id for p in place_list]) \
        .order_by('-date_mark_as_new', 'name')[:length]) 
    data = {
        'place_list': place_list,
    }
    return render_to_string('place/new_place_widget.html', data)