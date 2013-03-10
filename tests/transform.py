from django.test import TestCase
from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry, Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon, GeometryCollection
from trailguide.api.transform import to_json
from datetime import datetime
import json

class TransformTestCase(TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
        
    def test_to_json_basic_fields(self):
        """Check that basic fields returns correctly from trailguide.api.transform.to_json"""
        class TestBasicFields(models.Model):
            auto = models.AutoField(primary_key=True)
            bool = models.BooleanField()
            char = models.CharField(max_length=255)
            csi = models.CommaSeparatedIntegerField()
            decimal = models.DecimalField()
            email = models.EmailField()
            file_path = models.FilePathField(path="/")
            float = models.FloatField()
            int = models.IntegerField()
            ip = models.IPAddressField()
            gen_ip = models.GenericIPAddressField()
            null_bool = models.NullBooleanField()
            pos_int = models.PositiveIntegerField()
            pos_small_int = models.PositiveSmallIntegerField()
            slug = models.SlugField()
            small_int = models.SmallIntegerField()
            text = models.TextField()
            url = models.URLField()
        
        values = {
            "auto":0,
            "bool":True,
            "char":"testing, 1..2..3",
            "csi":1,
            "decimal":1.2,
            "email":"nothing@fake.com",
            "file_path":"var",
            "float":1.2,
            "int":1,
            "ip":"127.0.0.1",
            "gen_ip":"127.0.0.1",
            "null_bool":False,
            "pos_int":1,
            "pos_small_int":1,
            "slug":"test-slug",
            "small_int":1,
            "text":"testing, 1...2...3",
            "url":"http://www.google.com"      
        }
        instance = TestBasicFields(**values)        
        result = to_json(instance)
                 
        self.assertIsInstance(
            result,
            str,
            "trailguide.api.transform.to_json did not return a string when testing basic fields."
        )
        
        self.assertEqual(
            json.loads(result), 
            values,            
            "trailguide.api.transform.to_json did not return the correct values for basic fields."
        )
        
    def test_to_json_date_time_fields(self):
        """Check that Date, DateTime and Time Fields return correct ISO-formatted dates from trailguide.api.transform.to_json"""
        class TestDateTime(models.Model):
            the_date = models.DateField()
            the_datetime = models.DateTimeField()
            the_time = models.TimeField()
        
        now = datetime.now()
        instance = TestDateTime(
            the_date=datetime.date(now),
            the_datetime=now,
            the_time=datetime.time(now)                  
        )
        result = to_json(instance)

        self.assertIsInstance(
            result, 
            str, 
            "trailguide.api.transform.to_json did not return a string when testing DateTime fields."
        )
        
        self.assertEqual(
            json.loads(result),
            { "id": None,
              "the_date": datetime.date(now).isoformat(),
              "the_datetime": now.isoformat(),
              "the_time": datetime.time(now).isoformat() },
            "trailguide.api.transform.to_json did not return correctly formatted ISO date strings"                 
        )
        
    def test_to_json_geometry_fields(self):
        """Check that geometry fields return the correct GeoJSON data"""
        class TestGeometryFields(models.Model):
            geo = models.GeometryField()
            point = models.PointField()
            line = models.LineStringField()
            poly = models.PolygonField()
            multi_point = models.MultiPointField()
            multi_line = models.MultiLineStringField()
            multi_poly = models.MultiPolygonField()
            coll = models.GeometryCollectionField()
            objects = models.GeoManager()
        
        pntJson = '{"type": "Point", "coordinates": [102.0, 0.5]}'
        lineJson = '{ "type": "LineString", "coordinates": [ [102.0, 0.0], [103.0, 1.0], [104.0, 0.0], [105.0, 1.0] ] }'
        polyJson = '{ "type": "Polygon", "coordinates": [ [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0] ] ] }'
        multi_pointJson = '{ "type": "MultiPoint", "coordinates": [ [100.0, 0.0], [101.0, 1.0] ] }'
        multi_lineJson = '{ "type": "MultiLineString", "coordinates": [ [ [100.0, 0.0], [101.0, 1.0] ], [ [102.0, 2.0], [103.0, 3.0] ] ] }'
        multi_polyJson = '{ "type": "MultiPolygon", "coordinates": [ [[[102.0, 2.0], [103.0, 2.0], [103.0, 3.0], [102.0, 3.0], [102.0, 2.0]]], [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]], [[100.2, 0.2], [100.8, 0.2], [100.8, 0.8], [100.2, 0.8], [100.2, 0.2]]] ] }'
        collJson = '{ "type": "GeometryCollection", "geometries": [ { "type": "Point", "coordinates": [100.0, 0.0] }, { "type": "LineString", "coordinates": [ [101.0, 0.0], [102.0, 1.0] ] } ] }'
        
        instance = TestGeometryFields(
            geo = Point(102.0,0.5),
            point = Point(102.0,0.5),
            line = LineString( (102.0, 0.0), (103.0, 1.0), (104.0, 0.0), (105.0, 1.0) ),
            poly = Polygon( ( (100.0, 0.0), (101.0, 0.0), (101.0, 1.0), (100.0, 1.0), (100.0, 0.0) ) ),
            multi_point = MultiPoint(Point(100,0.0), Point(101, 1)),
            multi_line = MultiLineString( LineString( (100.0, 0.0), (101.0, 1.0) ), LineString( (102.0, 2.0), (103.0, 3.0) ) ),
            multi_poly = MultiPolygon( Polygon( ( (102.0, 2.0), (103.0, 2.0), (103.0, 3.0), (102.0, 3.0), (102.0, 2.0) ) ), Polygon( ( (100.0, 0.0), (101.0, 0.0), (101.0, 1.0), (100.0, 1.0), (100.0, 0.0) ), ( (100.2, 0.2), (100.8, 0.2), (100.8, 0.8), (100.2, 0.8), (100.2, 0.2) ) ) ),
            coll = GeometryCollection( Point(100.0, 0.0), LineString( (101.0, 0.0), (102.0, 1.0) ) )
        )
        
        result = to_json(instance)
        self.assertIsInstance(
            result,
            str,
            "trailguide.api.transform.to_json did not return a string when testing Geometry fields."
        )
        
        self.assertEqual(
            json.loads(result),
            { "id": None,
              "geo": json.loads(pntJson),
              "point": json.loads(pntJson),
              "line": json.loads(lineJson),
              "poly": json.loads(polyJson),
              "multi_point": json.loads(multi_pointJson),
              "multi_line": json.loads(multi_lineJson),
              "multi_poly": json.loads(multi_polyJson),
              "coll": json.loads(collJson) },
            "trailguide.api.transform.to_json did not return properly encoded GeoJSON strings for Geometry fields."                 
        )
                    