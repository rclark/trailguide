# Make sure that the app namespace is setup properly
root = @
app = root.trailapp ? root.trailapp = {}
views = app.views ? app.views = {}

class views.TrailMap extends Backbone.View
  initialize: (options) ->
    @layers = options.layers or []
    @setupMap()

  setupMap: () ->
    @map = map = new L.Map @el.id,
      center: new L.LatLng 33.610044573695625, -111.50024414062501
      zoom: 7

    # This block will automatically add all layers to the map, which probably is not what we want
    addLayer = @addLayer
    _.each @layers, (layerModel) ->
      if layerModel.get "isLayerReady"
        map.addLayer layerModel.get "mapLayer"
      else
        layerModel.on "layerReady", (layer) ->
          map.addLayer layer

  addLayer: (layerModel) ->
    @map.addLayer layerModel.get "mapLayer"

  removeLayer: (layerModel) ->
    @map.removeLayer layerModel.get "mapLayer"

trailapp.trailMap = new views.TrailMap
  el: $ "#map"
  layers: [
      new app.models.MapboxLayer
        code: "rclark.map-up7xciwe"
    ,
      new app.models.GeoJsonMapLayer
        data: new app.collections.SegmentCollection()
  ]