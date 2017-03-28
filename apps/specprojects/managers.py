from django.db import models

class SpecProjectManager(models.Manager):

    def top_menu(self):
        return self.filter(is_in_top=True)
