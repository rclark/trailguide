root = @
if not root.trailapp? then root.trailapp = trailapp = {} else trailapp = root.trailapp
if not trailapp.views? then trailapp.views = views = {} else views = trailapp.views

class views.TrailMap extends Backbone.View
  initialize: (options) ->
    @setupMap()

  setupMap: () ->
    @map = new L.Map @el.id,
      center: new L.LatLng 33.610044573695625, -111.50024414062501
      zoom: 7
      layers: new L.TileLayer "http://a.tiles.mapbox.com/v3/rclark.map-x9c4guq4/{z}/{x}/{y}.png"

trailapp.trailMap = new views.TrailMap
  el: "#map"