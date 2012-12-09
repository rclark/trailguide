from django.contrib.gis.db import models
from django.contrib import admin

class Trailhead(models.Model):
    """Point features representing trailheads"""
    class Meta:
        app_label = 'trailguide'
        
    geo = models.PointField()
    objects = models.GeoManager()
    
class TrailheadAdmin(admin.ModelAdmin):
    pass

admin.site.register(Trailhead, TrailheadAdmin)
    