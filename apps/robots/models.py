from apps.common.models import WithSite
from django.db import models
from django.utils.translation import ugettext_lazy as _

class RobotsItem(models.Model):
    url = models.CharField(max_length=250)
    content = models.TextField(_('content'), blank=True)

