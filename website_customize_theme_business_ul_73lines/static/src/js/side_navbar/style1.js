odoo.define('website_customize_theme_business_ul_73lines.style1', function (require) {
    'use strict';
    require('web.dom_ready');

    $("nav.navbar.navbar-default").insertBefore($("div#wrap"));

    if ($('#sidebarCollapse').hasClass('sidebarCollapse-1')){
        console.log("1111111111111111")
       $('#sidebarCollapse').on('click', function () {
            $('header').toggleClass('active');
            $('#wrapwrap').toggleClass('active');
            $('#sidebar').toggleClass('active');
            $('.collapse.in').toggleClass('in');
            $('a[aria-expanded=true]').attr('aria-expanded', 'false');
        });
    }

    if($('.oe_website_login_container').length) {
        $('footer').hide();
        $('nav.navbar.navbar-default').hide();
    };

});
