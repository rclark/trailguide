# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Route'
        db.create_table(u'trailguide_route', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('geo', self.gf('django.contrib.gis.db.models.fields.GeometryCollectionField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('test', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('trailguide', ['Route'])

        # Adding M2M table for field segments on 'Route'
        db.create_table(u'trailguide_route_segments', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('route', models.ForeignKey(orm['trailguide.route'], null=False)),
            ('segment', models.ForeignKey(orm['trailguide.segment'], null=False))
        ))
        db.create_unique(u'trailguide_route_segments', ['route_id', 'segment_id'])

        # Adding model 'Region'
        db.create_table(u'trailguide_region', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('geo', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')()),
        ))
        db.send_create_signal('trailguide', ['Region'])

        # Adding model 'Trailhead'
        db.create_table(u'trailguide_trailhead', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('geo', self.gf('django.contrib.gis.db.models.fields.PointField')()),
        ))
        db.send_create_signal('trailguide', ['Trailhead'])

        # Adding model 'Segment'
        db.create_table(u'trailguide_segment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('geo', self.gf('django.contrib.gis.db.models.fields.LineStringField')()),
        ))
        db.send_create_signal('trailguide', ['Segment'])

        # Adding model 'Description'
        db.create_table(u'trailguide_description', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('trailguide', ['Description'])

        # Adding model 'PointOfInterest'
        db.create_table(u'trailguide_pointofinterest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('geo', self.gf('django.contrib.gis.db.models.fields.PointField')()),
        ))
        db.send_create_signal('trailguide', ['PointOfInterest'])


    def backwards(self, orm):
        # Deleting model 'Route'
        db.delete_table(u'trailguide_route')

        # Removing M2M table for field segments on 'Route'
        db.delete_table('trailguide_route_segments')

        # Deleting model 'Region'
        db.delete_table(u'trailguide_region')

        # Deleting model 'Trailhead'
        db.delete_table(u'trailguide_trailhead')

        # Deleting model 'Segment'
        db.delete_table(u'trailguide_segment')

        # Deleting model 'Description'
        db.delete_table(u'trailguide_description')

        # Deleting model 'PointOfInterest'
        db.delete_table(u'trailguide_pointofinterest')


    models = {
        'trailguide.description': {
            'Meta': {'object_name': 'Description'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'trailguide.pointofinterest': {
            'Meta': {'object_name': 'PointOfInterest'},
            'geo': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'trailguide.region': {
            'Meta': {'object_name': 'Region'},
            'geo': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'trailguide.route': {
            'Meta': {'object_name': 'Route'},
            'geo': ('django.contrib.gis.db.models.fields.GeometryCollectionField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'segments': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['trailguide.Segment']", 'symmetrical': 'False'}),
            'test': ('django.db.models.fields.TextField', [], {})
        },
        'trailguide.segment': {
            'Meta': {'object_name': 'Segment'},
            'geo': ('django.contrib.gis.db.models.fields.LineStringField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'trailguide.trailhead': {
            'Meta': {'object_name': 'Trailhead'},
            'geo': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['trailguide']