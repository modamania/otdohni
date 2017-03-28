# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'City.site'
        db.alter_column('city_city', 'site_id', self.gf('django.db.models.fields.related.OneToOneField')(default=1, unique=True, to=orm['sites.Site']))


    def backwards(self, orm):
        
        # Changing field 'City.site'
        db.alter_column('city_city', 'site_id', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, null=True, to=orm['sites.Site']))


    models = {
        'city.city': {
            'Meta': {'object_name': 'City'},
            'accusative': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'genitive': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'name_by_geoip': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'post': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'city'", 'unique': 'True', 'to': "orm['sites.Site']"})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['city']
