from django.contrib.gis.db import models
from django.contrib.gis import admin

class Trailhead(models.Model):
    """Point features representing trailheads"""
    class Meta:
        app_label = 'trailguide'
    
    # Geospatial components of the model 
    geo = models.PointField()
    objects = models.GeoManager()
    
class TrailheadAdmin(admin.OSMGeoAdmin):
    pass

admin.site.register(Trailhead, TrailheadAdmin)
    