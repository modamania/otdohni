"""
Custom Managers for generic rating models.

"""
from django.db.models import Manager, Q
from django.conf import settings
from django.contrib.sites.managers import CurrentSiteManager


from rating.models import Vote


class PlaceManager(CurrentSiteManager):

    def published(self):
        return self.filter(is_published=True)

    def sponsored(self):
        return self.filter(is_sponsor=True)

    def promouted(self):
        return self.published().filter(promo_is_up=True)

    def experted(self):
        return self.published().filter(expert_choice=True)

    def experted_promouted(self):
        return self.experted().filter(promo_is_up=True)

    def experted_no_promouted(self):
        return self.experted().filter(promo_is_up=False)

    def from_time(self, fr, all_day=True):
        return self.filter(
            Q(
                address__work_time__from_time__lte=fr,
            ) |
            Q(
                address__work_time__all_day=all_day
            ))

    def till_time(self, till, all_day=True):
        return self.filter(
            Q(
                address__work_time__till_time__gte=till,
            ) |
            Q(
                address__work_time__all_day=all_day,
            ))


class GalleryManager(Manager):

    def all_active(self):
        return self.filter(image__isnull=False).exclude(image="")
        #return super(GalleryManager, self).filter(image=True)

    def exists_active(self):
        return self.all_active().exists()
        #return super(GalleryManager, self).filter(image=True).exists()

    def count_active(self):
        return self.all_active().count()
        #return super(GalleryManager, self).filter(image=True).count()


class CategoryRateManager(Manager):

    def get_top(self, category):
        #WTF ???
        return category.ratecategories_set\
                .select_related()\
                .filter(num_votes__gte=settings.CHART_VOTE_MIN)\
                .order_by('-rate')

    def get_category_mean(self, category):
        places = category.places.all()
        total_score, total_items = 0, 0
        for place in places:
            rated_obj = Vote.objects.get_score(place)
            total_score += rated_obj['score']
            if rated_obj['num_votes']:
                total_items += 1
        try:
            mean = total_score / total_items
        except ZeroDivisionError:
            return 1
        return '%.2f' % mean

    def get_place_rating(self, place, category):
        rated_object = Vote.objects.get_score(place)
        num_votes = float(rated_object['num_votes'])
        score = float(rated_object['score'])
        vote_min = float(settings.CHART_VOTE_MIN)

        num_votes, score, vote_min, category_mean = map(
                lambda x: float(x), (
                    rated_object['num_votes'], rated_object['score'],
                    settings.CHART_VOTE_MIN
                ), category.category_mean
        )

        rate_place = (num_votes / (num_votes + vote_min))\
                        * score\
                        + (vote_min / (num_votes + vote_min))\
                        * category_mean
        return '%.2f' % rate_place, int(num_votes)
