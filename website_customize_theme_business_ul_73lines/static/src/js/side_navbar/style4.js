odoo.define('website_customize_theme_business_ul_73lines.style4', function (require) {
    "use strict";
    require('web.dom_ready');

    $("nav.navbar.navbar-default").insertBefore($("div#wrap"));

    if ($('#sidebarCollapse').hasClass('sidebarCollapse-4')){
        console.log("44444444444")
        $('#sidebarCollapse').on('click', function () {
            $('#sidebar').toggleClass('active');
            $('#wrapwrap').toggleClass('active');
            $('header').toggleClass('active');
        });
    }

    if($('.oe_website_login_container').length) {
        $('footer').hide();
        $('nav.navbar.navbar-default').hide();
    };
});
