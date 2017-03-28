from datetime import datetime
from django.db import models
from django.contrib.sites.managers import CurrentSiteManager

class NewsItemManager(CurrentSiteManager):
    """ NewsItem model manager """

    def live(self):
        """ Returns live news """
        return self.filter(pub_date__lte=datetime.now(), is_published=True)

    def published(self):
        """ Returns all published news """
        return self.filter(is_published=True)

    def fixed(self):
        """ Returns fixed news """
        return self.live().filter(is_fixed=True)
