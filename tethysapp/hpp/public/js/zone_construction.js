var map;
var view;

require(["esri/Map", "esri/views/MapView"], function(Map, MapView) {
        var map = new Map({
          basemap: "streets"
        });
        var view = new MapView({
          container: "showmap", // Reference to the scene div created in step 5
          map: map, // Reference to the map object created before the scene
          zoom: 12, // Sets zoom level based on level of detail (LOD)
          center: [-93.25, 44.75] // Sets center point of view using longitude,latitude
        });
      });