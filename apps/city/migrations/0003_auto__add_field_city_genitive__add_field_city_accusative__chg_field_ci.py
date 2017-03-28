# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'City.genitive'
        db.add_column('city_city', 'genitive', self.gf('django.db.models.fields.CharField')(default=None, max_length=50, null=True), keep_default=False)

        # Adding field 'City.accusative'
        db.add_column('city_city', 'accusative', self.gf('django.db.models.fields.CharField')(default=None, max_length=50, null=True), keep_default=False)

        # Changing field 'City.post'
        db.alter_column('city_city', 'post', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))


    def backwards(self, orm):
        
        # Deleting field 'City.genitive'
        db.delete_column('city_city', 'genitive')

        # Deleting field 'City.accusative'
        db.delete_column('city_city', 'accusative')

        # User chose to not deal with backwards NULL issues for 'City.post'
        raise RuntimeError("Cannot reverse this migration. 'City.post' and its values cannot be restored.")


    models = {
        'city.city': {
            'Meta': {'object_name': 'City'},
            'accusative': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True'}),
            'genitive': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'name_by_geoip': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20', 'null': 'True'}),
            'post': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20', 'null': 'True'}),
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
