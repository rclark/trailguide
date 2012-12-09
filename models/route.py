from django.contrib.gis.db import models
from django.contrib import admin

class Route(models.Model):
    """A collection of segments that represents a 'trail' or a  'hike'"""
    class Meta:
        app_label = 'trailguide'
        
    geo = models.GeometryCollectionField()
    objects = models.GeoManager()
    
    segments = models.ManyToManyField('Segment')
    
    name = models.CharField(max_length=255)
    test = models.TextField()
    
class RouteAdmin(admin.ModelAdmin):
    pass

admin.site.register(Route, RouteAdmin)