var ajaxData = [];
var currentLocation;
var directionsService, directionsDisplay;
var markers = [];
var map;
var places = [];

String.prototype.format = function () {
    string = this;
    for (k in arguments) {
        string = string.replace("{" + k + "}", arguments[k])
    }
    return string
};

function initMap() {
    directionsService = new google.maps.DirectionsService;
    directionsDisplay = new google.maps.DirectionsRenderer;

    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 14
    });

    windowLoad()
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

    directionsDisplay.setMap(map);

    directionsService.route({
        origin: {lat: currentLocation['lat'], lng: currentLocation['lng']},
        destination: {lat: ajaxData[idx]['latitude'], lng: ajaxData[idx]['longitude']},
        travelMode: 'WALKING'
    }, function (response, status) {
        if (status === 'OK') {
            directionsDisplay.setDirections(response);
        } else {
            window.alert('Directions request failed due to ' + status);
        }
    });

    controlDisplay(idx);

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

    var star = (function () {
        var rStar = "";

        for (var i = 0; i < parseInt(place['rating'], 10); i++) {
            rStar += "<i class='material-icons tiny'>star</i>";
        }

        if (place['rating'] % 1 > 0) {
            rStar += "<i class='material-icons tiny'>star_half</i>";
        }

        var cntStar = (rStar.match(/material-icons/g) || []).length;

        for (var cntStar; cntStar < 5; cntStar++) {
            rStar += "<i class='material-icons tiny'>star_border</i>";
        }

        return rStar;
    })();

    var link = (function () {
        var rLink = "";
        if (place['yelpurl'] != "") {
            rLink += "<a target='_blank' href='" + place['yelpurl'] + "'>Yelp</a>"
        }
        return rLink;
    })();

    var detailParagraph = $("#detail-p");
    detailParagraph.empty();
    detailParagraph.append(
        "<p style='float: right'>" + setIcon(place) + "</p>" +
        "<p>" + star + "</p>" +
        "<p><i class='material-icons tiny'>local_phone</i>&nbsp" + place["phone_number"] + "</p>" +
        "<p><i class='material-icons tiny'>home</i>&nbsp" + place["address"] + "</p>" +
        "<p><i class='material-icons tiny'>link</i>&nbsp" + link + "</p>"
    )
    ;

    var cards = $(".cards");
    var detailInfo = $(".detail-info");

    var opacityMarker = function (opacity) {
        for (var i = 0; i < markers.length; i++) {
            markers[i].setOptions({'opacity': opacity});
        }
    };

    if (cards.css("display") == "none") {
        directionsDisplay.setMap(null);
        opacityMarker(1);
        map.setZoom(14);
        map.panTo(
            new google.maps.LatLng(
                currentLocation['lat'],
                currentLocation['lng']
            )
        );
        cards.show();
        detailInfo.hide();
    } else {
        opacityMarker(0);
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

var windowLoad = function () {

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

                        console.log(place);

                        places.push(
                            {
                                lat: place['latitude'],
                                lng: place['longitude']
                            }
                        );

                        var icon = setIcon(place);

                        cards.append(
                            "<div class='waves-effect waves-light card' id='" + key.toString() + "'>" +
                            "<div class='card-image'>" +
                            "<img src='" + place['photourl'] + "' height='220px' width='auto'>" +
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

function setIcon(place) {
    var icon = "";

    if (place['wi_fi_available']) {
        icon += "<i class='material-icons tiny'>wifi</i>";
    }

    if (place['parking_available']) {
        icon += "<i class='material-icons tiny'>local_parking</i>";
    }

    return icon;
}