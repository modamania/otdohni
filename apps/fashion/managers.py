from datetime import datetime
from django.db import models

class FashionItemManager(models.Manager):
    """ FashionItem model manager """

    def live(self):
        """ Returns live fashion-item """
        return self.filter(pub_date__lte=datetime.now(), is_published=True)

    def published(self):
        """ Returns all published fashion-item """
        return self.filter(is_published=True)

    def fixed(self):
        """ Returns fixed fashion """
        return self.live().filter(is_fixed=True)
