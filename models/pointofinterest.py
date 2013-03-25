from django.contrib.gis.db import models
from django.contrib.gis import admin

class PointOfInterestType(models.Model):
    """Category for points of interest."""
    class Meta:
        app_label = 'trailguide'
    
    name = models.CharField(max_length=255)

class PointOfInterest(models.Model):
    """Point features representing interesting places"""
    class Meta:
        app_label = 'trailguide'
    
    name = models.CharField(max_length=255)
    type = models.ForeignKey(PointOfInterestType)
    
    # Geospatial components of the model
    geo = models.PointField()
    objects = models.GeoManager()
    
class PointOfInterestAdmin(admin.OSMGeoAdmin):
    pass

admin.site.register(PointOfInterest, PointOfInterestAdmin)