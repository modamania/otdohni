from django import template
from gourmet.models import GourmetItem

register = template.Library()

@register.inclusion_tag('gourmet/_top5_gourmet.html')
def display_top5_gourmet():
    """Inclusion tag
    Returns latest 5 gourmet-item on main page
    """

    gourmet_items = GourmetItem.objects.live().order_by('-is_fixed','-pub_date')[:5]


    return {"gourmet_list" : gourmet_items}

