from django.core.management.base import BaseCommand
from django.db.transaction import commit_on_success

from event.models import EventCategory, update_rate_categories


class Command(BaseCommand):

    help = "Recalculate rating for all places and categories"
    @commit_on_success
    def handle(self, *args, **kwargs):
        for category in EventCategory.objects.all():
            update_rate_categories(category)
            self.stdout.write("Updated rating for %s category...\n" % category)
