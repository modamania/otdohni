# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Coupon'
        db.create_table('sales_coupon', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('is_published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('views', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('sales', ['Coupon'])


    def backwards(self, orm):
        
        # Deleting model 'Coupon'
        db.delete_table('sales_coupon')


    models = {
        'sales.coupon': {
            'Meta': {'object_name': 'Coupon'},
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['sales']
