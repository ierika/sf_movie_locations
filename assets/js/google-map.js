'use strict';

let renderMap = (location, target) => {
    var address = `${location}, San Francisco, USA`;

    var map = new google.maps.Map(target, {
        mapTypeId: google.maps.MapTypeId.STREET,
        zoom: 12
    });

    var geocoder = new google.maps.Geocoder();
    geocoder.geocode(
        { 'address': address },
        function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                new google.maps.Marker({
                    position: results[0].geometry.location,
                    map: map
                });
                map.setCenter(results[0].geometry.location);
            } else {
                alert('Address not found!');
                throw new Error('Address not found!');
            }
        }
    );
    return map;
};
