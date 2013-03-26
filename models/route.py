from django.contrib.gis.db import models
from django.contrib.gis import admin
from django.db.models import Avg
from trailguide.models.trailhead import Trailhead
from trailguide.models.segment import Segment

class Route(models.Model):
    """A collection of segments that represents a 'trail' or a  'hike'"""
    class Meta:
        app_label = 'trailguide'
    
    name = models.CharField(max_length=255)
    th_start = models.ForeignKey(Trailhead, help_text="The starting trailhead.")
    th_end = models.ForeignKey(Trailhead, help_text="The ending trailhead (may be the same as the starting trailhead).")
    segments = models.ManyToManyField(Segment, through='SegmentPosition')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    # Geospatial components of the model    
    geo = models.GeometryCollectionField(geography=True, srid=4326)
    objects = models.GeoManager()
    
    def _add_segments_field(self, field):
        """Add up a given field of the route's segments."""
        values = [ getattr(segment, field) for segment in self.segments ]
        return sum(values)
    
    def _average_segments_field(self, field):
        return self.segments.aggregate(Avg(field))[field + '__avg']
    
    def length(self):
        """
        Calculate the route's length by adding the lengths of
        all constituent segments.
        """ 
        return self._add_segments_field('length')
    
    def elevation_gains(self):
        """
        Calculate the route's elevation gains by adding the
        elevation gains of all constituent segments.
        """
        return self._add_segments_field('elevation_gains')
    
    def elevation_losses(self):
        """
        Calculate the route's elevation losses by adding the
        elevation losses of all constituent segments.
        """
        return self._add_segments_field('elevation_losses')
    
    def difficulty(self):
        """
        Calculate the route's difficulty by averaging the
        difficulties of all constituent segments.
        """
        return self._average_segments_field('difficulty')
    
    def points_of_interest(self):
        """
        Return a list of the route's points of interest by
        aggregating the points of interest from all constituent
        segments.
        """
        result = []
        for segment in self.segments:
            result.append([ poi for poi in segment.points_of_interest ])
        return result
    
    def notes(self):
        """
        Return a list of the route's notes by aggregating the
        notes from all constituent segments.
        """
        result = []
        for segment in self.segments:
            result.append([ notes for notes in segment.notes ])
        return result


class SegmentPosition(models.Model):
    route = models.ForeignKey(Route)
    segment = models.ForeignKey(Segment)
    position = models.IntegerField()
    
class RouteAdmin(admin.OSMGeoAdmin):
    pass

admin.site.register(Route, RouteAdmin)