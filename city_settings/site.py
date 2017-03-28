#!/usr/bin/python
import os

fl = open("sites", "r")
for line in fl.xreadlines():
	try:
		params = line.split(',')
		site_id = params[0][1:]
		domaen_prefix = params[1].split('.')[0][1:]
	except IndexError:
		exit(0)
	else:
		os.popen('cp omsk.py tmpl/%s.py' % domaen_prefix)
		os.popen('''replace "SITE_ID = 1" "SITE_ID = %s" "KEY_PREFIX = 'omsk_'" "KEY_PREFIX = '%s_'" -- tmpl/%s.py ''' % (site_id, domaen_prefix, domaen_prefix))
