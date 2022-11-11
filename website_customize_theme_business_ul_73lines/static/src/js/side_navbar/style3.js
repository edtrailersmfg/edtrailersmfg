odoo.define('website_customize_theme_business_ul_73lines.style3', function (require) {
    "use strict";
    require('web.dom_ready');

    $("nav.navbar.navbar-default").insertBefore($("div#wrap"));

    $('#dismiss, .overlay.overlay-3').on('click', function () {
    console.log("overrrr33333333333")
        $('#sidebar').removeClass('active');
        $('.overlay').removeClass('active');
    });

    if ($('#sidebarCollapse').hasClass('sidebarCollapse-3')){
        console.log("33333333333")
        $('#sidebarCollapse').on('click', function () {
            $('#sidebar').addClass('active');
            $('header').addClass('active');
            $('.overlay').addClass('active');
            $('.collapse.in').toggleClass('in');
            $('a[aria-expanded=true]').attr('aria-expanded', 'false');
        });
    }

    if($('.oe_website_login_container').length) {
        $('footer').hide();
        $('nav.navbar.navbar-default').hide();
    };

});
