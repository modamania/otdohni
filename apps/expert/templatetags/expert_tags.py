from datetime import datetime, timedelta, date

from django.db.models.query_utils import Q
from django.utils.translation import ugettext as _
from django import template

from apps.event.models import EventCategory
from apps.expert.models import ExpertComment
from django.db.models import Min

register = template.Library()

@register.inclusion_tag('expert/tags/show_comment.html')
def show_expert_comment(category, period):

    start_day = date.today()
    end_day = start_day + timedelta(days=6)
    #for today
    if period == 1:
        expert = ExpertComment.objects.filter(category=category,\
                                    start_date__lte=start_day,\
                                    end_date__gte=start_day, is_published=True)

    #for week
    if period == 2:
        expert = ExpertComment.objects.filter(Q(start_date__range=(start_day,end_day))|\
                                              Q(end_date__range=(start_day,end_day))|\
                                              Q(start_date__lte=start_day,end_date__gte=end_day))\
                                                .filter(category=category, is_published=True)\
                                                .distinct()
    #soon
    if period == 3:

        #For the next start date that is not belong to the current week
#        start_day = date.today()
#        end_day = start_day + timedelta(days=6)
#        start_date_min = ExpertComment.objects.filter(start_date__gte=end_day,category=category, is_published=True)\
#                                                     .aggregate(Min('start_date'))['start_date__min']
#        expert = ExpertComment.objects.filter(start_date=start_date_min)

        #The same as for the week
        expert = ExpertComment.objects.filter(Q(start_date__range=(start_day,end_day))|\
                                              Q(end_date__range=(start_day,end_day))|\
                                              Q(start_date__lte=start_day,end_date__gte=end_day))\
        .filter(category=category, is_published=True)\
        .distinct()

    return {
        "expert":expert[0] if expert else None,
    }

