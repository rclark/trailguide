from django.contrib.gis.db import models
from django.contrib.gis import admin
from django.contrib.gis import gdal, geos
from django.contrib.gis.measure import Distance
from trailguide.models.pointofinterest import PointOfInterest
from trailguide.models.constants import trail_conditions, difficulties
from trailguide.models.dem import Dem
from trailguide.utils import gis
from geographic_model import GeographicModel

class Segment(models.Model, GeographicModel):
    """Line features representing a trail segment"""
    class Meta:
        app_label = 'trailguide'

    #proj_epsg = 3857
    #proj_srs = gdal.SpatialReference(proj_epsg)

    name = models.CharField(max_length=255, blank=True)
    condition = models.IntegerField(choices=trail_conditions)
    notes = models.TextField(blank=True)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    adjacent_segments = models.ManyToManyField("Segment", blank=True)
    points_of_interest = models.ManyToManyField(PointOfInterest, blank=True)

    # Geospatial components of the model
    geo = models.LineStringField(srid=4326)
    #objects = models.GeoManager()

    '''
    def geom_in_spherical_mercator(self):
        """Return the geometry of the object in spherical mercator projection"""
        transformed = self.geo.ogr.transform(self.proj_srs, clone=True)
        return geos.GEOSGeometry(transformed.wkt, self.proj_epsg)
    '''

    def serialize_properties(self):
        """Serialize this object's properties"""
        return {
            'name': self.name,
            'condition': self.get_condition_display(),
            'notes': self.notes,
            'date_created': self.date_created.isoformat(),
            'date_updated': self.date_updated.isoformat()
        }

    def length(self):
        """Calculate the length of the line segment"""
        return Distance(m=self.geom_in_spherical_mercator().length)

    def geo_point_array(self):
        """Represent the geometry of the segment as an array of Points"""
        return [ geos.Point(coord[0], coord[1], srid=4326) for coord in self.geo.coords ]

    def proj_point_array(self):
        """Represent the geometry of the segment as an array of projected Points"""
        return [ pnt.ogr.transform(self.proj_srs, clone=True) for pnt in self.geo_point_array() ]

    def distance_array(self):
        """Generate an array of distances between each vertex"""
        return gis.distance_array(self.proj_point_array())

    def densified_point_array(self, threshold):
        """Add points to the line such that the distance between any two points is < threshold"""
        return gis.densified_line(self.proj_point_array(), threshold)

    def densified_distance_array(self, threshold):
        """Generate an array of distances between vertexes in a densified line"""
        return gis.distance_array(gis.densified_line(self.proj_point_array(), threshold))

    def elevation_profile(self):
        """
        Generate an elevation profile: a list of tuples, first number is distance from start, second is elevation
        
        This takes a second or two. Should consider caching the result.
        """
        dem = Dem()
        threshold = dem.pixel_distance
        densified_line = self.densified_point_array(threshold)
        densified_distances = self.densified_distance_array(threshold)
        elevations = gis.elevations_along_line(densified_line, dem)

        def profile_point(index):
            d = sum([ d.m for d in densified_distances[:index+1] ])
            return (Distance(m=d), elevations[index])

        return [profile_point(i) for i in range(0,len(elevations))]

    def profile_to_csv(self, csv_path):
        """Write out the elevation profile to a csv file"""
        import csv
        with open(csv_path, "wb") as f:
            writer = csv.writer(f)
            writer.writerows([ (d[0].m, d[1].m) for d in self.elevation_profile() ])

    def elevation_losses(self):
        """Calculate the total elevation lost along the segment"""
        profile = self.elevation_profile()
        losses = Distance()
        for i, pnt in enumerate(profile):
            if i > 0:
                prev = profile[i-1]
                dif = pnt[1] - prev[1]
                if dif < Distance():
                    losses += dif
        return losses


    def elevation_gains(self):
        """Calculate the total elevation gained along the segment"""
        profile = self.elevation_profile()
        gains = Distance()
        for i, pnt in enumerate(profile):
            if i > 0:
                prev = profile[i-1]
                dif = pnt[1] - prev[1]
                if dif > Distance():
                    gains += dif
        return gains

    def add_adjacent_segments(self):
        """Link adjacent segments by geometry analysis"""
        pass

    def difficulty(self):
        """Calculated difficulty based on elevation changes and condition"""
        pass

class SegmentAdmin(admin.OSMGeoAdmin):
    pass

admin.site.register(Segment, SegmentAdmin)