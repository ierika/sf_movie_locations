'use strict';

//------------------------
// Event listeners
//------------------------

$('.location-link').click(function(e) {
    let location = $(this).data('location');
    let target = document.getElementById('map');
    let $modalTitle = $('.modal-title');
    let $modalBody = $('.modal-body');
    if (location) {
        $modalTitle.text(location);
        renderMap(location, target);
    }
});
