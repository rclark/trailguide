from django.contrib.gis.db import models
from django.contrib.gis import admin
from django.db.models import Q

class Trailhead(models.Model):
    """Point features representing trailheads"""
    class Meta:
        app_label = 'trailguide'
        
    name = models.CharField(max_length=255)
    
    # Geospatial components of the model 
    geo = models.PointField(geography=True, srid=4326)
    objects = models.GeoManager()
    
    def routes(self):
        """
        Return a list of routes that use this trailhead
        as a starting or ending point.

        Route = get_model("trailguide", "Route")
        return Route.objects.filter(Q(th_start=self) | Q(th_end=self))
        """
    
class TrailheadAdmin(admin.OSMGeoAdmin):
    pass

admin.site.register(Trailhead, TrailheadAdmin)
    