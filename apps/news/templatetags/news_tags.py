from django import template
from news.models import NewsItem

register = template.Library()

@register.inclusion_tag('news/_top5_news.html')
def display_top5_news():
    """Inclusion tag
    Returns latest 5 news on main page
    """

    news_items = NewsItem.objects.live().order_by('-is_fixed','-pub_date')[:5]


    return {u"news_list" : news_items}
