# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Tag.name'
        db.alter_column('tagging_tag', 'name', self.gf('django.db.models.fields.CharField')(max_length=25))


    def backwards(self, orm):
        
        # Changing field 'Tag.name'
        db.alter_column('tagging_tag', 'name', self.gf('django.db.models.fields.CharField')(max_length=150))


    models = {
        'tagging.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['tagging']
