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
      center: new L.LatLng 32.30280417394316, -110.85685729980469
      zoom: 11
      maxBounds: new L.LatLngBounds [[31.9592, -111.286], [32.9085, -110.1283]]
      minZoom: 11
      maxZoom: 15

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
        #code: "rclark.map-up7xciwe" # satellite layer
        #code: "rclark.map-lgs3w52k" # terrain layer
        code: "rclark.trails" # first-cut custom layer

    ,
      new app.models.MapboxLayer
        code: "rclark.map-gbal2acz" # Roads and Rivers without background

      #new app.models.StamenLayer
        #mapName: "watercolor"
    ,
      new app.models.GeoJsonMapLayer
        data: new app.collections.SegmentCollection()
  ]