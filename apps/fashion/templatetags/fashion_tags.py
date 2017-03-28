from django import template
from fashion.models import FashionItem

register = template.Library()

@register.inclusion_tag('fashion/_top5_fashionitem.html')
def display_top5_fashion():
    """Inclusion tag
    Returns latest 5 fashion on main page
    """

    fashion_items = FashionItem.objects.live().order_by('-is_fixed','-pub_date')[:5]


    return {"fashion_list" : fashion_items}
