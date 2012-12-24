from django.contrib.gis.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
    """Persist a user's profile information"""
    class Meta:
        app_label = 'trailguide'
        
    # Relate a user's profile to the user herself
    user = models.OneToOneField(User)
    
    # Geospatial components of the model
    objects = models.GeoManager()

# This bit automatically generates a user profile for each created user
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)        
post_save.connect(create_user_profile, sender=User)
    
class UserProfileAdmin(admin.ModelAdmin):
    pass
admin.site.register(UserProfile, UserProfileAdmin)