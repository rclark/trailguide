from django.contrib.gis.db import models
from django.contrib import admin

class Description(models.Model):
    """A base class for descriptions of segments, routes, regions, etc..."""
    class Meta:
        app_label = 'trailguide'
        
    objects = models.GeoManager()
    
class DescriptionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Description, DescriptionAdmin)