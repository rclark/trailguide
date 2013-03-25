from django.test import TestCase
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import Distance
from django.contrib.gis import gdal
from trailguide.models import Segment

class SegmentTestCase(TestCase):
    """Test Segment model methods"""
    sample_geojson = '{ "type": "LineString", "coordinates": [ [100.0, 0.0], [101.0, 1.0] ] }'

    def setUp(self):
        self.sample_segment = Segment(condition=1, geo=GEOSGeometry(self.sample_geojson))
        geom = self.sample_segment.geo.ogr.transform(gdal.SpatialReference(900913), clone=True)
        self.sample_projected_geom = GEOSGeometry(geom.wkt, 900913)

    def tearDown(self):
        pass

    def test_segment_length(self):
        """Segment's length must return an GeoDjango Distance"""
        self.assertIsInstance(self.sample_segment.length(), Distance)

    def test_segment_mercator(self):
        """Segment's method should properly convert to spherical mercator"""
        result = self.sample_segment.geom_in_spherical_mercator()
        self.assertEqual(result, self.sample_projected_geom)

    def test_segment_length_is_correct(self):
        """Segment's length returns the right value"""
        d = Distance(m=self.sample_projected_geom.length)


