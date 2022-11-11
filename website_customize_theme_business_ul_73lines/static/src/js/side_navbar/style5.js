odoo.define('website_customize_theme_business_ul_73lines.style5', function (require) {
    "use strict";
    require('web.dom_ready');

    $("nav.navbar.navbar-default").insertBefore($("div#wrap"));

    if ($('#sidebarCollapse5').hasClass('sidebarCollapse-5')){
        console.log("5555555555")
        $('#sidebarCollapse5').on('click', function () {
            $('#sidebar').toggleClass('active');
            $('header').toggleClass('active');
            $('#wrapwrap').toggleClass('active');
            $(this).toggleClass('active');
        });
    }
    if($('.oe_website_login_container').length) {
        $('footer').hide();
        $('nav.navbar.navbar-default').hide();
    };
});
