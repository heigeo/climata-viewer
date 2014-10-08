# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # These tables were already created by vera before we swapped out the
        # models
        db.rename_table('wq_event', 'data_event')
        return

        # Adding model 'Event'
        db.create_table('data_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['locations.Site'], null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'data', ['Event'])

        # Adding unique constraint on 'Event', fields ['site', 'date']
        db.create_unique('data_event', ['site_id', 'date'])

        # Adding model 'EventResult'
        db.create_table('wq_eventresult', (
            ('id', self.gf('django.db.models.fields.PositiveIntegerField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Event'])),
            ('result', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vera.Result'])),
            ('event_site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['locations.Site'], null=True, blank=True)),
            ('event_date', self.gf('django.db.models.fields.DateField')()),
            ('result_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vera.Parameter'])),
            ('result_report', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vera.Report'])),
            ('result_value_numeric', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('result_value_text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('result_empty', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'data', ['EventResult'])

        # Adding unique constraint on 'EventResult', fields ['event', 'result_type']
        db.create_unique('wq_eventresult', ['event_id', 'result_type_id'])


    def backwards(self, orm):
        db.rename_table('data_event', 'wq_event')
        return

        # Removing unique constraint on 'EventResult', fields ['event', 'result_type']
        db.delete_unique('wq_eventresult', ['event_id', 'result_type_id'])

        # Removing unique constraint on 'Event', fields ['site', 'date']
        db.delete_unique('data_event', ['site_id', 'date'])

        # Deleting model 'Event'
        db.delete_table('data_event')

        # Deleting model 'EventResult'
        db.delete_table('wq_eventresult')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'data.datarequest': {
            'Meta': {'ordering': "('-requested',)", 'object_name': 'DataRequest'},
            'completed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'requested': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'webservice': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Webservice']"})
        },
        u'data.event': {
            'Meta': {'ordering': "('-date',)", 'unique_together': "(('site', 'date'),)", 'object_name': 'Event', 'db_table': "'data_event'"},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['locations.Site']", 'null': 'True', 'blank': 'True'})
        },
        u'data.eventresult': {
            'Meta': {'unique_together': "(('event', 'result_type'),)", 'object_name': 'EventResult', 'db_table': "'wq_eventresult'"},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Event']"}),
            'event_date': ('django.db.models.fields.DateField', [], {}),
            'event_site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['locations.Site']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.PositiveIntegerField', [], {'primary_key': 'True'}),
            'result': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['vera.Result']"}),
            'result_empty': ('django.db.models.fields.BooleanField', [], {}),
            'result_report': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['vera.Report']"}),
            'result_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['vera.Parameter']"}),
            'result_value_numeric': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'result_value_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'data.project': {
            'Meta': {'object_name': 'Project'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'data.webservice': {
            'Meta': {'object_name': 'Webservice'},
            'authority': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['identify.Authority']"}),
            'class_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'homepage': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'identify.authority': {
            'Meta': {'object_name': 'Authority', 'db_table': "'wq_identifiertype'"},
            'homepage': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'object_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'locations.site': {
            'Meta': {'object_name': 'Site'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'vera.parameter': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Parameter', 'db_table': "'wq_parameter'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_numeric': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'units': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'vera.report': {
            'Meta': {'ordering': "('-entered',)", 'object_name': 'Report', 'db_table': "'wq_report'"},
            'entered': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['vera.ReportStatus']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'vera_report'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'vera.reportstatus': {
            'Meta': {'unique_together': "[['slug']]", 'object_name': 'ReportStatus', 'db_table': "'wq_reportstatus'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_valid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'vera.result': {
            'Meta': {'ordering': "('type',)", 'object_name': 'Result', 'db_table': "'wq_result'", 'index_together': "[('type', 'report', 'empty')]"},
            'empty': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'results'", 'to': u"orm['vera.Report']"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['vera.Parameter']"}),
            'value_numeric': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'value_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['data']
