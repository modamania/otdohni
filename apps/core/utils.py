import os
import urllib
import urllib2
import json
import hashlib
import pickle
import pytils

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils import simplejson
from django.http import HttpResponse
from django.core.cache import cache
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

from sorl.thumbnail.main import DjangoThumbnail
from threadedcomments.models import ThreadedComment


def md5(word):
    md5 = hashlib.md5()
    md5.update(word)
    return md5.hexdigest() 

def sha(word):
    sha = hashlib.sha1()
    sha.update(word)
    return sha.hexdigest() 

def get_return_link(request, redirect_field_name=REDIRECT_FIELD_NAME):
    return_link = request.REQUEST.get(redirect_field_name, None)
    if not return_link:
        return_link = '/'

    return return_link

def ImgPreview(get_field, size, name=None):
    def wrapper(admin, obj):
        field = get_field(obj)
        if field:
            try:
                url = DjangoThumbnail(field, size).absolute_url
            except:
                url = ''
            return u'<img src="%s">' % url
        return u''
    wrapper.allow_tags = True
    wrapper.short_description = name if name else 'Preview'
    return wrapper

def as_json(func):
    def wrapped(request, *args, **kwargs):
        json = func(request, *args, **kwargs)
        return HttpResponse(simplejson.dumps(json))
    return wrapped


def method_cache(seconds=0):
    """
    A `seconds` value of `0` means that we will not memcache it.
    
    If a result is cached on instance, return that first.  If that fails, check 
    memcached. If all else fails, hit the db and cache on instance and in memcache. 
    
    ** NOTE: Methods that return None are always "recached".
    """
    def inner_cache(method):
        def x(instance, *args, **kwargs):
            key = hashlib.sha224(str(method.__module__) + str(method.__name__)\
                    + str(args) + str(kwargs)+'_siteid'+str(settings.SITE_ID)).hexdigest()
            
            if hasattr(instance, key):
                # has on class cache, return that
                result = getattr(instance, key)
            else:
                result = cache.get(key)
                
                if result is None:
                    # all caches failed, call the actual method
                    result = method(instance, *args, **kwargs)
                    
                    # save to memcache and class attr
                    if seconds and isinstance(seconds, int):
                        cache.set(key, pickle.dumps(result), seconds)
                    setattr(instance, key, result)
                else:
                    result = pickle.loads(result)
            return result
        return x
    return inner_cache

def func_cache(seconds=0):
    def inner_cache(func):
        def x(*args, **kwargs):
            key = hashlib.sha224(str(func.__module__) + str(func.__name__)\
                    + str(args) + str(kwargs)).hexdigest()
            result = cache.get(key)
            if result is None:
                # all caches failed, call the actual method
                result = func(*args, **kwargs)
                
                # save to memcache and class attr
                if seconds and isinstance(seconds, int):
                    cache.set(key, pickle.dumps(result), seconds)
            else:
                result = pickle.loads(result)
            return result
        return x
    return inner_cache


def slugify_filename(prefix):
    def _slugify(instance, filename):
        if '.' in filename:
            filename, ext = filename.rsplit('.', 1)
        else:
            ext = 'png'
        return os.path.join(prefix, '%s.%s'  % (pytils.translit.slugify(filename), ext))
    return _slugify


def get_json(url, params=[]):
    url = '%s?%s' % (url, urllib.urlencode(params))
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
        return None
    else:
        return json.loads(data)


def denormalize_comments(instance):
    if hasattr(instance, 'num_comments'):
        ctype = ContentType.objects.get_for_model(instance)
        filter={
            'content_type': ctype,
            'object_pk': instance.id,
            'is_public': True,
            'is_removed': False,
        }
        instance.num_comments = ThreadedComment.objects.filter(**filter).count()
        instance.save()

def denormalize_comments_async(data):
    if settings.USE_RQ:
        import django_rq

        if type(data) == dict:
            try:
                instance = data['content_type'].get_object_for_this_type(id=data['id'])
            except ObjectDoesNotExist:
                return
        else:
            instance = data

        queue = django_rq.get_queue('asap')
        queue.enqueue(denormalize_comments, instance)
