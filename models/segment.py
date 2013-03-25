from django.contrib.gis.db import models
from django.contrib.gis import admin
from django.contrib.gis import gdal, geos
from django.contrib.gis.measure import Distance
from trailguide.models import PointOfInterest

trail_conditions = (
    (1, "Easy"),
    (2, "Fucking Terrible")
)

class Segment(models.Model):
    """Line features representing a trail segment"""
    class Meta:
        app_label = 'trailguide'

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
        transformed = self.geo.ogr.transform(gdal.SpatialReference(900913), clone=True)
        return geos.GEOSGeometry(transformed.wkt, 900913    )

    def length(self):
        """Calculate the length of the line segment"""
        return Distance(m=self.geom_in_spherical_mercator().length)

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