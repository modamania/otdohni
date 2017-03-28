# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'LogEntry'
        db.delete_table('common_logentry')


    def backwards(self, orm):
        
        # Adding model 'LogEntry'
        db.create_table('common_logentry', (
            ('action', self.gf('django.db.models.fields.IntegerField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='go51_logs', to=orm['profiles.Profile'])),
        ))
        db.send_create_signal('common', ['LogEntry'])


    models = {
        
    }

    complete_apps = ['common']
