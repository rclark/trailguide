from django.test import TestCase
from trailguide.models import Segment, Trailhead, Route, SegmentPosition, PointOfInterest
from django.contrib.gis import geos
from django.contrib.gis.geos import GeometryCollection
import json

class RouteTestCase(TestCase):
    """Test Route model methods."""

    
    def setUp(self):
        # first sample point of interest
        poi1_coords = [100, 3]
        poi1_geojson = '{ "type": "Point", "coordinates": %s }' % json.dumps(poi1_coords)
        self.poi1 = PointOfInterest.objects.create(name="Point1", type=1, geo=geos.GEOSGeometry(poi1_geojson))
        # second sample point of interest
        poi2_coords = [101, 3]
        poi2_geojson = '{ "type": "Point", "coordinates": %s }' % json.dumps(poi2_coords)
        self.poi2 = PointOfInterest.objects.create(name="Point2", type=2, geo=geos.GEOSGeometry(poi2_geojson))        
        # first sample segment
        seg1_coords = [ [100, 0], [101, 1], [110, 9] ]
        seg1_geojson = '{ "type": "LineString", "coordinates": %s }' % json.dumps(seg1_coords)
        self.seg1 = Segment.objects.create(condition=1, geo=geos.GEOSGeometry(seg1_geojson))
        self.seg1.points_of_interest.add(self.poi1)
        # second sample segment
        seg2_coords = [ [110, 9], [112, 12], [100, 3] ]
        seg2_geojson = '{ "type": "LineString", "coordinates": %s }' % json.dumps(seg2_coords)
        self.seg2 = Segment.objects.create(condition=1, geo=geos.GEOSGeometry(seg2_geojson))
        self.seg2.points_of_interest.add(self.poi2)
        # first sample trailhead
        th1_coords = [100, 0]
        th3_geojson = '{ "type": "Point", "coordinates": %s }' % json.dumps(th1_coords)
        self.th1 = Trailhead.objects.create(name="Test1", geo=geos.GEOSGeometry(th3_geojson))
        # first sample trailhead
        th4_coords = [100, 3]
        th4_geojson = '{ "type": "Point", "coordinates": %s }' % json.dumps(th4_coords)
        self.th2 = Trailhead.objects.create(name="Test2", geo=geos.GEOSGeometry(th4_geojson))
        # sample route
        self.route = Route.objects.create(name="Route", th_start=self.th1, th_end=self.th2)
        # sample segment positions
        self.pos1 = SegmentPosition.objects.create(route=self.route, segment=self.seg1, position=1)
        self.pos2 = SegmentPosition.objects.create(route=self.route, segment=self.seg2, position=2)

    def tearDown(self):
        pass
    
    def test_length(self):
        length = self.seg1.length() + self.seg2.length()
        self.assertEqual(length, self.route.length())
    
    def test_pois(self):
        seg1_pois = [ poi for poi in self.seg1.points_of_interest.all() ]
        seg2_pois = [ poi for poi in self.seg2.points_of_interest.all() ]
        all_pois = [seg1_pois, seg2_pois]
        self.assertEqual(all_pois, self.route.points_of_interest())
