from django.contrib.gis.db import models
from django.contrib import admin

class Route(models.Model):
    """A collection of segments that represents a 'trail' or a  'hike'"""
    class Meta:
        app_label = 'trailguide'
    
    # Geospatial components of the model    
    geo = models.GeometryCollectionField()
    objects = models.GeoManager()
    
class RouteAdmin(admin.ModelAdmin):
    pass

admin.site.register(Route, RouteAdmin)