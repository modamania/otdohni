# -*- coding: utf-8 -*-
import regex
import re

from django.core.management.base import BaseCommand
from django.db.transaction import commit_on_success

from django.contrib.sites.models import Site
from seo.models import Metadata


fields = (
    'title',
    'description',
    'keywords',
    'tooltip',
    'heading',
    'paginator',
    '_path',
)


class Command(BaseCommand):
    @commit_on_success
    def handle(self, *args, **kwargs):
    	print ''
    	print '-'*80
    	path_model = Metadata._meta.get_model('path')
    	origin_path_list = path_model.objects.filter(_site=1)

    	citys = open('citys.txt', 'r')

        # for s in Site.objects.all().exclude(id__in=(1,2,)):
        for s in citys.readlines():
        	if len(s) < 5:
        		continue
        	data = s.split('|')
        	id = int(data[0])
        	site = Site.objects.get(id=id)
	    	for p in origin_path_list:
	        	# print ''
	        	# print '--- %s ---' % data[1]
	    		filter = dict()
	    		filter['_site'] = site
	    		for f in fields:
		    		val = getattr(p, f)
		    		val = regex.subf(ur'Омск\b', data[1].decode('utf-8'), val)
		    		val = regex.subf(ur'Омске\b', data[2].decode('utf-8'), val)
		    		val = regex.subf(ur'Омска\b', data[3].decode('utf-8'), val)
		    		filter[f] = val
	    		new_p, is_create = path_model.objects.get_or_create(**filter)
	    		if is_create:
	    			print 'CREATE %s %s' % (site, filter['_path'],)
		    	
