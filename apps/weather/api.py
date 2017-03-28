#!/usr/bin/env python
# TODO: nuke json dependency
from django.conf import settings

import logging

import urllib
import urllib2

from lxml import etree, objectify


logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

PARTNER_ID = getattr(settings, 'WEATHER_PARTNER_ID', 1069241775)
KEY = getattr(settings, 'WEATHER_KEY', '5955325f48444f83')
GEO  = getattr(settings, 'WEATHER_GEO', 'RSXX0080')

class Error(Exception):
    pass

class WeatherError(Exception):
    pass

class API(object):

    def __init__(self, geo=GEO, par=PARTNER_ID, key=KEY, **defaults):
        self.par = par
        self.key = key
        self.geo = geo
        self.URL = 'http://xoap.weather.com/weather/local/%s' % self.geo

        defaults['par'] = self.par
        defaults['key'] = self.key
        defaults['cc'] = '*'
        defaults['link'] = 'xoap'
        defaults['prod'] = 'xoap'
        defaults['unit'] = 'm'
        defaults['dayf'] = 5
        serialized = self._encode(defaults)
        logger.debug('About to call %s with params %r' % (self.URL, defaults))
        try:
            c = urllib2.urlopen(self.URL, serialized)
        except urllib2.URLError, e:
            raise WeatherError("Unexpected error while talking to server: %s" % (e, ))
        resp = c.read()
        root  = etree.fromstring(resp)
        objects = objectify.XML(resp)
        logging.debug('Result: %r' % resp)
        if root.tag== 'error':
            msg = root.find('err').text
            raise WeatherError(msg)
        self.response = resp
        self.root = root
        self.objects = objects

    # Stolen from Stripe
    def _encodeInner(self, d):
        """
        We want post vars of form:
        {'foo': 'bar', 'nested': {'a': 'b', 'c': 'd'}}
        to become:
        foo=bar&nested[a]=b&nested[c]=d
        """
        stk = []
        for key, value in d.items():
            if isinstance(value, dict):
                n = {}
                for k, v in value.items():
                    n["%s[%s]" % (key, k)] = v
                    stk.extend(self._encodeInner(n))
            else:
                stk.append((key, value))
        return stk

    # Stolen from Stripe
    def _encode(self, d):
        """
        Internal: encode a string for url representation
        """
        return urllib.urlencode(self._encodeInner(d))

    def get_temp(self, tag='day'):
        return self.root.find('cc/tmp').text

    def get_icon(self, tag='day'):
        pass
