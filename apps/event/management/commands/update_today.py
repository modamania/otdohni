from django.core.management.base import BaseCommand
from django.db.transaction import commit_on_success
from django.contrib.sites.models import Site

from event.models import Event, TodayEvent, Occurrence


class Command(BaseCommand):

    help = "Update today events"
    output_transaction = True
    @commit_on_success
    def handle(self, *args, **kwargs):
        rotten_ids = set(TodayEvent.default_manager.all().values_list('event', flat=True))
        TodayEvent.default_manager.all().delete()
        new_ids = Event.objects.on_day_ids(site_id=None)
        events = Event.default_manager.filter(id__in=new_ids).select_related()
        for event in events:
            if event.id in rotten_ids:
                rotten_ids.remove(event.id)
            try:
                today_flag = event.today_flag
            except TodayEvent.DoesNotExist:
                today_flag = TodayEvent(event=event)
                today_flag.save()
            sites = list()
            for o in Occurrence.default_manager.filter(event=event):
                sites = sites + list(o.sites.all())
            today_flag.sites.clear()
            today_flag.sites.add(*set(sites))
        #TodayEvent.default_manager.filter(id__in=rotten_ids).delete()

