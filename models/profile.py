from django.contrib.gis.db import models
from django.contrib import admin
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """Persist a user's profile information"""
    class Meta:
        app_label = 'trailguide'
        
    # Relate a user's profile to the user herself
    user = models.OneToOneField(User)
    
    # Geospatial components of the model
    objects = models.GeoManager()
    
class UserProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile, UserProfileAdmin)