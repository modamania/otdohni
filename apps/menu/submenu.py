from django.core.urlresolvers import reverse

from place.models import PlaceCategory
from models import MenuItem


class Submenu(object):

    def place(self):
        return [MenuItem({'title': cat.__unicode__(), \
            'url': reverse('place.views.show_category', args=[cat.slug])}) \
            for cat in PlaceCategory.objects.select_related(depth=1).filter(is_published=True).all()]

