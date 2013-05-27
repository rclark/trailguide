from django.contrib.gis.db import models
from django.contrib.gis import geos, gdal
from django.contrib.gis.geos import Polygon
import json

class GeographicModel():
    class DeserializationError(Exception):
        pass

    proj_epsg = 3857
    proj_srs = gdal.SpatialReference(proj_epsg)

    # This field should overriden in child classes
    geo = models.GeometryField(srid=4326)

    def geom_in_spherical_mercator(self):
        """Return the geometry of the object in spherical mercator projection"""
        transformed = self.geo.ogr.transform(self.proj_srs, clone=True)
        return geos.GEOSGeometry(transformed.wkt, self.proj_epsg)

    @classmethod
    def filtered_set(cls, query_dict):
        # Find keys in the query that are also fields in the model
        query_keys = [key.lower() for key in query_dict.keys() if key.lower() in cls._meta.get_all_field_names()]

        query_params = {}
        for key in query_keys:
            query_params[key] = query_dict[key]

        # Also allow for a bbox parameter
        if "bbox" in query_dict.keys():
            box = Polygon.from_bbox([float(coord) for coord in query_dict["bbox"].split(",")])
            query_params["geo__intersects"] = box

        return cls.objects.filter(**query_params)

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
        valid_keys = [key for key in properties_obj.keys() if key in cls._meta.get_all_field_names()]

        kwargs = {}
        for key in valid_keys:
            kwargs[key] = properties_obj[key]

        return kwargs


    def serialize(self):
        """Serialize the object as GeoJSON"""
        properties = self.serialize_properties()
        if "pk" not in properties.keys():
            properties["pk"] = self.pk

        return {
            "type": "Feature",
            "id": self.uri(),
            "geometry": json.loads(self.geo.geojson),
            "properties": properties
        }

    def serialize_properties(self):
        """Serialize the properties of the object. Child classes should override this function"""
        return {}

    def uri(self):
        """Define the object's URI."""
        return "http://{domain}/api/{model_name}/%s/" % str(self.pk)

