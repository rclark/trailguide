from django.test import TestCase
from trailguide.models import Segment, Trailhead, Route, SegmentPosition
from django.contrib.gis import geos
from django.contrib.gis.geos import GeometryCollection
import json

class RouteTestCase(TestCase):
    """Test Route model methods."""
    # first sample segment
    sample_coords = [ [100, 0], [101, 1], [110, 9] ]
    sample_geojson = '{ "type": "LineString", "coordinates": %s }' % json.dumps(sample_coords)
    sample_segment = Segment(condition=1, geo=geos.GEOSGeometry(sample_geojson))
    sample_segment.save()
    # second sample segment
    sample_coords2 = [ [110, 9], [112, 12], [100, 3] ]
    sample_geojson2 = '{ "type": "LineString", "coordinates": %s }' % json.dumps(sample_coords2)
    sample_segment2 = Segment(condition=1, geo=geos.GEOSGeometry(sample_geojson2))
    sample_segment2.save()
    # first sample trailhead
    sample_coords3 = [100, 0]
    sample_geojson3 = '{ "type": "Point", "coordinates": %s }' % json.dumps(sample_coords3)
    sample_th1 = Trailhead(name="Test1", geo=geos.GEOSGeometry(sample_geojson3))
    sample_th1.save()
    # first sample trailhead
    sample_coords4 = [100, 3]
    sample_geojson4 = '{ "type": "Point", "coordinates": %s }' % json.dumps(sample_coords4)
    sample_th2 = Trailhead(name="Test2", geo=geos.GEOSGeometry(sample_geojson4))
    sample_th2.save()
    # sample route
    sample_route = Route(name="Route", th_start=sample_th1, th_end=sample_th2)
    sample_route.save()
    # sample segment positions
    pos1 = SegmentPosition(route=sample_route, segment=sample_segment, position=1)
    pos1.save()
    pos2 = SegmentPosition(route=sample_route, segment=sample_segment2, position=2)
    pos2.save()
    
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_has_geometry(self):
        gc = GeometryCollection(self.sample_segment.geo, self.sample_segment2.geo)
        self.assertEqual(gc, self.sample_route.geo)
    
    def test_length(self):
        length = self.sample_segment.length() + self.sample_segment2.length()
        self.assertEqual(length, self.sample_route.length())
