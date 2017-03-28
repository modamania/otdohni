# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Subscriber'
        db.create_table('newsletter_subscriber', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal('newsletter', ['Subscriber'])

        # Adding model 'Newsletter'
        db.create_table('newsletter_newsletter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('text', self.gf('tinymce.models.HTMLField')()),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
            ('subscribe_template', self.gf('django.db.models.fields.related.ForeignKey')(default=2L, related_name='subcribe_template', to=orm['newsletter.EmailTemplate'])),
            ('unsubscribe_template', self.gf('django.db.models.fields.related.ForeignKey')(default=3L, related_name='unsubcribe_template', to=orm['newsletter.EmailTemplate'])),
            ('message_template', self.gf('django.db.models.fields.related.ForeignKey')(default=1L, related_name='message_template', to=orm['newsletter.EmailTemplate'])),
        ))
        db.send_create_signal('newsletter', ['Newsletter'])

        # Adding M2M table for field photoreports on 'Newsletter'
        db.create_table('newsletter_newsletter_photoreports', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('newsletter', models.ForeignKey(orm['newsletter.newsletter'], null=False)),
            ('photoreport', models.ForeignKey(orm['photoreport.photoreport'], null=False))
        ))
        db.create_unique('newsletter_newsletter_photoreports', ['newsletter_id', 'photoreport_id'])

        # Adding M2M table for field newsitems on 'Newsletter'
        db.create_table('newsletter_newsletter_newsitems', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('newsletter', models.ForeignKey(orm['newsletter.newsletter'], null=False)),
            ('newsitem', models.ForeignKey(orm['news.newsitem'], null=False))
        ))
        db.create_unique('newsletter_newsletter_newsitems', ['newsletter_id', 'newsitem_id'])

        # Adding M2M table for field actions on 'Newsletter'
        db.create_table('newsletter_newsletter_actions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('newsletter', models.ForeignKey(orm['newsletter.newsletter'], null=False)),
            ('action', models.ForeignKey(orm['action.action'], null=False))
        ))
        db.create_unique('newsletter_newsletter_actions', ['newsletter_id', 'action_id'])

        # Adding M2M table for field events on 'Newsletter'
        db.create_table('newsletter_newsletter_events', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('newsletter', models.ForeignKey(orm['newsletter.newsletter'], null=False)),
            ('event', models.ForeignKey(orm['event.event'], null=False))
        ))
        db.create_unique('newsletter_newsletter_events', ['newsletter_id', 'event_id'])

        # Adding model 'EmailTemplate'
        db.create_table('newsletter_emailtemplate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default=u'Default', max_length=200)),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=16, db_index=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('html', self.gf('tinymce.models.HTMLField')(null=True, blank=True)),
        ))
        db.send_create_signal('newsletter', ['EmailTemplate'])

        # Adding unique constraint on 'EmailTemplate', fields ['title', 'action']
        db.create_unique('newsletter_emailtemplate', ['title', 'action'])

        # Adding model 'Subscription'
        db.create_table('newsletter_subscription', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('activation_code', self.gf('django.db.models.fields.CharField')(default='0df5813ed5e9597c88c94c75830baaa5f729d016', max_length=40)),
            ('subscribed', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('subscribe_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('unsubscribed', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('unsubscribe_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('name_field', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, db_column='name', blank=True)),
            ('email_field', self.gf('django.db.models.fields.EmailField')(db_index=True, max_length=75, null=True, db_column='email', blank=True)),
        ))
        db.send_create_signal('newsletter', ['Subscription'])

        # Adding unique constraint on 'Subscription', fields ['user', 'email_field']
        db.create_unique('newsletter_subscription', ['user_id', 'email'])

        # Adding model 'Submission'
        db.create_table('newsletter_submission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('newsletter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['newsletter.Newsletter'])),
            ('publish_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 10, 3, 14, 7, 18, 523550), null=True, db_index=True, blank=True)),
            ('publish', self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True)),
            ('prepared', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('sent', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('sending', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
        ))
        db.send_create_signal('newsletter', ['Submission'])

        # Adding M2M table for field subscriptions on 'Submission'
        db.create_table('newsletter_submission_subscriptions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('submission', models.ForeignKey(orm['newsletter.submission'], null=False)),
            ('subscription', models.ForeignKey(orm['newsletter.subscription'], null=False))
        ))
        db.create_unique('newsletter_submission_subscriptions', ['submission_id', 'subscription_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Subscription', fields ['user', 'email_field']
        db.delete_unique('newsletter_subscription', ['user_id', 'email'])

        # Removing unique constraint on 'EmailTemplate', fields ['title', 'action']
        db.delete_unique('newsletter_emailtemplate', ['title', 'action'])

        # Deleting model 'Subscriber'
        db.delete_table('newsletter_subscriber')

        # Deleting model 'Newsletter'
        db.delete_table('newsletter_newsletter')

        # Removing M2M table for field photoreports on 'Newsletter'
        db.delete_table('newsletter_newsletter_photoreports')

        # Removing M2M table for field newsitems on 'Newsletter'
        db.delete_table('newsletter_newsletter_newsitems')

        # Removing M2M table for field actions on 'Newsletter'
        db.delete_table('newsletter_newsletter_actions')

        # Removing M2M table for field events on 'Newsletter'
        db.delete_table('newsletter_newsletter_events')

        # Deleting model 'EmailTemplate'
        db.delete_table('newsletter_emailtemplate')

        # Deleting model 'Subscription'
        db.delete_table('newsletter_subscription')

        # Deleting model 'Submission'
        db.delete_table('newsletter_submission')

        # Removing M2M table for field subscriptions on 'Submission'
        db.delete_table('newsletter_submission_subscriptions')


    models = {
        'action.action': {
            'Meta': {'ordering': "['-pub_date']", 'object_name': 'Action'},
            'full_text': ('tinymce.models.HTMLField', [], {}),
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
        'event.event': {
            'Meta': {'ordering': "['category', 'id']", 'object_name': 'Event'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'events'", 'to': "orm['event.EventCategory']"}),
            'description': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'genre': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'events'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['event.EventGenre']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'events'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'num_votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'place': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'events'", 'symmetrical': 'False', 'through': "orm['event.Occurrence']", 'to': "orm['place.Place']"}),
            'rate': ('django.db.models.fields.FloatField', [], {'default': '1', 'max_length': '10'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'trailer': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'event.eventcategory': {
            'Meta': {'object_name': 'EventCategory'},
            'category_mean': ('django.db.models.fields.FloatField', [], {'default': '1.0', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rating_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
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
        'news.newsitem': {
            'Meta': {'object_name': 'NewsItem'},
            'ext_authors': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'ext_authors_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'full_text': ('tinymce.models.HTMLField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'is_fixed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'short_text': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'news'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['tagging.Tag']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'newsletter.emailtemplate': {
            'Meta': {'ordering': "('title',)", 'unique_together': "(('title', 'action'),)", 'object_name': 'EmailTemplate'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '16', 'db_index': 'True'}),
            'html': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'default': "u'Default'", 'max_length': '200'})
        },
        'newsletter.newsletter': {
            'Meta': {'ordering': "['id']", 'object_name': 'Newsletter'},
            'actions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'newsletters'", 'symmetrical': 'False', 'to': "orm['action.Action']"}),
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'newsletters'", 'symmetrical': 'False', 'to': "orm['event.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_template': ('django.db.models.fields.related.ForeignKey', [], {'default': '1L', 'related_name': "'message_template'", 'to': "orm['newsletter.EmailTemplate']"}),
            'newsitems': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'newsletters'", 'symmetrical': 'False', 'to': "orm['news.NewsItem']"}),
            'photoreports': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'newsletters'", 'symmetrical': 'False', 'to': "orm['photoreport.PhotoReport']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'subscribe_template': ('django.db.models.fields.related.ForeignKey', [], {'default': '2L', 'related_name': "'subcribe_template'", 'to': "orm['newsletter.EmailTemplate']"}),
            'text': ('tinymce.models.HTMLField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'unsubscribe_template': ('django.db.models.fields.related.ForeignKey', [], {'default': '3L', 'related_name': "'unsubcribe_template'", 'to': "orm['newsletter.EmailTemplate']"}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'newsletter.submission': {
            'Meta': {'object_name': 'Submission'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'newsletter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['newsletter.Newsletter']"}),
            'prepared': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'publish': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 10, 3, 14, 7, 18, 523550)', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'sending': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'subscriptions': ('django.db.models.fields.related.ManyToManyField', [], {'db_index': 'True', 'to': "orm['newsletter.Subscription']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'newsletter.subscriber': {
            'Meta': {'ordering': "['id']", 'object_name': 'Subscriber'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'newsletter.subscription': {
            'Meta': {'unique_together': "(('user', 'email_field'),)", 'object_name': 'Subscription'},
            'activation_code': ('django.db.models.fields.CharField', [], {'default': "'51ea6ba07006ab02ac0275d7f178925c73d1d7e1'", 'max_length': '40'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email_field': ('django.db.models.fields.EmailField', [], {'db_index': 'True', 'max_length': '75', 'null': 'True', 'db_column': "'email'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'name_field': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'db_column': "'name'", 'blank': 'True'}),
            'subscribe_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'subscribed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'unsubscribe_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'unsubscribed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'photoreport.photoreport': {
            'Meta': {'ordering': "['-date_event']", 'object_name': 'PhotoReport'},
            'date_event': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'on_mainpage': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'place_event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photoreports'", 'to': "orm['place.Place']"}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'photoreports'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['tagging.Tag']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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

    complete_apps = ['newsletter']
