#-*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from threadedcomments.models import  ThreadedComment
from tinymce import models as tinymce_models
from common.models import WithAuthors, WithPublished, WithSite
from blog.managers import PostManager


class Post(WithAuthors, WithPublished, WithSite):
    """Post class"""

    tags = models.ManyToManyField('tagging.Tag',
                            verbose_name=_('tags'),
                            related_name="blog",
                            null=True, blank=True)
    title = models.CharField(_('title'),
                            max_length=250)
    slug = models.SlugField(unique=True)
    short_text = models.CharField(_('short_text'),
                            max_length=500)
    full_text = tinymce_models.HTMLField(_('full text'))
    is_fixed = models.BooleanField(_('is fixed'),
                            default=False)
    num_comments = models.PositiveIntegerField(_('number of comments'),
                            default=0)

    objects = PostManager()

    class Meta:
        verbose_name = _(u'WebLogItem')
        verbose_name_plural = _(u'WebLog')

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        """Returns absolute url
        for blog item by slug
        """
        return u'post_detail', {}, {u"slug" : self.slug}


from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^tinymce\.models\.HTMLField"])
