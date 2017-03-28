# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Wolf'
        db.create_table('core_wolf', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_dt', self.gf('django.db.models.fields.DateField')()),
            ('to_dt', self.gf('django.db.models.fields.DateField')()),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('core', ['Wolf'])

        # Adding model 'Logo'
        db.create_table('core_logo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_dt', self.gf('django.db.models.fields.DateField')()),
            ('to_dt', self.gf('django.db.models.fields.DateField')()),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('core', ['Logo'])


    def backwards(self, orm):
        
        # Deleting model 'Wolf'
        db.delete_table('core_wolf')

        # Deleting model 'Logo'
        db.delete_table('core_logo')


    models = {
        'core.logo': {
            'Meta': {'ordering': "('from_dt', 'to_dt')", 'object_name': 'Logo'},
            'from_dt': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'to_dt': ('django.db.models.fields.DateField', [], {})
        },
        'core.wolf': {
            'Meta': {'ordering': "('from_dt', 'to_dt')", 'object_name': 'Wolf'},
            'from_dt': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'to_dt': ('django.db.models.fields.DateField', [], {})
        }
    }

    complete_apps = ['core']
