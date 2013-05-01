# Make sure that the app namespace is setup properly
root = @
app = root.trailapp ? root.trailapp = {}
models = app.models ? app.models = {}
collections = app.collections ? app.collections = {}

class models.GeoDataModel extends Backbone.Model
  """This is a base class for GeoJSON data pulled from Trailguide API"""

  modelName: "Trail Data" # Child classes should override this

  """
  Proper REST-ful architecture would have us maintain the GeoJSON "id" attribute as the URI for the resource -- in our
  case, that would be the URL that we access it on via API call. But this will confuse Backbone, as the entire URI
  would be appended to the urlRoot resulting in invalid API calls. Instead, the GeoJSON objects returned via API will
  include a "pk" property, which Backbone will treat as the ID.
  """
  idAttribute: "pk"

  parse: (response, options) ->
    """
    From Backbone.js docs:
    "parse is called whenever a model's data is returned by the server, in fetch, and save. The function is passed the
    raw response object, and should return the attributes hash to be set on the model."

    GeoJSON puts attributes in a 'properties' object, so we need to pull that out here for fetch to work as we expect

    @response: GeoJSON object retrieved by a fetch or save
    @options: unknown...
    """
    properties = response.properties or {}
    geometry = response.geometry or {}

    _.extend {}, properties, geometry: geometry

  toJSON: () ->
    """
    From Backbone.js docs:
    "Return a copy of the model's attributes for JSON stringification."

    Put the attributes hash in the right place to create a valid GeoJSON object
    """

    geojson =
      type: "Feature"
      id: @id
      properties: _.omit @attributes, "geometry"
      geometry: @get "geometry"

class collections.GeoDataCollection extends Backbone.Collection
  """A base class for GeoJSON data collections from the Trailguide API"""

  model: models.GeoDataModel # Child classes should override this

  url: () ->
    """Generate the URL for the API calls to this data set"""
    "/api/#{@model.prototype.modelName}"

  parse: (response, options) ->
    """
    From Backbone docs:
    "parse is called by Backbone whenever a collection's models are returned by the server, in fetch. The function is
    passed the raw response object, and should return the array of model attributes to be added to the collection."

    We will get back a GeoJSON FeatureCollection, and need to pull our the individual GeoJSON objects in order to create
    models

    @response: This will be a GeoJSON object returned by the Trailguide API
    @options: unknown
    """
    response.features or []

  toGeoJSON: () ->
    """
    Create a GeoJSON FeatureCollection from the data in this model. Useful for generating map layers
    """
    featureCollection =
      type: "FeatureCollection"
      features: ( m.toJSON() for m in @models )

class models.SegmentModel extends models.GeoDataModel
  modelName: "segment"

class collections.SegmentCollection extends collections.GeoDataCollection
  model: models.SegmentModel
