from django.contrib.gis.db import models
from django.contrib import admin

class Region(models.Model):
    """Polygon features representing areas of interest"""
    class Meta:
        app_label = 'trailguide'
        
    # Geospatial components of the model
    geo = models.MultiPolygonField()
    objects = models.GeoManager()
    
class RegionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Region, RegionAdmin)