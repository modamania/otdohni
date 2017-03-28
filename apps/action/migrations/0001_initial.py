# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Action'
        db.create_table('action_action', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_published', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('short_text', self.gf('django.db.models.fields.TextField')()),
            ('full_text', self.gf('django.db.models.fields.TextField')()),
            ('is_completed', self.gf('django.db.models.fields.BooleanField')(default=False, max_length=13)),
        ))
        db.send_create_signal('action', ['Action'])

        # Adding M2M table for field sites on 'Action'
        db.create_table('action_action_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('action', models.ForeignKey(orm['action.action'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('action_action_sites', ['action_id', 'site_id'])

        # Adding model 'Poll'
        db.create_table('action_poll', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_published', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(related_name='polls', to=orm['action.Action'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('status', self.gf('django.db.models.fields.CharField')(default='SOON', max_length=10)),
        ))
        db.send_create_signal('action', ['Poll'])

        # Adding model 'WorkBidder'
        db.create_table('action_workbidder', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('poll', self.gf('django.db.models.fields.related.ForeignKey')(related_name='workbidders', to=orm['action.Poll'])),
            ('author_name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('action', ['WorkBidder'])


    def backwards(self, orm):
        
        # Deleting model 'Action'
        db.delete_table('action_action')

        # Removing M2M table for field sites on 'Action'
        db.delete_table('action_action_sites')

        # Deleting model 'Poll'
        db.delete_table('action_poll')

        # Deleting model 'WorkBidder'
        db.delete_table('action_workbidder')


    models = {
        'action.action': {
            'Meta': {'ordering': "['-pub_date']", 'object_name': 'Action'},
            'full_text': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'is_completed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'max_length': '13'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'short_text': ('django.db.models.fields.TextField', [], {}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'action.poll': {
            'Meta': {'ordering': "['-start_date']", 'object_name': 'Poll'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'polls'", 'to': "orm['action.Action']"}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'SOON'", 'max_length': '10'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'action.workbidder': {
            'Meta': {'ordering': "['id']", 'object_name': 'WorkBidder'},
            'author_name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'workbidders'", 'to': "orm['action.Poll']"}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['action']
