# encoding: utf-8
from south.db import db
from south.v2 import SchemaMigration

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field sites on 'SitesAdmin'
        db.create_table('auth_user_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('sitesadmin', models.ForeignKey(User, null=False)),
            ('site', models.ForeignKey(Site, null=False))
        ))

        db.create_unique('auth_user_sites', ['sitesadmin_id', 'site_id'])


    def backwards(self, orm):
        db.delete_table('auth_user_sites')


    models = {
    }

    complete_apps = ['omskadmin']


