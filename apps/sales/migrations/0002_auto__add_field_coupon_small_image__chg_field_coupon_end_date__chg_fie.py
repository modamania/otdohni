# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Coupon.small_image'
        db.add_column('sales_coupon', 'small_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True), keep_default=False)

        # Changing field 'Coupon.end_date'
        db.alter_column('sales_coupon', 'end_date', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Coupon.start_date'
        db.alter_column('sales_coupon', 'start_date', self.gf('django.db.models.fields.DateTimeField')(null=True))


    def backwards(self, orm):
        
        # Deleting field 'Coupon.small_image'
        db.delete_column('sales_coupon', 'small_image')

        # User chose to not deal with backwards NULL issues for 'Coupon.end_date'
        raise RuntimeError("Cannot reverse this migration. 'Coupon.end_date' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Coupon.start_date'
        raise RuntimeError("Cannot reverse this migration. 'Coupon.start_date' and its values cannot be restored.")


    models = {
        'sales.coupon': {
            'Meta': {'object_name': 'Coupon'},
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'small_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['sales']
