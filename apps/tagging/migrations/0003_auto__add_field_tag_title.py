# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Tag.title'
        db.add_column('tagging_tag', 'title', self.gf('django.db.models.fields.CharField')(default='', max_length=250, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Tag.title'
        db.delete_column('tagging_tag', 'title')


    models = {
        'tagging.tag': {
            'Meta': {'ordering': "['name']", 'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'})
        }
    }

    complete_apps = ['tagging']
