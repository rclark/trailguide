from django.contrib.gis.db import models
from django.contrib import admin

class UserUpload(models.Model):
    """A base class for files uploaded by a user"""
    class Meta:
        app_label = 'trailguide'
        
    # Geospatial components of the model
    objects = models.GeoManager()

class UserUploadAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserUpload, UserUploadAdmin)