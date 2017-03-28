from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.event.models import EventCategory

class ExpertComment(models.Model):
    category = models.ForeignKey(EventCategory, related_name='essays',
        verbose_name=_('category'))
    comment = models.TextField(_('comment'))
    start_date = models.DateField(_('publication date'),
        blank=True,
        null=True)
    end_date = models.DateField(_('publication end date'),
        blank=True,
        null=True)
    is_published = models.BooleanField(default=False,
        verbose_name=_('comment is published'))
    author=models.ForeignKey('auth.User', null=True, blank=True, verbose_name=_('user'))

    class Meta:
        verbose_name = _('Expert comment')
        verbose_name_plural = _('Expert comments')

    def __unicode__(self):
        return u"%d %s" % (self.pk, self.author)
#
    def get_absolute_url(self):
        return reverse('expert_list', args=[self.pk])