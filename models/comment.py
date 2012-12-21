from django.contrib.gis.db import models
from django.contrib import admin

class Comment(models.Model):
    """A base class for comments provided by users"""
    class Meta:
        app_label = 'trailguide'
    
    # Geospatial components of the model    
    objects = models.GeoManager()

class CommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Comment, CommentAdmin)