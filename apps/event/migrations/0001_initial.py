# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'EventGenre'
        db.create_table('event_eventgenre', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=80)),
        ))
        db.send_create_signal('event', ['EventGenre'])

        # Adding model 'EventCategory'
        db.create_table('event_eventcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
        ))
        db.send_create_signal('event', ['EventCategory'])

        # Adding model 'Event'
        db.create_table('event_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='events', to=orm['event.EventCategory'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('description', self.gf('tinymce.models.HTMLField')(null=True, blank=True)),
            ('trailer', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('event', ['Event'])

        # Adding M2M table for field genre on 'Event'
        db.create_table('event_event_genre', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['event.event'], null=False)),
            ('eventgenre', models.ForeignKey(orm['event.eventgenre'], null=False))
        ))
        db.create_unique('event_event_genre', ['event_id', 'eventgenre_id'])

        # Adding model 'Occurrence'
        db.create_table('event_occurrence', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(related_name='periods', to=orm['event.Event'])),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(related_name='periods', to=orm['place.Place'])),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('start_time', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('event', ['Occurrence'])


    def backwards(self, orm):
        
        # Deleting model 'EventGenre'
        db.delete_table('event_eventgenre')

        # Deleting model 'EventCategory'
        db.delete_table('event_eventcategory')

        # Deleting model 'Event'
        db.delete_table('event_event')

        # Removing M2M table for field genre on 'Event'
        db.delete_table('event_event_genre')

        # Deleting model 'Occurrence'
        db.delete_table('event_occurrence')


    models = {
        'event.event': {
            'Meta': {'ordering': "['category', 'id']", 'object_name': 'Event'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'events'", 'to': "orm['event.EventCategory']"}),
            'description': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'genre': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'events'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['event.EventGenre']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'place': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'events'", 'symmetrical': 'False', 'through': "orm['event.Occurrence']", 'to': "orm['place.Place']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'trailer': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'event.eventcategory': {
            'Meta': {'object_name': 'EventCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'event.eventgenre': {
            'Meta': {'object_name': 'EventGenre'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'event.occurrence': {
            'Meta': {'object_name': 'Occurrence'},
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'periods'", 'to': "orm['event.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'periods'", 'to': "orm['place.Place']"}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'start_time': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'place.place': {
            'Meta': {'ordering': "['name']", 'object_name': 'Place'},
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['place.PlaceCategory']", 'null': 'True', 'blank': 'True'}),
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
            'rate_in_category': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tagging': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'places'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['tagging.Tag']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'urlhits': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'place.placecategory': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'PlaceCategory'},
            'category_mean': ('django.db.models.fields.FloatField', [], {'default': '1.0', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'main_tag': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'place_category'", 'unique': 'True', 'to': "orm['tagging.Tag']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'places': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['place.Place']", 'symmetrical': 'False', 'blank': 'True'}),
            'rating_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'tagging': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['tagging.Tag']", 'null': 'True', 'blank': 'True'})
        },
        'tagging.tag': {
            'Meta': {'ordering': "['name']", 'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['event']
