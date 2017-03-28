from django.db import models

from event.models import Event
from place.models import Place


class KinohodSeance(models.Model):
    dt = models.DateTimeField()
    seance_id = models.TextField()
    event = models.ForeignKey(Event, related_name='kh_seances')
    place = models.ForeignKey(Place, related_name='kh_seances')

    def __unicode__(self):
        return '%s - %s - %s - %s' % (self.place.name, self.event.title, self.dt, self.seance_id)