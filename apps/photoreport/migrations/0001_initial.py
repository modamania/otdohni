# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PhotoReport'
        db.create_table('photoreport_photoreport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_published', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('on_mainpage', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_event', self.gf('django.db.models.fields.DateTimeField')()),
            ('place_event', self.gf('django.db.models.fields.related.ForeignKey')(related_name='photoreports', to=orm['place.Place'])),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('photoreport', ['PhotoReport'])

        # Adding M2M table for field sites on 'PhotoReport'
        db.create_table('photoreport_photoreport_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('photoreport', models.ForeignKey(orm['photoreport.photoreport'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('photoreport_photoreport_sites', ['photoreport_id', 'site_id'])

        # Adding M2M table for field tags on 'PhotoReport'
        db.create_table('photoreport_photoreport_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('photoreport', models.ForeignKey(orm['photoreport.photoreport'], null=False)),
            ('tag', models.ForeignKey(orm['tagging.tag'], null=False))
        ))
        db.create_unique('photoreport_photoreport_tags', ['photoreport_id', 'tag_id'])

        # Adding model 'Photo'
        db.create_table('photoreport_photo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('photoreport', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='photos', null=True, to=orm['photoreport.PhotoReport'])),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
            ('caption', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('photoreport', ['Photo'])

        # Adding model 'PhotoReportUpload'
        db.create_table('photoreport_photoreportupload', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zip_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('photoreport', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['photoreport.PhotoReport'], null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('caption', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('photoreport', ['PhotoReportUpload'])


    def backwards(self, orm):
        
        # Deleting model 'PhotoReport'
        db.delete_table('photoreport_photoreport')

        # Removing M2M table for field sites on 'PhotoReport'
        db.delete_table('photoreport_photoreport_sites')

        # Removing M2M table for field tags on 'PhotoReport'
        db.delete_table('photoreport_photoreport_tags')

        # Deleting model 'Photo'
        db.delete_table('photoreport_photo')

        # Deleting model 'PhotoReportUpload'
        db.delete_table('photoreport_photoreportupload')


    models = {
        'photoreport.photo': {
            'Meta': {'ordering': "['-date_added', '-id']", 'object_name': 'Photo'},
            'caption': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'photoreport': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'photos'", 'null': 'True', 'to': "orm['photoreport.PhotoReport']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'photoreport.photoreport': {
            'Meta': {'ordering': "['-date_event']", 'object_name': 'PhotoReport'},
            'date_event': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'on_mainpage': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'place_event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photoreports'", 'to': "orm['place.Place']"}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'photoreports'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['tagging.Tag']"}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'photoreport.photoreportupload': {
            'Meta': {'object_name': 'PhotoReportUpload'},
            'caption': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photoreport': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['photoreport.PhotoReport']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'zip_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'place.place': {
            'Meta': {'ordering': "['name']", 'object_name': 'Place'},
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'places'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['place.PlaceCategory']"}),
            'date_promo_down': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_promo_up': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'expert_choice': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hits': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_new': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'logotype': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'logotype_alt': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'photo_alt': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'promo_is_up': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tagging': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'places'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['tagging.Tag']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'urlhits': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'place.placecategory': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'PlaceCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'main_tag': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'place_category'", 'unique': 'True', 'to': "orm['tagging.Tag']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'tagging': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['tagging.Tag']", 'null': 'True', 'blank': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'tagging.tag': {
            'Meta': {'ordering': "['name']", 'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['photoreport']