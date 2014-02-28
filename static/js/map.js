// set variables
var geocoder;
var map;
var lat;
var lng;

// initialize the map per v3 spec on google
//
function initialize() {
  geocoder = new google.maps.Geocoder();
  var latlng = new google.maps.LatLng(lat,lng);
  var mapOptions = {
    zoom: 13,
    center: latlng
  }
  map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
}


// find the address based on the variables lat  and lng
//
function codeAddress() {
  var latlng =  new google.maps.LatLng(lat,lng);
  geocoder.geocode( { 'latLng': latlng}, function(results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
      map.setCenter(results[0].geometry.location);
      var marker = new google.maps.Marker({
          map: map,
          position: results[0].geometry.location
      });
    } else {
      alert('Geocode was not successful for the following reason: ' + status);
    }
  });
}


// get the map via the json request api/map
//
$.getJSON( "api/map", function( data ) {
  //console.log(data);
  lat = data['lat'];
  lng = data['lng'];
  initialize();
  codeAddress();

}).error(function(error){console.log(error)});
