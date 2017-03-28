# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'LunchObject.pub_date'
        db.add_column('lunch_lunchobject', 'pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now), keep_default=False)

        # Adding M2M table for field sites on 'LunchObject'
        db.create_table('lunch_lunchobject_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('lunchobject', models.ForeignKey(orm['lunch.lunchobject'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('lunch_lunchobject_sites', ['lunchobject_id', 'site_id'])


    def backwards(self, orm):
        
        # Deleting field 'LunchObject.pub_date'
        db.delete_column('lunch_lunchobject', 'pub_date')

        # Removing M2M table for field sites on 'LunchObject'
        db.delete_table('lunch_lunchobject_sites')


    models = {
        'lunch.lunchobject': {
            'Meta': {'object_name': 'LunchObject'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'description': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longtitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['lunch']
