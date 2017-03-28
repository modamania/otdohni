from datetime import datetime
from core.fields import RGBColorField
from specprojects.managers import SpecProjectManager
from django.core.urlresolvers import reverse
from django.db import models
from common.models import WithSite
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from tinymce import models as tinymce_models

class SpecProject(WithSite):
    is_in_top = models.BooleanField(default=False, verbose_name=_('top menu'))
    top_title = models.CharField(_('title in top menu'), max_length=250)
    color = RGBColorField(_('background color'))
    slug = models.SlugField()
    title = models.CharField(_('title'), max_length=250)
    description = tinymce_models.HTMLField(_('full text'), blank=True, null=True)
    date_modified = models.DateTimeField(auto_now=True, default=datetime.now, verbose_name=_('date of change'))

    objects = SpecProjectManager()

    class Meta:
        verbose_name = _('Special Project')
        verbose_name_plural = _('Special Projects')

    def __unicode__(self):
        return self.top_title

    def get_absolute_url(self):
        return reverse('spec_detail', args=[self.slug])

