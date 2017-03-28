import datetime

from django.core.management.base import BaseCommand
from django.db.transaction import commit_on_success

from place.models import Place


class Command(BaseCommand):

    help = "Toggle promo on the place"
    @commit_on_success
    def handle(self, *args, **kwargs):
        today = datetime.date.today()
        for place in Place.objects.filter(date_promo_down__lt=today, promo_is_up=True):
            place.promo_is_up = False
            place.save()

        for place in Place.objects.filter(date_promo_up=today, promo_is_up=False):
            place.promo_is_up = True
            place.save()

