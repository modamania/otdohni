# encoding: utf-8

from urlparse import urlparse
import urllib

from django.http import Http404
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.gis.utils import GeoIP

from annoying.functions import get_object_or_None
from grab import Grab

from core.views import flatpage
from city.models import City


class FlatpageFallbackMiddleware(object):
    def process_response(self, request, response):
        if response.status_code != 404:
            return response # No need to check for a flatpage for non-404 responses.
        try:
            return flatpage(request, request.path_info)
        # Return the original response if any errors happened. Because this
        # is a middleware, we can't assume the errors will be caught elsewhere.
        except Http404:
            return response
        except:
            if settings.DEBUG:
                raise
            return response

def get_real_ip(request):
    """
    Get IP from request.

    :param request: A usual request object
    :type request: HttpRequest
    :return: ipv4 string or None
    """
    # return '90.188.118.19' #Tomsk
    # return '195.208.131.1' #Nsk
    try:
        # Trying to work with most common proxy headers
        real_ip = request.META['HTTP_X_FORWARDED_FOR']
        return real_ip.split(',')[0]
    except KeyError:
        return request.META['REMOTE_ADDR']
    except Exception:
        # Unknown IP
        return None





class CityAndDeviceRedirect(object):
    redirect_to = None

    def set_redirect_by_ip(self, request):
        g = GeoIP()
        ip = get_real_ip(request)
        user_city = g.city(ip)
        target_city = None
        if user_city:
            target_city = get_object_or_None(City, name_by_geoip = user_city['city'])

        if not target_city:
            target_city = City.objects.get(is_default=True)

        target_domain = target_city.site.domain
        if not target_city.site.domain.startswith('http'):
            target_domain = 'http://%s' % target_domain
        target_url = urlparse(target_domain)
        request_url = urlparse('http://%s/' % request.get_host())

        if not target_url.netloc == request_url.netloc:
            self.redirect_to = target_city.site.domain


    def set_redirect_for_mobile_devices(self, request):
        #Здесь определять мобильный девайс и при необходсмости менять домен на мобильный
        headers = dict()
        for m in request.META:
            if m.startswith('HTTP_') and not m == 'HTTP_HOST' and not m == 'HTTP_CONNECTION':
                headers[m.replace('HTTP_', '').lower().replace('_', '-')] = request.META[m]
        get_params = urllib.urlencode(headers)
        g = Grab()
        g.go('http://phd.yandex.net/detect/?%s' % get_params)
        if g.doc.select('//yandex-mobile-info').exists():
            if not self.redirect_to:
                self.redirect_to = 'm.%s/' % request.get_host()
            else:
                self.redirect_to = 'm.%s' % self.redirect_to


    def process_request(self, request):
        if request.path.startswith('/admin'):
            return
        if not request.session.get('domain_set', False) \
                    or getattr(settings, 'CITY_AND_DEVICE_REDIRECT_DEBUG', False):
            self.set_redirect_by_ip(request)
            self.set_redirect_for_mobile_devices(request)
            request.session['domain_set'] = True

            if self.redirect_to:
                if self.redirect_to.endswith('/'):
                    self.redirect_to = self.redirect_to[:-1]
                return redirect('http://%s%s' % (self.redirect_to, request.get_full_path()))
