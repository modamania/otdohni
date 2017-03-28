from datetime import datetime
from django.db import models


class CouponManager(models.Manager):
    """Manager for Coupon model"""

    def live(self):
        """Returns active coupons"""
        now = datetime.now()
        return self.filter(
            models.Q(
                is_published=True,
                start_date__lte=now,
                end_date__gte=now
            ) |
            models.Q(
                is_published=True,
                start_date__isnull=True,
                end_date__isnull=True
            )
        )
