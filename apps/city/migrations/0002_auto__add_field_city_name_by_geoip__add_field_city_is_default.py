# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'City.name_by_geoip'
        db.add_column('city_city', 'name_by_geoip', self.gf('django.db.models.fields.CharField')(default=None, max_length=20, null=True), keep_default=False)

        # Adding field 'City.is_default'
        db.add_column('city_city', 'is_default', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'City.name_by_geoip'
        db.delete_column('city_city', 'name_by_geoip')

        # Deleting field 'City.is_default'
        db.delete_column('city_city', 'is_default')


    models = {
        'city.city': {
            'Meta': {'object_name': 'City'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'name_by_geoip': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20', 'null': 'True'}),
            'post': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cityes'", 'to': "orm['sites.Site']"})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['city']
