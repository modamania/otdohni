#-*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from threadedcomments.models import  ThreadedComment
from tinymce import models as tinymce_models
from common.models import WithAuthors, WithPublished, WithSite
from news.managers import NewsItemManager


class NewsItem(WithAuthors, WithPublished, WithSite):
    """NewsItem class"""

    tags = models.ManyToManyField('tagging.Tag',
                            verbose_name=_('tags'),
                            related_name="news",
                            null=True, blank=True)
    title = models.CharField(_('title'),
                            max_length=250)
    slug = models.SlugField(unique=True)
    short_text = models.CharField(_('short_text'),
                            max_length=500)
    full_text = tinymce_models.HTMLField(_('full text'))
    image = models.ImageField(_('image'),
                            upload_to="uploads/news/%Y/%m",
                            null=True, blank=True)
    is_fixed = models.BooleanField(_('is fixed'),
                            default=False)
    num_comments = models.PositiveIntegerField(_('number of comments'),
                            default=0)

    objects = NewsItemManager()

    class Meta:
        verbose_name = _(u'NewsItem')
        verbose_name_plural = _(u'News')

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        """Returns absolute url
        for news item by slug
        """
        return u'news_detail', {}, {u"slug" : self.slug}

    def get_image(self):
        """Returns no_image.gif if image is blank"""
        return self.image if self.image else u'i/no_image.gif'


from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^tinymce\.models\.HTMLField"])
