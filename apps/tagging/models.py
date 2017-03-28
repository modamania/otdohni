from django.db import models
from django.utils.translation import ugettext_lazy as _

class Tag(models.Model):
    name = models.CharField(max_length=25)
    slug = models.SlugField()
    title = models.CharField(_('title'), max_length=250, default='', blank=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return "%s" % (self.name)
