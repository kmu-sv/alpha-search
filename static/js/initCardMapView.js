var places = [];
var markers = [];
var currentLocation;
var map;
var ajaxData = [];

String.prototype.format = function () {
    string = this;
    for (k in arguments) {
        string = string.replace("{" + k + "}", arguments[k])
    }
    return string
};

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
            animation: google.maps.Animation.DROP,
            position: position,
            map: map
        });

        markers.push(newMarker);

        google.maps.event.addListener(newMarker, "click", function (e) {
            setCardAndMap(this, places[idx], idx);
        });
        $('#' + idx.toString() + "").on('click', function (e) {
            setCardAndMap(markers[idx], places[idx], idx);
        });
    }, timeout);
}

function setCardAndMap(marker, place, idx) {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setOptions({'opacity': 0.3});
    }

    controlDisplay(idx);

    marker.setOptions({'opacity': 1});

    console.log("click card");

    map.panTo(
        new google.maps.LatLng(
            (currentLocation['lat'] + place['lat']) / 2,
            (currentLocation['lng'] + place['lng']) / 2
        )
    );
}

function controlDisplay(idx) {

    var place = ajaxData[idx];

    $("#detail-image").attr(
        "src",
        place['photourl']
    );

    $("#detail-title").text(
        place['name']
    );

    var detailParagraph = $("#detail-p");
    detailParagraph.empty();
    detailParagraph.append(
        "<p>" + place["address"] + "</p>"
    );

    // for (var info in place) {
    //     detailContent.append(
    //         "<p>" + info + " : " + place[info] + "</p>"
    //     );
    // }

    var cards = $(".cards");
    var detailInfo = $(".detail-info");

    if (cards.css("display") == "none") {
        cards.show();
        detailInfo.hide();
    } else {
        cards.hide();
        detailInfo.show();
    }
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

    Materialize.toast('Hello!! My name is Alpha Search!');
    Materialize.toast("I'm looking for a cafe to recommend you...");

    $('#card-content').slimScroll({
        height: '100%'
    });

    var startPos;
    var geoSuccess = function (position) {
        startPos = position;

        var token = $("#token").val();

        currentLocation = {
            lat: startPos.coords.latitude,
            lng: startPos.coords.longitude
        };

        urlAPI = "https://alpha-search.in:5000/mappedcafes/{0}/{1}/{2}"
            .format(
                token,
                currentLocation['lat'],
                currentLocation['lng']
            );

        map.panTo(currentLocation);

        var marker = new google.maps.Marker({
            position: map.getCenter(),
            icon: {
                path: google.maps.SymbolPath.CIRCLE,
                fillColor: 'white',
                fillOpacity: 0.8,
                strokeColor: 'green',
                scale: 7,
                strokeWeight: 5
            },
            draggable: true,
            map: map
        });

        console.log(urlAPI);

        $.ajax(
            {
                url: urlAPI,

                error: function () {
                    Materialize.toast("Aah! Failed! I'll look again. :(");
                    setTimeout(function () {
                        location.reload();
                    }, 3500)
                },

                success: function (data) {

                    ajaxData = data;

                    var cards = $('.cards');
                    cards.carousel();

                    $.each(data, function (key, place) {
                        places.push(
                            {
                                lat: place['latitude'],
                                lng: place['longitude']
                            }
                        );

                        console.log(place);

                        var icon = "";

                        if (place['wi_fi_available']) {
                            icon += "<i class='material-icons'>wifi</i>";
                        }

                        if (place['parking_available']) {
                            icon += "<i class='material-icons'>local_parking</i>";
                        }

                        cards.append(
                            "<div class='waves-effect waves-light card' id='" + key.toString() + "'>" +
                            "<div class='card-image'>" +
                            "<img src='" + place['photourl'] + "' height='200px' width='auto'>" +
                            "</div>" +
                            "<div class='card-content'>" +
                            "<p style='float: right'>" + icon + "</p>" +
                            "<span class='card-title grey-text text-darken-4'>" + place['name'] + "</span>" +
                            "<p>" + place['address'] + "</p>" +
                            "</div>" +
                            "</div>"
                        );
                    });

                    Materialize.toast('I found a cafe to recommend you!!');
                    drop();

                    setTimeout(function () {
                        $('.preloader-background').delay(1700).fadeOut('slow');
                        $('.preloader-wrapper').delay(1700).fadeOut();
                        Materialize.Toast.removeAll();
                    }, 2500);
                }
            }
        );
    };
    navigator.geolocation.getCurrentPosition(geoSuccess);
};
