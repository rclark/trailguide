from django.test import TestCase
from trailguide.models import Segment, Trailhead, Route, SegmentPosition
from django.contrib.gis import geos
from django.contrib.gis.geos import GeometryCollection
import json

class RouteTestCase(TestCase):
    """Test Route model methods."""

    
    def setUp(self):
        # first sample segment
        sample_coords = [ [100, 0], [101, 1], [110, 9] ]
        sample_geojson = '{ "type": "LineString", "coordinates": %s }' % json.dumps(sample_coords)
        self.sample_segment = Segment.objects.create(condition=1, geo=geos.GEOSGeometry(sample_geojson))
        # second sample segment
        sample_coords2 = [ [110, 9], [112, 12], [100, 3] ]
        sample_geojson2 = '{ "type": "LineString", "coordinates": %s }' % json.dumps(sample_coords2)
        self.sample_segment2 = Segment.objects.create(condition=1, geo=geos.GEOSGeometry(sample_geojson2))
        # first sample trailhead
        sample_coords3 = [100, 0]
        sample_geojson3 = '{ "type": "Point", "coordinates": %s }' % json.dumps(sample_coords3)
        self.sample_th1 = Trailhead.objects.create(name="Test1", geo=geos.GEOSGeometry(sample_geojson3))
        # first sample trailhead
        sample_coords4 = [100, 3]
        sample_geojson4 = '{ "type": "Point", "coordinates": %s }' % json.dumps(sample_coords4)
        self.sample_th2 = Trailhead.objects.create(name="Test2", geo=geos.GEOSGeometry(sample_geojson4))
        # sample route
        self.sample_route = Route.objects.create(name="Route", th_start=self.sample_th1, th_end=self.sample_th2)
        # sample segment positions
        self.pos1 = SegmentPosition.objects.create(route=self.sample_route, segment=self.sample_segment, position=1)
        self.pos2 = SegmentPosition.objects.create(route=self.sample_route, segment=self.sample_segment2, position=2)

    def tearDown(self):
        pass
    
    def test_length(self):
        length = self.sample_segment.length() + self.sample_segment2.length()
        self.assertEqual(length, self.sample_route.length())
