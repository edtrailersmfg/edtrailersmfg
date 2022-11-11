$(document).ready(function () {
    $('#mid_header_top').hide();
    $('#mid_header_bottom').hide();
    $('.o_header_affix').hide();
    $('nav.navbar').addClass('fixed-bottom');
    $('ul.navbar-nav .dropdown').removeClass('dropdown').addClass('dropup');
    $('footer').css('padding-bottom','53px');
});
