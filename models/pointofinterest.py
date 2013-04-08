from django.contrib.gis.db import models
from django.contrib.gis import admin
from trailguide.models.constants import poi_types

class PointOfInterest(models.Model):
    """Point features representing interesting places"""
    class Meta:
        app_label = 'trailguide'
    
    name = models.CharField(max_length=255)
    type = models.IntegerField(choices=poi_types)
    
    # Geospatial components of the model
    geo = models.PointField()
    objects = models.GeoManager()
    
class PointOfInterestAdmin(admin.OSMGeoAdmin):
    pass

admin.site.register(PointOfInterest, PointOfInterestAdmin)