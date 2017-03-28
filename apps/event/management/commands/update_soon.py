from django.core.management.base import BaseCommand
from django.db.transaction import commit_on_success
from django.contrib.sites.models import Site

from event.models import Event, SoonEvent, Occurrence


class Command(BaseCommand):

    help = "Update today events"
    output_transaction = True
    @commit_on_success
    def handle(self, *args, **kwargs):
        rotten_ids = set(SoonEvent.default_manager.all().values_list('event', flat=True))
        SoonEvent.default_manager.all().delete()
        new_ids = Event.objects.soon_ids(site_id=None)
        events = Event.default_manager.filter(id__in=new_ids).select_related()
        for event in events:
            if event.id in rotten_ids:
                rotten_ids.remove(event.id)
            try:
                soon_flag = event.soon_flag
            except SoonEvent.DoesNotExist:
                soon_flag = SoonEvent(event=event)
                soon_flag.save()
            sites = list()
            for o in Occurrence.default_manager.filter(event=event):
                sites = sites + list(o.sites.all())
            soon_flag.sites.clear()
            soon_flag.sites.add(*set(sites))
        # SoonEvent.default_manager.filter(id__in=rotten_ids).delete()

