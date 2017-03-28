from django.core.management.base import BaseCommand
from django.db.transaction import commit_on_success

from place.models import PlaceCategory, update_rate_categories


class Command(BaseCommand):

    help = "Recalculate rating for all places and categories"
    @commit_on_success
    def handle(self, *args, **kwargs):
        for category in PlaceCategory.objects.filter(is_published=True):
            update_rate_categories(category)
            self.stdout.write("Updated rating for %s category...\n" % category)
