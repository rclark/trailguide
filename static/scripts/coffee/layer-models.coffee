# Make sure that the app namespace is setup properly
root = @
app = root.trailapp ? root.trailapp = {}
models = app.models ? app.models = {}
collections = app.collections ? app.collections = {}

class models.MapLayer extends Backbone.Model
  """Base class for any map layers"""
  defaults: # These are the things you should probably pass in as options when creating a new one
    name: "Layer's Name"
    url: "http://where-do-i-get-data.com"
    visible: false
    selectable: false

  initialize: (options) ->
    @options = options
    @set "mapLayer", @createMapLayer()

  createMapLayer: () ->
    """
    This function should be overridden by child models and should produce an object that can be added to the map. There
    is some conflation of data and portrayal here, since the object produced will depend on the type of map that we're
    adding the thing to. We're pretty wedded to Leaflet though, so we might be able to get away with this
    """
    l = {}
    @trigger "layerReady", l

class models.GeoJsonMapLayer extends models.MapLayer
  """Class that generates an L.GeoJSON layer from data via JSON request"""
  initialize: (options) ->
    @set "data", options.data or new collections.GeoDataCollection()
    models.MapLayer.prototype.initialize.call @, options

  createMapLayer: () ->
    """
    This function needs to end up setting the model's "mapLayer" attribute, and triggering the "layerReady" event. Since
    the call for GeoJSON via collection.fetch is asynchronous, we listen for custom events.
    """
    @on "dataFetch.success", (dataCollection) ->
      l = new L.GeoJSON dataCollection.toGeoJSON()
      @set "mapLayer", l
      @trigger "layerReady", l

    @on "dataFetch.error", (response) ->
      console.log response

    @getData()

  getData: () ->
    """
    Get data from the server through the embedded Backbone.Collection.fetch(). Fire events upon asynchronous completion.
    """
    thisLayerModel = @
    collection = @get "data"
    collection.fetch
      success: (collection, response, options) ->
        thisLayerModel.trigger "dataFetch.success", collection
      error: (collection, response, options) ->
        thisLayerModel.trigger "dataFetch.error", response