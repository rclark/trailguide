from django.contrib.gis.db import models
from django.contrib.gis import admin
from trailguide.models.constants import poi_types

class PointOfInterest(models.Model):
    """Point features representing interesting places"""
    class Meta:
        app_label = 'trailguide'
    
    name = models.CharField(max_length=255)
    type = models.IntegerField(choices=poi_types)
    
    # Geospatial components of the model
    geo = models.PointField()
    objects = models.GeoManager()

    def geojson(self):
        gj = { "type": "Feature" }
        gj["geometry"] = self.geo.geojson
        props = {
            "name": self.name,
            "type": [ self.type, self.get_type_display() ],
            "description": self.description
        }
        gj["properties"] = props
                
        return gj
        
        
    @classmethod
    def from_geojson(cls):
        # poi = GEOSGeomtry('{ "type": "Point", "coordinates": [] }')
        pass
    
    
class PointOfInterestAdmin(admin.OSMGeoAdmin):
    pass

admin.site.register(PointOfInterest, PointOfInterestAdmin)