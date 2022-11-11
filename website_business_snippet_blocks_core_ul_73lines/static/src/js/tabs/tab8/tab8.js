$(document).ready(function($){
    $("#services-tabs").responsiveTabs({
      animation: 'slide'
    });

    $('.filtering').on( 'click', 'span', function() {
      var filterValue = $(this).attr('data-filter');
      $gallery.isotope({ filter: filterValue });
    });
});
