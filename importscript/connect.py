# -*- coding: utf-8 -*-
import MySQLdb
from django.conf import settings

DB_HOST = settings.DATABASES['otdohni_old']['HOST']
DB_USER = settings.DATABASES['otdohni_old']['USER']
DB_PASS = settings.DATABASES['otdohni_old']['PASSWORD']
DB_DATABASE = settings.DATABASES['otdohni_old']['NAME']

db = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASS, db=DB_DATABASE)
c = db.cursor()
c.execute("SET NAMES 'cp1251' collate cp1251_general_ci;")
c.execute("SET CHARACTER SET 'utf8'")
c.close()
