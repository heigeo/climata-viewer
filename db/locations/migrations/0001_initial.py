# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Site'
        db.create_table(u'locations_site', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'locations', ['Site'])

        # Adding model 'State'
        db.create_table(u'locations_state', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'locations', ['State'])

        # Adding model 'County'
        db.create_table(u'locations_county', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'locations', ['County'])

        # Adding model 'Basin'
        db.create_table(u'locations_basin', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'locations', ['Basin'])


    def backwards(self, orm):
        # Deleting model 'Site'
        db.delete_table(u'locations_site')

        # Deleting model 'State'
        db.delete_table(u'locations_state')

        # Deleting model 'County'
        db.delete_table(u'locations_county')

        # Deleting model 'Basin'
        db.delete_table(u'locations_basin')


    models = {
        u'locations.basin': {
            'Meta': {'ordering': "('primary_identifiers__slug',)", 'object_name': 'Basin'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'locations.county': {
            'Meta': {'object_name': 'County'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'locations.site': {
            'Meta': {'object_name': 'Site'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'locations.state': {
            'Meta': {'object_name': 'State'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['locations']