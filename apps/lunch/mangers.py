from datetime import datetime
from django.db import models
from django.db.models import Q

class LunchObjectManager(models.Manager):
    """Manager for LunchObject model"""

    def live(self):
        """Returns active lunch objects"""
        now = datetime.now()
        return self.filter(Q(is_published=True, start_date__lte=now, end_date__gte=now) | \
                           Q(is_published=True, start_date__isnull=True, end_date__isnull=True))