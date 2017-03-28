# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PlaceCategory'
        db.create_table('place_placecategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('main_tag', self.gf('django.db.models.fields.related.OneToOneField')(related_name='place_category', unique=True, to=orm['tagging.Tag'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
        ))
        db.send_create_signal('place', ['PlaceCategory'])

        # Adding M2M table for field tagging on 'PlaceCategory'
        db.create_table('place_placecategory_tagging', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('placecategory', models.ForeignKey(orm['place.placecategory'], null=False)),
            ('tag', models.ForeignKey(orm['tagging.tag'], null=False))
        ))
        db.create_unique('place_placecategory_tagging', ['placecategory_id', 'tag_id'])

        # Adding model 'PlaceAddress'
        db.create_table('place_placeaddress', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_main_office', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('geopoint', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('district', self.gf('django.db.models.fields.CharField')(default='none', max_length=12)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
        ))
        db.send_create_signal('place', ['PlaceAddress'])

        # Adding model 'Place'
        db.create_table('place_place', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['place.PlaceAddress'], unique=True, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('promo_is_up', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_promo_up', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('date_promo_down', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('place', ['Place'])

        # Adding M2M table for field category on 'Place'
        db.create_table('place_place_category', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('place', models.ForeignKey(orm['place.place'], null=False)),
            ('placecategory', models.ForeignKey(orm['place.placecategory'], null=False))
        ))
        db.create_unique('place_place_category', ['place_id', 'placecategory_id'])

        # Adding M2M table for field tagging on 'Place'
        db.create_table('place_place_tagging', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('place', models.ForeignKey(orm['place.place'], null=False)),
            ('tag', models.ForeignKey(orm['tagging.tag'], null=False))
        ))
        db.create_unique('place_place_tagging', ['place_id', 'tag_id'])

        # Adding model 'PlaceGallery'
        db.create_table('place_placegallery', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(related_name='gallery', to=orm['place.Place'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('place', ['PlaceGallery'])


    def backwards(self, orm):
        
        # Deleting model 'PlaceCategory'
        db.delete_table('place_placecategory')

        # Removing M2M table for field tagging on 'PlaceCategory'
        db.delete_table('place_placecategory_tagging')

        # Deleting model 'PlaceAddress'
        db.delete_table('place_placeaddress')

        # Deleting model 'Place'
        db.delete_table('place_place')

        # Removing M2M table for field category on 'Place'
        db.delete_table('place_place_category')

        # Removing M2M table for field tagging on 'Place'
        db.delete_table('place_place_tagging')

        # Deleting model 'PlaceGallery'
        db.delete_table('place_placegallery')


    models = {
        'place.place': {
            'Meta': {'object_name': 'Place'},
            'address': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['place.PlaceAddress']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'places'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['place.PlaceCategory']"}),
            'date_promo_down': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_promo_up': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'promo_is_up': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tagging': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'places'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['tagging.Tag']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'place.placeaddress': {
            'Meta': {'object_name': 'PlaceAddress'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'district': ('django.db.models.fields.CharField', [], {'default': "'none'", 'max_length': '12'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'geopoint': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_main_office': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'place.placecategory': {
            'Meta': {'object_name': 'PlaceCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_tag': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'place_category'", 'unique': 'True', 'to': "orm['tagging.Tag']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'tagging': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tagging.Tag']", 'symmetrical': 'False'})
        },
        'place.placegallery': {
            'Meta': {'object_name': 'PlaceGallery'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gallery'", 'to': "orm['place.Place']"})
        },
        'tagging.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['place']
