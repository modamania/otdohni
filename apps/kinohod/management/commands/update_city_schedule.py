import datetime

from django.core.management.base import BaseCommand

from kinohod.utils import KinohodUtils


class Command(BaseCommand):

    help = "Update schedules of city from kinohod"
    def handle(self, *args, **kwargs):
        KinohodUtils().update_city()