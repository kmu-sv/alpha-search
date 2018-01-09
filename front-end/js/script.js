function initMap() {
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 7
    });

    var labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';

    var latlngbounds = new google.maps.LatLngBounds();

    for (i = 0; i < locations.length; i++) {
        var data = locations[i];
        var myLatlng = new google.maps.LatLng(data['lat'], data['lng']);
        var marker = new google.maps.Marker({
            position : myLatlng,
            map: map,
            label: labels[i % labels.length]
        });

        var idx = i;
        (function (marker, myLatlng, idx) {
            google.maps.event.addListener(marker, "click", function (e) {
                map.panTo(myLatlng);
                $('.carousel').carousel('set', idx);
            });

            $('#' + idx.toString() + "").on('click', function (e) {
                map.panTo(myLatlng);
            })

        })(marker, data, idx);

        latlngbounds.extend(marker.position);

    }

    var bounds = new google.maps.LatLngBounds();

    map.setCenter(latlngbounds.getCenter());
    map.fitBounds(latlngbounds);

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