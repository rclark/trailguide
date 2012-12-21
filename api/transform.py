from django.db.models.fields import DateField, DateTimeField, TimeField
from django.db.models.fields.files import FileField, ImageField
from django.db.models.fields.related import ForeignKey, ManyToManyField, OneToOneField
from django.contrib.gis.db.models.fields import GeometryField, PointField, LineStringField, PolygonField, MultiPointField, MultiLineStringField, MultiPolygonField, GeometryCollectionField
import json

def to_json(model_instance):
    """Transform a model instance into a JSON string"""
    output = {}
    
    model = model_instance.__class__
    for field_name in model._meta.get_all_field_names():
        field = model._meta.get_field(field_name)
        
        # Field types that need special treatment
        
        # Date and Time fields need to return ISO-formatted strings
        if type(field) in [ DateField, DateTimeField, TimeField ]:
            output[field_name] = getattr(model_instance, field_name).isoformat()
            
        elif type(field) in [ FileField, ImageField ]:
            pass
        elif type(field) in [ ForeignKey, OneToOneField ]:
            pass
        elif type(field) is ManyToManyField:
            pass
        elif type(field) in [ GeometryField, PointField, LineStringField, PolygonField, MultiPointField, MultiLineStringField, MultiPolygonField, GeometryCollectionField ]:
            # Get the geometry as a GeoJSON string
            geojson_str = getattr(model_instance, field_name).json
            
            # Plug it in as a Python object to avoid double stringification
            output[field_name] = json.loads(geojson_str)
        
        # All other fields are simple
        else:
            output[field_name] = getattr(model_instance, field_name)
    
    return json.dumps(output)

def to_geojson(model_instance):
    """Transforms a model instance into a GeoJSON feature"""
    output = { "type": "Feature", "id": model_instance.pk, "properties": { } }
    properties = output["properties"]
    
    model = model_instance.__class__
    for field_name in model._meta.get_all_field_names():
        field = model._meta.get_field(field_name)
        
        # First deal with fields that are special cases
        
        # Date and Time fields need to return ISO-formatted strings
        if type(field) in [ DateField, DateTimeField, TimeField ]:
            properties[field_name] = getattr(model_instance, field_name).isoformat()
            
        elif type(field) in [ FileField, ImageField ]:
            pass
        elif type(field) in [ ForeignKey, OneToOneField ]:
            pass
        elif type(field) is ManyToManyField:
            pass
        
        # Geometry fields need to be plugged into the feature's geometry member
        elif type(field) in [ GeometryField, PointField, LineStringField, PolygonField, MultiPointField, MultiLineStringField, MultiPolygonField, GeometryCollectionField ]:
            # Get the geometry as a GeoJSON string
            geojson_str = getattr(model_instance, field_name).json
            
            # Plug it in as a Python object to avoid double stringification
            output["geometry"] = json.loads(geojson_str)
        
        # All other fields are simple
        else:
            properties["properties"][field_name] = getattr(model_instance, field_name)
    
    # Stringify it and return    
    return json.dumps(output)