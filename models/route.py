from django.contrib.gis.db import models
from django.contrib.gis import admin
from django.db.models import Avg
from trailguide.models.trailhead import Trailhead
from trailguide.models.segment import Segment

class Route(models.Model):
    pass
    
    
class RouteAdmin(admin.OSMGeoAdmin):
    pass

admin.site.register(Route, RouteAdmin)