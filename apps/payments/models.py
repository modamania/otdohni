from django.db import models


class PaymentSystem(models.Model):
    name = models.CharField(max_length=255)
    display = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.display or self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(PaymentSystem, self).save(*args, **kwargs)