import pprint
import StringIO
import cgi

from django.utils import simplejson
from django.http import HttpResponse

from django.conf import settings


class json:

    def __init__(self, function):
        self._f = function

    def __call__(self, *args, **kwargs):

        response = self._f(*args, **kwargs)
        if settings.DEBUG and int(args[0].REQUEST.get('debug', False)):
            keys = args[0].REQUEST.getlist('debug_keys')
            if keys:
                response = self.get_keys(response, keys)
            s = StringIO.StringIO()
            pprint.pprint(response, s)
            return HttpResponse('<pre>'+s.getvalue()+'</pre>')
        else:
            return HttpResponse(simplejson.dumps(response),
                                mimetype='application/javascript')

    def get_keys(self, dirty_response, keys):
        response = []
        for item in dirty_response:
            o = {}
            for k in keys:
                if k in item:
                    v = item[k]
                    if type(v) == unicode:
                        v = cgi.escape(v).encode('ascii', 'xmlcharrefreplace')
                    o[k] = v
            response.append(o)
        return response