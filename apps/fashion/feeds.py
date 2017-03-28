#coding: utf-8
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils import feedgenerator
from fashion.models import FashionItem
from tagging.models import Tag
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

RSS_ITEM_COUNT = getattr(settings,'RSS_ITEM_COUNT', 30)

class FashionFeed(Feed):
    """FashionItem rss feed"""
    feed_type = feedgenerator.Rss201rev2Feed

    title = _(u'Мода — ОтдохниОмск.ру')
    
    def link(self):
        return reverse('fashion_list')

    def items(self, obj):
        return FashionItem.objects.live().order_by('-pub_date')[:RSS_ITEM_COUNT]

    def item_title(self, obj):
        return obj.title

    def item_link(self, obj):
        return obj.get_absolute_url()

    def item_description(self, obj):
        return render_to_string("fashion/feeds/fashionitem_detail.html", {"object" : obj})


class FashionByTagFeed(Feed):
    """ FashionItem rss feed by tag """
    feed_type = feedgenerator.Rss201rev2Feed
    
    def get_object(self, request, tag_slug):
        return get_object_or_404(Tag, slug=tag_slug)

    def link(self, obj):
        return reverse("fashion_tag_list", args=[obj.slug])

    def title(self, obj):
        return u'Мода — ОтдохниОмск.ру по тегу: %s' % obj.name

    def items(self, obj):
        return obj.fashion.live().order_by('-pub_date')[:RSS_ITEM_COUNT]

    def item_title(self, obj):
        return obj.title

    def item_link(self, obj):
        return obj.get_absolute_url()

    def item_description(self, obj):
        return render_to_string("fashion/feeds/fashionitem_detail.html", {"object" : obj})
