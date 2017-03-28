from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from tinymce import models as tinymce_models
from common.models import WithAuthors, WithPublished, WithSite
from gourmet.managers import GourmetItemManager

class GourmetItem(WithAuthors, WithPublished, WithSite):
    """GourmetItem class"""

    title = models.CharField(_('title'), max_length=250)
    slug = models.SlugField(unique=True)
    short_text = models.CharField(_('short_text'), max_length=500)
    full_text = tinymce_models.HTMLField(_('full text'))
    image = models.ImageField(_('image'), upload_to="uploads/gourmet/%Y/%m", null=True, blank=True)
    tags = models.ManyToManyField('tagging.Tag', verbose_name=_('tags'), related_name="gourmet", null=True, blank=True)

    is_fixed = models.BooleanField(_('is fixed'), default=False)



    objects = GourmetItemManager()

    class Meta:
        verbose_name = _('Gourmet item')
        verbose_name_plural = _('Gourmet items')

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        """Returns absolute url
        for gourmet item by slug
        """
        return 'gourmet_detail', {}, {"slug" : self.slug}

    def get_image(self):
        """Returns no_image.gif if image is blank"""
        return self.image if self.image else 'i/no_image.gif'


from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^tinymce\.models\.HTMLField"])
