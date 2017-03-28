# -*- coding: utf-8 -*-

import urllib
import urllib2
import json
import time
import random

from django.conf import settings

from grab import Grab


def get_data(url, params=[]):
    time.sleep(random.random()*5)
    if not hasattr(params, 'apikey'):
        params['apikey'] = settings.KINOHOD_API_KEY
    url = url + urllib.urlencode(params)
    print url
    req = urllib2.Request(url, headers={
        'User-Agent': 'Mozilla/5.0',
        'Accept-Charset': 'utf-8',
        # "User-Agent": "XMLHttpRequest",
    })
    try:
        data = urllib2.urlopen(req).read()
    except urllib2.HTTPError as e:
        print 'HTTP Error'
        print e.code
        print e.reason
        print ''
        # exit(0)
        return None
    else:
        # print '-'*40
        # print data
        # print '-'*40
        return json.loads(data)

def get_movie_id(search):
    params = {
        'search': search.encode('utf-8'),
    }
    data = get_data('https://api.kinohod.ru/api/rest/partner/v1/movies?', params)
    if data:
        return data[0]['id']
    return None

def get_schedules(movie_id,  city_id, date=u'0'):
    params = {
        'city': city_id,
        'date': date,
    }
    data = get_data('https://api.kinohod.ru/api/rest/partner/v1/movies/%s/schedules?' % movie_id, params)
    return data or list()

def get_city_schedule(city_id):
    params = {
        'city': city_id,
    }
    data = get_data('https://api.kinohod.ru/api/rest/partner/v1/movies?', params)
    return data or list()

def get_image(image_name):
    url = 'https://api.kinohod.ru/o/%s/%s/%s' % (
        image_name[0:2],
        image_name[2:4],
        image_name,
    )
    g = Grab()
    g.go(url)
    if g.response.code == 200:
        return g.django_file()
    return None