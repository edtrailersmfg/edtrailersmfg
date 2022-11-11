odoo.define('website_customize_theme_business_ul_73lines.style2', function (require) {
    "use strict";
    require('web.dom_ready');

    $("nav.navbar.navbar-default").insertBefore($("div#wrap"));

    if ($('#sidebarCollapse').hasClass('sidebarCollapse-2')){
        console.log("2222222222222")
        $('#sidebarCollapse').on('click', function () {
              $('header').toggleClass('active');
              $('#wrapwrap').toggleClass('active');
              console.log('testingggg');
        });
    }


    if($('.oe_website_login_container').length) {
        $('footer').hide();
        $('nav.navbar.navbar-default').hide();
    };
});
