# Make sure that the app namespace is setup properly
root = @
app = root.trailapp ? root.trailapp = {}
models = app.models ? app.models = {}
collections = app.collections ? app.collections = {}

class models.MapLayer extends Backbone.Model
  ###Base class for any map layers###
  defaults: # These are the things you should probably pass in as options when creating a new one
    name: "Layer's Name"
    isLayerReady: false
    visible: false
    selectable: false

  initialize: (options) ->
    @options = options

    thisLayerModel = @
    @on "layerReady", () ->
      thisLayerModel.set "isLayerReady", true

    @set "mapLayer", @createMapLayer()

  createMapLayer: () ->
    ###
    This function should be overridden by child models and should produce an object that can be added to the map. There
    is some conflation of data and portrayal here, since the object produced will depend on the type of map that we're
    adding the thing to. We're pretty wedded to Leaflet though, so we might be able to get away with this
    ###
    l = {}
    @trigger "layerReady", l
    l

class models.GeoJsonMapLayer extends models.MapLayer
  ###Class that generates an L.GeoJSON layer from data via JSON request###
  createMapLayer: () ->
    ###
    This function needs to end up setting the model's "mapLayer" attribute, and triggering the "layerReady" event. Since
    the call for GeoJSON via collection.fetch is asynchronous, we listen for custom events.
    ###
    @on "dataFetch.success", (dataCollection) ->
      layer = new L.GeoJSON dataCollection.toGeoJSON()
      @set "mapLayer", layer
      @trigger "layerReady", layer

    @on "dataFetch.error", (response) ->
      console.log response

    @getData()

  getData: () ->
    ###
    Get data from the server through the embedded Backbone.Collection.fetch(). Fire events upon asynchronous completion.
    ###
    thisLayerModel = @
    collection = @get "data"
    if not collection?
      @trigger "dataFetch.error", "No GeoDataCollection was given to this GeoJsonMapLayer"
      null

    collection.fetch
      success: (collection, response, options) ->
        thisLayerModel.trigger "dataFetch.success", collection
      error: (collection, response, options) ->
        thisLayerModel.trigger "dataFetch.error", response

class models.MapboxLayer extends models.MapLayer
  ###Class that generates an L.TileLayer from MapBox###
  createMapLayer: () ->
    code = @get "code"
    if not code?
      console.log "Tried to create a MapBox layer without specifying its ID"
      null

    layer = new L.TileLayer "http://a.tiles.mapbox.com/v3/#{code}/{z}/{x}/{y}.png"
    @trigger "layerReady", layer
    layer

class models.StamenLayer extends models.MapLayer
  ###Class that generates a tile layer from Stamen Design###
  createMapLayer: () ->
    mapName = @get "mapName"
    if not mapName? or mapName not in [ "terrain", "watercolor", "toner" ]
      console.log "Tried to create a Stamen Designs map without specifying an appropriate mapName"
      null

    layer = new L.StamenTileLayer mapName
    @trigger "layerReady", layer
    layer
