from django.contrib.gis.db import models
from django.contrib.gis import admin
from django.contrib.gis import gdal, geos
from django.contrib.gis.measure import Distance
from trailguide.models.pointofinterest import PointOfInterest
from trailguide.models.constants import trail_conditions, difficulties
from trailguide.models.dem import Dem
import math

class Segment(models.Model):
    """Line features representing a trail segment"""
    class Meta:
        app_label = 'trailguide'

    proj_epsg = 900913
    proj_srs = gdal.SpatialReference(proj_epsg)

    name = models.CharField(max_length=255, blank=True)
    condition = models.IntegerField(choices=trail_conditions)
    notes = models.TextField(blank=True)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    adjacent_segments = models.ManyToManyField("Segment", blank=True)
    points_of_interest = models.ManyToManyField(PointOfInterest, blank=True)

    # Geospatial components of the model
    geo = models.LineStringField(geography=True, srid=4326)
    objects = models.GeoManager()

    def geom_in_spherical_mercator(self):
        """Return the geometry of the object in spherical mercator projection"""
        transformed = self.geo.ogr.transform(self.proj_srs, clone=True)
        return geos.GEOSGeometry(transformed.wkt, self.proj_epsg)

    def length(self):
        """Calculate the length of the line segment"""
        return Distance(m=self.geom_in_spherical_mercator().length)

    def as_point_array(self):
        """Represent the geometry of the segment as an array of Points"""
        return [ geos.Point(coord[0], coord[1], srid=4326) for coord in self.geo.coords ]

    def as_projected_point_array(self):
        """Represent the geometry of the segment as an array of projected Points"""
        return [ pnt.ogr.transform(self.proj_srs, clone=True) for pnt in self.as_point_array() ]

    def elevation_array(self, dem=Dem()):
        """Generate an array of elevation values along the segment"""
        threshold = dem.pixel_distance
        return [ dem.read_value(pnt) for pnt in self.densified_point_array(threshold) ]

    def _distance(self, first_point, second_point):
        """Calculate the linear distance between two points"""
        dx = first_point.x - second_point.x
        dy = first_point.y - second_point.y
        return math.sqrt(dx**2 + dy**2)

    def distance_array(self):
        """Generate an array of distances between each vertex"""
        proj_points = self.as_projected_point_array()
        result = []
        for index, end_point in enumerate(proj_points):
            if index == 0:
                d = 0
            else:
                start_point = proj_points[index-1]
                d = self._distance(start_point, end_point)
            result.append(Distance(m=d))
        return result

    def densified_point_array(self, threshold):
        """Add points to the line such that the distance between any two points is < threshold"""
        distances = self.distance_array()
        proj_points = self.as_projected_point_array()
        densified = []

        def gen_new_point(start_point, dx, dy):
            coords = (start_point.x + dx.m, start_point.y + dy.m)
            pnt = geos.Point(coords)
            densified.append(pnt)
            return pnt

        for index, end_point in enumerate(proj_points):
            if index == 0: densified.append(end_point)
            else:
                if distances[index] > threshold: # Is distance from previous point > threshold?
                    # Find the angle of the line between the two points
                    start_point = proj_points[index-1]
                    dx = end_point.x - start_point.x
                    dy = end_point.y - start_point.y
                    angle = math.atan(dy/dx)

                    # Calculate the dx/dy for points to be added along the line
                    dx = threshold * math.cos(angle)
                    dy = threshold * math.sin(angle)

                    # Make a new point
                    new_point = gen_new_point(start_point, dx, dy)

                    # Continue making points until we are within the threshold of the end point
                    while Distance(m=self._distance(new_point, end_point)) > threshold:
                        new_point = gen_new_point(new_point, dx, dy)

                # Have appended any required new points, slap in the end point
                densified.append(end_point)

        return densified

    def elevation_losses(self):
        """Calculate the total elevation lost along the segment"""
        pass

    def elevation_gains(self):
        """Calculate the total elevation gained along the segment"""
        pass

    def add_adjacent_segments(self):
        """Link adjacent segments by geometry analysis"""
        pass

    def difficulty(self):
        """Calculated difficulty based on elevation changes and condition"""
        pass

class SegmentAdmin(admin.OSMGeoAdmin):
    pass

admin.site.register(Segment, SegmentAdmin)