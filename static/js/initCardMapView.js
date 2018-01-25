var places = [];
var markers = [];
var map;

String.prototype.format = function () {
    string = this;
    for (k in arguments) {
        string = string.replace("{" + k + "}", arguments[k])
    }
    return string
};

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 14
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
            animation: google.maps.Animation.DROP,
            position: position,
            map: map
        });

        (function (marker, place, idx) {
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

if (navigator.geolocation) {
    console.log('Geolocation is supported!');
} else {
    console.log('Geolocation is not supported for this Browser/OS.');
}

window.onload = function () {

    $('#card-content').slimScroll({
        height: '100%'
    });

    var startPos;
    var geoSuccess = function (position) {
        startPos = position;

        var token = $("#token").val();

        urlAPI = "https://alpha-search.in:5000/mappedcafes/{0}/{1}/{2}"
            .format(
                token,
                startPos.coords.latitude,
                startPos.coords.longitude
            );

        map.panTo(
            {
                lat: startPos.coords.latitude,
                lng: startPos.coords.longitude
            }
        );

        console.log(urlAPI);

        $.ajax(
            {
                url: urlAPI,

                complete: function () {
                    $('.preloader-background').delay(1700).fadeOut('slow');
                    $('.preloader-wrapper').delay(1700).fadeOut();
                },

                success: function (data) {
                    var cards = $('.cards');
                    cards.carousel();

                    $.each(data, function (key, place) {
                        places.push(
                            {
                                lat: place['latitude'],
                                lng: place['longitude']
                            }
                        );

                        cards.append(
                            "<div class='card'><div class='card-image'>" +
                            "<img src='" + place['photourl'] + "' height='200px' width='auto'>" +
                            "</div><div class='card-content'><small>" + place['name'] + "\n" + place['address'] +
                            "</small></div></div>"
                        );
                    });
                    drop();
                }
            }
        );
    };
    navigator.geolocation.getCurrentPosition(geoSuccess);
};
