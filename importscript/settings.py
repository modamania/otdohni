# -*- coding: utf-8 -*-

# Mysql
DB_USER = ''
DB_HOST = ''
DB_PASS = ''
DB_DATABASE = ''

DEBUG = False

PATH_FOR_OLD_SITE = '/home/steelkiwidev/projects/otdohni/public_html'
OLD_USERPIC_PATH = '/home/steelkiwidev/projects/otdohni/public_html/images/comprofiler/large'

try:
    from settings_local import *
except ImportError:
    pass

