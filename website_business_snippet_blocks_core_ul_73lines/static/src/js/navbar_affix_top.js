$(document).ready(function(){

       $(window).bind('scroll', function() {
       var navHeight = $( window ).height() / 3 - 70;
             if ($(window).scrollTop() > navHeight) {
                 $('.navbar').addClass('o_header_affix affix affixed');
             }
             else {
                 $('.navbar').removeClass('o_header_affix affix affixed');
             }
        });


});

