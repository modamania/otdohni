# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from graber.models import HeroCategory

class Migration(DataMigration):

    def forwards(self, orm):
        for hc in orm.HeroCategory.objects.all():
            new_hc = HeroCategory()
            new_hc.category_id = hc.category_id
            new_hc.hero_name = hc.hero_name
            new_hc.save()


    def backwards(self, orm):
        "Write your backwards methods here."
        HeroCategory.objects.all().delete()


    models = {
        'city.city': {
            'Meta': {'ordering': "['name']", 'object_name': 'City'},
            'accusative': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'foursquare': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'genitive': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'name_by_geoip': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'post': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'city'", 'unique': 'True', 'to': "orm['sites.Site']"})
        },
        'payments.paymentsystem': {
            'Meta': {'object_name': 'PaymentSystem'},
            'display': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'place.foursquarephoto': {
            'Meta': {'object_name': 'FoursquarePhoto'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'photo_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'foursquare_photo'", 'to': "orm['place.Place']"}),
            'prefix': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'suffix': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'place.herocategory': {
            'Meta': {'object_name': 'HeroCategory'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['place.PlaceCategory']"}),
            'hero_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'place.place': {
            'Meta': {'ordering': "['name']", 'object_name': 'Place'},
            'can_buy_tiket': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['place.PlaceCategory']", 'null': 'True', 'blank': 'True'}),
            'date_mark_as_new': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'date_promo_down': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_promo_up': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'expert_choice': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'flash3d': ('django.db.models.fields.URLField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'foursquare_show': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'hits': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identity': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_sponsor': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'kinohod_place_id': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'last_foursquare_update': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'logotype': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'logotype_alt': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'main_address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'manual_changed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'num_comments': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'payments': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['payments.PaymentSystem']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'photo_alt': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'promo_is_up': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'score': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['sites.Site']", 'null': 'True', 'blank': 'True'}),
            'sponsor_logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'tagging': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'places'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['tagging.Tag']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'url_is_follow': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'urlhits': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'place.placeaddress': {
            'Meta': {'object_name': 'PlaceAddress'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['city.City']", 'null': 'True', 'blank': 'True'}),
            'district': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'fsid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'geopoint': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_main_office': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lat': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'lng': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'address'", 'to': "orm['place.Place']"})
        },
        'place.placeaddressworktime': {
            'Meta': {'ordering': "['id']", 'object_name': 'PlaceAddressWorkTime'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'work_time'", 'to': "orm['place.PlaceAddress']"}),
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
            'Meta': {'ordering': "['order', 'id']", 'object_name': 'PlaceCategory'},
            'category_mean': ('django.db.models.fields.FloatField', [], {'default': '1.0', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'main_tag': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'place_category'", 'unique': 'True', 'to': "orm['tagging.Tag']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'places': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['place.Place']", 'null': 'True', 'blank': 'True'}),
            'rating_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'tagging': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['tagging.Tag']", 'null': 'True', 'blank': 'True'})
        },
        'place.placegallery': {
            'Meta': {'object_name': 'PlaceGallery'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gallery'", 'to': "orm['place.Place']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'})
        },
        'place.tempgallery': {
            'Meta': {'object_name': 'TempGallery'},
            'gallery': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'temps'", 'to': "orm['place.PlaceGallery']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
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
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'})
        }
    }

    complete_apps = ['place']
