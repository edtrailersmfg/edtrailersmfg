odoo.define('website_customize_theme_business_ul_73lines.style6', function (require) {
    "use strict";
    require('web.dom_ready');

    $("nav.navbar.navbar-default").insertBefore($("div#wrap"));

    if ($('#sidebarCollapse5').hasClass('sidebarCollapse-6')){
        console.log("66666666666666")
        $('#sidebarCollapse5').addClass('active');
        $('#sidebarCollapse5').on('click', function () {
            $('#sidebar').toggleClass('active');
            $('header').toggleClass('active');
            $('#close').toggleClass('active');
            $('#wrapwrap').toggle();
        });
    }
    $('#close').on('click', function () {
        $('#close').removeClass('active');
        $('header').toggleClass('active');
        $('#sidebar').removeClass('active');
        $('#wrapwrap').css('display', 'block');
    });

    if ($('.oe_website_login_container').length) {
        $('footer').hide();
        $('nav.navbar.navbar-default').hide();
    }
    ;
});
