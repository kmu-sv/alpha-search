var places = [];
var markers = [];
var map;

var paramsList = location.search.substring(1).split("&");

function paramsFunc(paramsNm) {
    var nullChk = "";
    for (var i = 0; i < paramsList.length; i++) {
        if (paramsNm == paramsList[i].split("=")[0]) {
            return paramsList[i].split("=")[1];
        } else {
            if (i == paramsList.length - 1) nullChk = true;
        }
    }
    if (nullChk) {
        alert("Not found parameter");
    }
}

$.ajax(
    {
        url: "http://www.alpha-search.in:5000/mappedcafes/" + paramsFunc("token"),

        complete: function () {
            $('.preloader-background').delay(1700).fadeOut('slow');
            $('.preloader-wrapper').delay(1700).fadeOut();
        },

        success: function (data) {
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
                    fullwidth: true,
                    padding: 10,
                    shift: 10
                }
            );

            map.panTo(places[0]);

            var activeCard = null;

            setInterval(function (e) {
                var currentActiveCard = $('.active');
                if (activeCard !== currentActiveCard) {
                    activeCard = currentActiveCard;
                    activeCard.trigger("click");
                }
            }, 500);

            drop();
        }
    }
);

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