from apps.common.models import ObjectSubscribe
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_list, object_detail
from news.models import NewsItem
from tagging.models import Tag
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import cache_page


#@cache_page(60 * 5)
def news_list(request, tag_slug=None, **kwargs):
    """ Return live news
    Use generic list view with overridden arguments
    tag_slug - default None else return all news with this tag
    """

    queryset = NewsItem.objects.live().order_by('-pub_date')

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        queryset = queryset.filter(tags=tag)
        kwargs['extra_context'] = { "tag" : tag }

    kwargs['queryset'] = queryset
    kwargs['template_object_name']  = "news"

    return object_list(request, **kwargs)


def news_detail(request, slug, **kwargs):
    """ Returns news detail page
    Use generic list view with overridden arguments
    """
    is_subscribed = 0
    news_id = get_object_or_404(NewsItem, slug=slug).id
    if request.user.is_authenticated():
        _content_type_id = ContentType.objects.get(model='newsitem').id
        is_subscribed = list(ObjectSubscribe.objects.filter(user = request.user, object_pk = news_id, content_type = _content_type_id))

    kwargs['queryset'] = NewsItem.objects.live()
    kwargs['slug'] = slug
    kwargs['extra_context'] = {'is_subscribed': is_subscribed, }

    return object_detail(request, **kwargs)

def news_comment_subscribe(request, slug, **kwargs):
    _content_type_id = ContentType.objects.get(model='newsitem').id
    _site_id = Site.objects.get_current().id
    news_id = get_object_or_404(NewsItem, slug=slug).id
    new_subscribe = ObjectSubscribe(user=request.user, object_pk=news_id, site_id=_site_id, content_type_id=_content_type_id)
    new_subscribe.save()
    messages.success(request, _("You will be sent the e-mail notification about new comments!"))

    return HttpResponseRedirect(reverse('news_detail', kwargs={'slug': slug,}))

def news_comment_unsubscribe(request, slug, **kwargs):
    news_id = get_object_or_404(NewsItem, slug=slug).id
    _content_type_id = ContentType.objects.get(model='newsitem').id
    subscribe = get_object_or_404(ObjectSubscribe, user=request.user, object_pk=news_id, content_type = _content_type_id)
    subscribe.delete()
    messages.success(request, _("You will no longer receive the notification about new comments!"))

    return HttpResponseRedirect(reverse('news_detail', kwargs={'slug': slug,}))
