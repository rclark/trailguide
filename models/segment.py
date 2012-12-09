from django.contrib.gis.db import models
from django.contrib import admin

class Segment(models.Model):
    """Line features representing a trail segment"""
    class Meta:
        app_label = 'trailguide'
    
    # Geospatial components of the model
    geo = models.LineStringField()
    objects = models.GeoManager()
    
class SegmentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Segment, SegmentAdmin)