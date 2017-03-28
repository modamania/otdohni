from django import template
from tea.models import Interview
from django.conf import settings

register = template.Library()

@register.inclusion_tag("tea/_last_interviews.html")
def display_last_interviews(count=None, interview_id=None):

    if interview_id:
        cur_interview = interview_id
    else:
        cur_interview = Interview.objects.live().order_by('-pub_date')[0].id
    count = count if count else getattr(settings,"TEA_INTERVIEWS_COUNT", 10)

    interviews = Interview.objects.live().exclude(pk = cur_interview).order_by('?')[:count]

    return {
        "interviews" : interviews
    }