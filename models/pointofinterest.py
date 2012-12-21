from django.contrib.gis.db import models
from django.contrib import admin

class PointOfInterest(models.Model):
    """Point features representing interesting places"""
    class Meta:
        app_label = 'trailguide'
    
    # Geospatial components of the model
    geo = models.PointField()
    objects = models.GeoManager()
    
class PointOfInterestAdmin(admin.ModelAdmin):
    pass

admin.site.register(PointOfInterest, PointOfInterestAdmin)