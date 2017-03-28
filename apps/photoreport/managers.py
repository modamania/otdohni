from datetime import datetime
from django.db.models import Q
from django.contrib.sites.managers import CurrentSiteManager


class PhotoReportManager(CurrentSiteManager):
    """ PhotoReport model manager """

    def published(self):
        """ Returns all published photoreports """
        return self.filter(is_published=True)

    def soon(self):
        """ Returns photoreports is coming soon"""
        return self.published().filter(photos__exact=None)

    def active(self):
        """Returns photoreports where photos not empty and event date is over"""
        return self.published().filter(
                ~Q(
                    photos__exact=None
                ) , date_event__lt=datetime.now()
        )

    def new(self):
        """ Returns 3 active photoreports checked on mainpage """
        return self.active().order_by('-on_mainpage', '-date_event')[:3]

