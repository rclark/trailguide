from django.contrib.gis.db import models
from django.contrib.gis import geos, gdal
import json

class GeographicModel():
    class DeserializationError(Exception):
        pass

    proj_epsg = 3857
    proj_srs = gdal.SpatialReference(proj_epsg)
    objects = models.GeoManager()

    # This field should overriden in child classes
    geo = models.GeometryField(srid=4326)

    def geom_in_spherical_mercator(self):
        """Return the geometry of the object in spherical mercator projection"""
        transformed = self.geo.ogr.transform(self.proj_srs, clone=True)
        return geos.GEOSGeometry(transformed.wkt, self.proj_epsg)

    @classmethod
    def deserialize(cls, geojson_str):
        """Returns a model instance given some GeoJSON string"""

        # Some rudimentary validation of the GeoJSON string
        geojson = json.loads(geojson_str) # If that fails then the GeoJSON string was not a valid JSON object

        if "type" not in geojson.keys() or geojson["type"] != "Feature":
            raise cls.DeserializationError("Invalid GeoJSON object: not a Feature")

        kwargs = cls.deserialize_properties(geojson["properties"]) # Delegate property deserialization

        if "geometry" not in geojson.keys():
            raise cls.DeserializationError("Invalid GeoJSON object: no 'geometry' specified")

        kwargs["geo"] = geos.GEOSGeometry(json.dumps(geojson["geometry"])) # If that fails then the GeoJSON geometry was invalid

        # Now create an object and return it
        return cls(**kwargs)

    @classmethod
    def deserialize_properties(cls, properties_obj):
        """Return kwargs capable of creating an instance with these properties. Should be overridden by child classes"""
        return {}

    def serialize(self):
        """Serialize the object as GeoJSON"""
        return {
            "type": "Feature",
            "id": self.uri(),
            "geometry": json.loads(self.geo.geojson),
            "properties": self.serialize_properties()
        }

    def serialize_properties(self):
        """Serialize the properties of the object. Child classes should override this function"""
        return {}

    def uri(self):
        """Define the object's URI. Child classes should override this function"""
        return "http://{domain}/api/{model_name}/%s/" + str(self.pk)

