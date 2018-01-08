function initMap() {
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 7,
        center: locations[0]
    });
    // Create an array of alphabetical characters used to label the markers.
    var labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    // Add some markers to the map.
    // Note: The code uses the JavaScript Array.prototype.map() method to
    // create an array of markers based on a given "locations" array.
    // The map() method here has nothing to do with the Google Maps API.
    var markers = locations.map(function (location, i) {
        return new google.maps.Marker({
            position: location,
            label: labels[i % labels.length]
        });
    });
    // Add a marker clusterer to manage the markers.
    var markerCluster = new MarkerClusterer(map, markers,
        {imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'});

    for (i = 0; i < markers.length; i++) {
        console.log(markers[i]);
    }
}

// mark random
var locations = []

for (var i = 0; i < 5; i++) {
    locations.push(
        {
            lat: Math.random() * (3) + 3 + 37.7779056,
            lng: Math.random() * (3) + 3 - 122.414231
        }
    )
}

$(document).ready(function () {
    $('.carousel').carousel(
        {
            dist: 0,
            padding: 10,
            fullwidth: true,
            shift: 10

        }
    );

});