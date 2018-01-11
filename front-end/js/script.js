var places = [];
var markers = [];
var map;

$.getJSON("data.json", function (data) {
    var cards = $('.carousel');
    cards.carousel();

    $.each(data, function (key, place) {
        places.push(
            {
                lat: place['latitude'],
                lng: place['longitude']
            }
        );

        cards.append("" +
            "<div class='carousel-item' id='" + key.toString() + "'>" +
            "<div class='card'><div class='card-image'>" +
            "<img src='" + place['photourl'][0] + "' height='130px'>" +
            "</div><div class='card-content'><small>" + place['name'] + "\n" + place['address'] +
            "</small></div></div></div>"
        );

        if (cards.hasClass('initialized')) {
            cards.removeClass('initialized')
        }
    });

    cards.carousel(
        {
            dist: 0,
            padding: 10,
            fullwidth: true,
            shift: 10

        }
    );
});

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 15
    });
}

function drop() {
    clearMarkers();
    for (var i = 0; i < places.length; i++) {
        addMarkerWithTimeout(places[i], i * 200, i);
    }
}

function addMarkerWithTimeout(position, timeout, idx) {
    window.setTimeout(function () {

        newMarker = new google.maps.Marker({
            position: position,
            map: map,
            animation: google.maps.Animation.DROP
        });

        (function (marker, place, idx) {
            google.maps.event.addListener(marker, "click", function (e) {
                console.log("click marker");
                map.panTo(new google.maps.LatLng(place['lat'], place['lng']));
                $('.carousel').carousel('set', idx);
            });

            $('#' + idx.toString() + "").on('click', function (e) {
                console.log("click card");
                map.panTo(new google.maps.LatLng(place['lat'], place['lng']));
            });
        })(newMarker, places[idx], idx);

        markers.push(newMarker);
    }, timeout);
}

function clearMarkers() {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
    }
    markers = [];
}

$(document).ready(function (event) {
    map.panTo(places[0]);
    drop();
});
