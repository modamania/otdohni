from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag("lunch/_map.html")
def draw_lunch_map(lunches):
    return {
        "api_key" : settings.YANDEX_MAPS_API_KEY,
        "lunches" : lunches,
    }
