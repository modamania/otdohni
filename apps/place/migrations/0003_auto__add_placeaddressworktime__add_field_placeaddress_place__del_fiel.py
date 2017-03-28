# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PlaceAddressWorkTime'
        db.create_table('place_placeaddressworktime', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['place.PlaceAddress'])),
            ('mon', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tue', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('wed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('thu', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('fri', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sat', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sun', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('from_time', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('till_time', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('all_day', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('day_off', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('place', ['PlaceAddressWorkTime'])

        # Adding field 'PlaceAddress.place'
        db.add_column('place_placeaddress', 'place', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['place.Place']), keep_default=False)

        # Deleting field 'Place.address'
        db.delete_column('place_place', 'address_id')


    def backwards(self, orm):
        
        # Deleting model 'PlaceAddressWorkTime'
        db.delete_table('place_placeaddressworktime')

        # Deleting field 'PlaceAddress.place'
        db.delete_column('place_placeaddress', 'place_id')

        # Adding field 'Place.address'
        db.add_column('place_place', 'address', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['place.PlaceAddress'], unique=True, null=True, blank=True), keep_default=False)


    models = {
        'place.place': {
            'Meta': {'object_name': 'Place'},
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'places'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['place.PlaceCategory']"}),
            'date_promo_down': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_promo_up': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['place.Place']"})
        },
        'place.placeaddressworktime': {
            'Meta': {'object_name': 'PlaceAddressWorkTime'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['place.PlaceAddress']"}),
            'all_day': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'day_off': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fri': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'from_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mon': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sat': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sun': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'thu': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'till_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'tue': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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
