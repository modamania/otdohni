from django.db import models


class CityManager(models.Manager):
    def get(self, *args, **kwargs):
        if self.exists():
            return self.all()[0]
        return None
