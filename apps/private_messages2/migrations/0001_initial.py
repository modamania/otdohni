# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Chain'
        db.create_table('private_messages2_chain', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('private_messages2', ['Chain'])

        # Adding M2M table for field members on 'Chain'
        db.create_table('private_messages2_chain_members', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('chain', models.ForeignKey(orm['private_messages2.chain'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('private_messages2_chain_members', ['chain_id', 'user_id'])

        # Adding M2M table for field have_read on 'Chain'
        db.create_table('private_messages2_chain_have_read', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('chain', models.ForeignKey(orm['private_messages2.chain'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('private_messages2_chain_have_read', ['chain_id', 'user_id'])

        # Adding model 'Message'
        db.create_table('private_messages2_message', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='messages_sent', null=True, to=orm['auth.User'])),
            ('chain', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='messages', null=True, to=orm['private_messages2.Chain'])),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('sent_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('private_messages2', ['Message'])

        # Adding M2M table for field removed on 'Message'
        db.create_table('private_messages2_message_removed', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('message', models.ForeignKey(orm['private_messages2.message'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('private_messages2_message_removed', ['message_id', 'user_id'])


    def backwards(self, orm):
        
        # Deleting model 'Chain'
        db.delete_table('private_messages2_chain')

        # Removing M2M table for field members on 'Chain'
        db.delete_table('private_messages2_chain_members')

        # Removing M2M table for field have_read on 'Chain'
        db.delete_table('private_messages2_chain_have_read')

        # Deleting model 'Message'
        db.delete_table('private_messages2_message')

        # Removing M2M table for field removed on 'Message'
        db.delete_table('private_messages2_message_removed')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'private_messages2.chain': {
            'Meta': {'object_name': 'Chain'},
            'have_read': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'messages_chain'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"})
        },
        'private_messages2.message': {
            'Meta': {'object_name': 'Message'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'chain': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'messages'", 'null': 'True', 'to': "orm['private_messages2.Chain']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'removed': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'messages_removed'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'messages_sent'", 'null': 'True', 'to': "orm['auth.User']"}),
            'sent_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['private_messages2']
