from datetime import datetime
from django.db import models

class GourmetItemManager(models.Manager):
    """ GourmetItem model manager """

    def live(self):
        """ Returns live gourmet """
        return self.filter(pub_date__lte=datetime.now(), is_published=True)

    def published(self):
        """ Returns all published gourmet """
        return self.filter(is_published=True)

    def fixed(self):
        """ Returns fixed gourmet """
        return self.live().filter(is_fixed=True)
