# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'City'
        db.create_table('city_city', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cityes', to=orm['sites.Site'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('post', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('city', ['City'])


    def backwards(self, orm):
        
        # Deleting model 'City'
        db.delete_table('city_city')


    models = {
        'city.city': {
            'Meta': {'object_name': 'City'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
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
