function initMap() {
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 7
    });

    var latLngBounds = new google.maps.LatLngBounds();

    for (var location = 0; location < locations.length; location++) {
        var data = locations[location];
        var myLatlng = new google.maps.LatLng(data['lat'], data['lng']);
        var marker = new google.maps.Marker({
            position: myLatlng,
            map: map,
            label: String.fromCharCode(65 + location)
        });

        var idx = location;
        (function (marker, myLatlng, idx) {
            google.maps.event.addListener(marker, "click", function (e) {
                map.panTo(myLatlng);
                $('.carousel').carousel('set', idx);
            });

            $('#' + idx.toString() + "").on('click', function (e) {
                map.panTo(myLatlng);
            });

            $('.carousel').on("mouseover", function (e) {
                var activeCard = $('.active');
                activeCard.trigger("click");
            });

        })(marker, data, idx);

        latLngBounds.extend(marker.position);

    }

    var bounds = new google.maps.LatLngBounds();

    map.setCenter(latLngBounds.getCenter());
    map.fitBounds(latLngBounds);

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