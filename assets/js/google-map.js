'use strict';

/*
 * Finds map locations via address.
 */

//------------------------
// Functions
//------------------------

let renderMap = (locations, target) => {
    let map = new google.maps.Map(target, {
        mapTypeId: google.maps.MapTypeId.STREET,
        zoom: 12
    });

    for (let i = 0; i < locations.length; i++) {
        let address = `${locations[i]}, San Francisco, USA`;

        let geocoder = new google.maps.Geocoder();

        geocoder.geocode({ 'address': address },
            (results, status) => {
                if (status == google.maps.GeocoderStatus.OK) {
                    new google.maps.Marker({
                        position: results[0].geometry.location,
                        map: map
                    });
                    map.setCenter(results[0].geometry.location);
                } else {
                    console.log(`Cannot find location: ${locations[i]}`);
                }
            }
        );
    }
};

// var googlemaps = (function() {
//     var geocoder;
//     var map;
//     var bounds = new google.maps.LatLngBounds();
//     var exportable = {};

//     exportable.renderGoogleMap = function(locations) {
//         map = new google.maps.Map(
//             document.getElementById("map"), {
//                 center: new google.maps.LatLng(37.4419, -122.1419),
//                 zoom: 13,
//                 mapTypeId: google.maps.MapTypeId.ROADMAP
//             });
//         geocoder = new google.maps.Geocoder();

//         for (let i = 0; i < locations.length; i++) {
//             this.geocodeAddress(locations[i]);
//         }
//     }
//     google.maps.event.addDomListener(window, "load", exportable.renderGoogleMap);

//     exportable.geocodeAddress = function(location) {
//         var address = location;
//         var title = location;
//         geocoder.geocode({
//                 'address': location,
//             },

//             function(results, status) {
//                 if (status == google.maps.GeocoderStatus.OK) {
//                     var marker = new google.maps.Marker({
//                         icon: 'http://maps.google.com/mapfiles/ms/icons/blue.png',
//                         map: map,
//                         position: results[0].geometry.location,
//                         title: title,
//                         animation: google.maps.Animation.DROP,
//                         address: address
//                     })
//                     this.infoWindow(marker, map, title, address);
//                     bounds.extend(marker.getPosition());
//                     map.fitBounds(bounds);
//                 } else {
//                     console.log("geocode of " + address + " failed:" + status);
//                 }
//             });
//     }

//     exportable.infoWindow = function infoWindow(marker, map, title, address) {
//         google.maps.event.addListener(marker, 'click', function() {
//             var html = "<div><h3>" + title + "</h3><p>" + address + "<br></div></p></div>";
//             iw = new google.maps.InfoWindow({
//                 content: html,
//                 maxWidth: 350
//             });
//             iw.open(map, marker);
//         });
//     }

//     return exportable;
// }());


//------------------------
// Event listeners
//------------------------

// For map modals
$('.location-link').click(function(e) {
    let location = $(this).data('location');
    let target = document.getElementById('map');
    let $modalTitle = $('.modal-title');
    let $modalBody = $('.modal-body');

    if (location) {
        $modalTitle.text(location);
        renderMap([location], target);
    }
});
