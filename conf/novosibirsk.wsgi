import sys
import os
import site

HOME_DIR = '/home/webmaster/www/otdohni'
sys.path.insert(0, HOME_DIR)
site.addsitedir(os.path.join(HOME_DIR, 'env/lib/python2.7/site-packages'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'novosibirsk_settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
