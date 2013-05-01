# Make sure that the app namespace is setup properly
root = @
app = root.trailapp ? root.trailapp = {}
views = app.views ? app.views = {}

class views.TrailMap extends Backbone.View
  initialize: (options) ->
    @setupMap()

  setupMap: () ->
    @map = new L.Map @el.id,
      center: new L.LatLng 33.610044573695625, -111.50024414062501
      zoom: 7
      layers: new L.TileLayer "http://a.tiles.mapbox.com/v3/rclark.map-up7xciwe/{z}/{x}/{y}.png"

  addLayer: (layerModel) ->
    @map.addLayer layerModel.get "mapLayer"

  removeLayer: (layerModel) ->
    @map.removeLayer layerModel.get "mapLayer"

trailapp.trailMap = new views.TrailMap
  el: $ "#map"