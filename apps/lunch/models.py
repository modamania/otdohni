from django.db import models
from common.models import WithPublished, WithMapAndAddress, WithSite
from lunch.mangers import LunchObjectManager
from django.utils.translation import ugettext_lazy as _
from tinymce import models as tinymce_models

class LunchObject(WithMapAndAddress, WithPublished, WithSite):
    """ LunchObject model inherited from WithMapAndAddress """

    title = models.CharField(_('title'), max_length=250)
    image = models.ImageField(_('logo'), blank=True, null=True, upload_to="uploads/lunch/%Y/%m/")
    description = tinymce_models.HTMLField(_('full text'), blank=True, null=True)
    label = models.CharField(_('label title'), max_length=250, null=True, blank=True)

    start_date = models.DateTimeField(_('start date'), blank=True, null=True)
    end_date = models.DateTimeField(_('end date'), blank=True, null=True)

    objects = LunchObjectManager()

    class Meta:
        verbose_name = _('Lunch Object')
        verbose_name_plural = _('Lunch Objects')

    def __unicode__(self):
        return self.title
    
