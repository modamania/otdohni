# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Interview'
        db.create_table('tea_interview', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_published', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('full_text', self.gf('tinymce.models.HTMLField')()),
        ))
        db.send_create_signal('tea', ['Interview'])


    def backwards(self, orm):
        
        # Deleting model 'Interview'
        db.delete_table('tea_interview')


    models = {
        'tea.interview': {
            'Meta': {'object_name': 'Interview'},
            'full_text': ('tinymce.models.HTMLField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        }
    }

    complete_apps = ['tea']
