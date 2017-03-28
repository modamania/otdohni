from urllib2 import urlopen

from django import template
from django.core.cache import cache
from django.contrib.sites.models import Site
from django.conf import settings

from xml.dom.minidom import parse


register = template.Library()

SUFFIX_TMP = {
    'vfrost': xrange(-100,-24),
    'frost': xrange(-24,-14),
    'vcold': xrange(-14,-4),
    'cold': xrange(-4, 1),
    'cool': xrange(1,6),
    'fresh': xrange(6,16),
    'warm': xrange(16,26),
    'hot': xrange(26,100),
}

SUFFIX_ICON = {
    'rain': [0,1,2,3,4,6,8,9,10,11,12,17,18,35,37,38,39,40,45,47],
    'sunny': [19,20,21,23,24,26,27,29,30,33,34],
    'snow': [5,7,13,14,15,16,41,42,43,46],
}

WEATER_URL = u'http://weather.yahooapis.com/forecastrss?w=%s&u=c'

# OMSK
# p = `RSXX0080`
# w = 2122641

# NOVOSIBIRSK
# p = `RSXX0077`
# w = 2122541

def _make_weather_url():
    site = Site.objects.get(id=settings.SITE_ID)
    city = site.city

    if not city:
        raise AttributeError('No city on this site')
    if not city.post:
        raise AttributeError('No "post" on this city')
    return WEATER_URL % city.post


def get_suffixes(tmp, icon):
    suffix_tmp = ''
    suffix_icon = ''
    suffix_special = ''
    for k,v in SUFFIX_TMP.items():
        if tmp in v:
            suffix_tmp = k
            break
    for k,v in SUFFIX_ICON.items():
        if icon in v:
            suffix_icon = k
            break
    return suffix_tmp, suffix_icon, suffix_special


def get_weather():
    u = urlopen(_make_weather_url())
    dom = parse(u)
    cond = dom.getElementsByTagName('yweather:condition')[0]
    forc = dom.getElementsByTagName('yweather:forecast')
    forc1, forc2 = forc[0:2]

    tmp = float(cond.attributes['temp'].value)
    icon = cond.attributes['code'].value
    low = float(forc1.attributes['low'].value)
    hi = float(forc2.attributes['high'].value)

    suffix_tmp, suffix_icon, suffix_special = get_suffixes(tmp, icon)
    tmp, low, hi = (u'%+.f' % tmp, u'%+.f' % low, u'%+.f' % hi)
    data = {
        'tmp': tmp,
        'icon': icon,
        'low': low,
        'hi': hi,
        'suffix_tmp': suffix_tmp,
        'suffix_icon': suffix_icon,
        'suffix_special': suffix_special,
        'active': True,
    }
    return data


@register.inclusion_tag('weather/show_weather.html', takes_context=True)
def show_weather(context):
    """Get weather data"""
    try:
        if getattr(settings, 'NO_GET_WEARTHER', False):
            raise Exception('In settings set no get wearther')
        data = cache.get('weather')
        if not data:
            data = get_weather()
            cache.set('weather', data, 30 * 60)
    except:
        data = {
            'tmp': 0.0,
            'icon': None,
            'low': 0.0,
            'hi': 0.0,
            'suffix_tmp': 'warm',
            'suffix_icon': 0,
            'active': False,
        }
    context.update(data)
    return context
