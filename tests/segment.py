from django.test import TestCase
from django.contrib.gis.measure import Distance
from django.contrib.gis import geos
from django.contrib.gis import gdal
from trailguide.models import Segment
from trailguide.models.dem import Dem
import os, json, math

class SegmentTestCase(TestCase):
    """Test Segment model methods"""
    sample_coords = [ [100, 0], [101, 1], [110, 9] ]
    geo_points = [ geos.Point(pnt[0], pnt[1], srid=4326) for pnt in sample_coords ]
    proj_srs = gdal.SpatialReference(3857)
    proj_points = [ pnt.ogr.transform(proj_srs, clone=True) for pnt in geo_points ]
    sample_geojson = '{ "type": "LineString", "coordinates": %s }' % json.dumps(sample_coords)
    geo_geom = geos.GEOSGeometry(sample_geojson, 4326)
    proj_geom = geos.GEOSGeometry(geo_geom.ogr.transform(proj_srs, clone=True).wkt, 3857)
    sample_segment = Segment(condition=1, geo=geos.GEOSGeometry(sample_geojson))

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_segment_length_type(self):
        """Segment's length must return an GeoDjango Distance"""
        self.assertIsInstance(self.sample_segment.length(), Distance)

    def test_segment_mercator(self):
        """Segment's method should properly convert to spherical mercator"""
        result = self.sample_segment.geom_in_spherical_mercator()
        self.assertEqual(result, self.proj_geom)

    def test_segment_length_is_correct(self):
        """Segment's length returns the right value"""
        d = Distance(m=self.proj_geom.length)

    def test_array_of_points(self):
        """Check that segment can be portrayed as an array of Points"""
        self.assertEqual(self.sample_segment.as_point_array(), self.geo_points)

    def test_array_of_projected_points(self):
        """Check that segment can be portrayed as an array of projected Points"""
        self.assertEqual(self.sample_segment.as_projected_point_array(), self.proj_points)

    def test_elevation_array(self):
        """Segment should be able to represent an array of elevations at each vertex"""
        test_dem_path = os.path.join(os.path.dirname(__file__), "dem", "test_dem.tif")
        dem = Dem(test_dem_path)
        expected = [ dem.read_value(pnt) for pnt in self.sample_segment.densified_point_array(dem.pixel_distance) ]
        self.assertEqual(self.sample_segment.elevation_array(dem), expected)

    def test_distance_array(self):
        """Segment should be able to calculate the distance between each vertex"""
        expected = []
        for index, end_point in enumerate(self.proj_points):
            if index == 0:
                d = 0
            else:
                start_point = self.proj_points[index-1]
                dx = start_point.x - end_point.x
                dy = start_point.y - end_point.y
                d = math.sqrt(dx**2 + dy**2)
            expected.append(Distance(m=d))
        self.assertEqual(self.sample_segment.distance_array(), expected)

    def test_distance_calculation(self):
        for index, last_point in enumerate(self.proj_points):
            if index != 0:
                first_point = self.proj_points[index-1]
                dx = first_point.x - last_point.x
                dy = first_point.y - last_point.y
                expected = math.sqrt(dx**2 + dy**2)
                result = self.sample_segment._distance(first_point, last_point)
                self.assertEqual(result, expected)

    def test_densify(self):
        def distance(first_point, last_point):
            dx = first_point.x - last_point.x
            dy = first_point.y - last_point.y
            return Distance(m=math.sqrt(dx**2 + dy**2))

        def distance_array():
            output = []
            for index, point in enumerate(self.proj_points):
                if index == 0: d = 0
                else:
                    first = self.proj_points[index-1]
                    d = distance(first, point)
                output.append(d)
            return output

        distances = distance_array()
        expected = []
        threshold = Distance(m=10000)

        def gen_new_point(start_point, dx, dy):
            coords = (start_point.x + dx.m, start_point.y + dy.m)
            pnt = geos.Point(coords)
            expected.append(pnt)
            return pnt

        for index, end_point in enumerate(self.proj_points):
            if index == 0: expected.append(end_point)
            else:
                if distances[index] > threshold:
                    # Find the angle of the line between the two points
                    start_point = self.proj_points[index-1]
                    dx = end_point.x - start_point.x
                    dy = end_point.y - start_point.y
                    angle = math.atan(dy/dx)

                    # Calculate the dx/dy for points to be added along the line
                    dx = threshold * math.cos(angle)
                    dy = threshold * math.sin(angle)

                    # Coordinates of the new point
                    new_point = gen_new_point(start_point, dx, dy)

                    # Continue making new points until you're within the threshold of the end point
                    while distance(new_point, end_point) > threshold:
                        new_point = gen_new_point(new_point, dx, dy)

                # Once you've added all your points, add the end point
                expected.append(end_point)

        self.assertEqual(self.sample_segment.densified_point_array(threshold), expected)
