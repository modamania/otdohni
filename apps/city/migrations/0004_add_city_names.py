# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        citys = open('citys.txt', 'r')
        for s in citys.readlines():
            if len(s) < 5:
                continue
            data = s.split('|')
            id = int(data[0])
            Site = orm['sites.Site']
            site = Site.objects.get(id=id)
            city = orm.City()
            city.site = site
            city.name = data[1].decode('utf-8')
            city.genitive = data[3].decode('utf-8')
            city.accusative = data[2].decode('utf-8')
            city.save()
        omsk = orm.City.objects.get(name=u'Омск')
        omsk.genitive = u'Омска'
        omsk.accusative = u'Омске'
        omsk.save()
        nsk = orm.City.objects.get(name=u'Новосибирск')
        nsk.genitive = u'Новосибирска'
        nsk.accusative = u'Новосибирске'
        nsk.save()
            


    def backwards(self, orm):
        "Write your backwards methods here."


    models = {
        'city.city': {
            'Meta': {'object_name': 'City'},
            'accusative': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True'}),
            'genitive': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'name_by_geoip': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20', 'null': 'True'}),
            'post': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20', 'null': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cityes'", 'to': "orm['sites.Site']"})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['city']
