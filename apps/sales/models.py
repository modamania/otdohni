from django.db import models
from django.utils.translation import ugettext_lazy as _
from common.models import WithPublished
from sales.managers import CouponManager

class Coupon(WithPublished):
    """Coupon model"""

    title = models.CharField(_('title'), max_length=250)
    small_image = models.ImageField(_('small image'), upload_to="uploads/coupons/%Y/%d/", blank=True, null=True)
    image = models.ImageField(_('image'), upload_to="uploads/coupons/%Y/%d/")

    start_date = models.DateTimeField(_('start date'), blank=True, null=True)
    end_date = models.DateTimeField(_('end date'), blank=True, null=True)

    views = models.IntegerField(_('views'), default=0, editable=False)

    objects = CouponManager()

    class Meta:
        verbose_name = _('Coupon')
        verbose_name_plural = _('Coupons')

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        """Returns absolute url
        for coupon by id
        """
        return 'coupon_detail', {}, {"coupon_id" : self.pk}

    def update_views(self):
        """ Update views counter, increment views field """
        self.views+=1
        self.save()
        
        return self.views
