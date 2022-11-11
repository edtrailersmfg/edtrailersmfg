$(document).ready(function(){
      $('.oe_website_sale').each(function() {
            var oe_website_sale = this;

            var $attr_to_reorder = $('#products_grid_before > form.js_attributes', oe_website_sale);

            var $categ_to_reorder = $('#products_grid_before > ul#o_shop_collapse_category', oe_website_sale);

            var $heading_to_reorder = $('.category-heading',oe_website_sale);

            $categ_to_reorder.insertBefore($attr_to_reorder);

            $heading_to_reorder.insertBefore($categ_to_reorder);
        });

        /*---- Alternative Product ----*/
        if($('.owl-carousel').length){
            $('.owl-carousel').owlCarousel({
                loop: false,
                autoplay: true,
                pagination: true,
                responsive: {
                    0: {
                        items: 2,
                        nav: false
                    },
                    600: {
                        items: 2,
                        nav: false
                    },
                    1000: {
                        items: 2,
                        nav: true,
                    }
                },
                 navText : ["<i class='fa fa-chevron-left'></i>","<i class='fa fa-chevron-right'></i>"]
            });
        }
});

$(document).ready(function() {
    if($('.ul_vertical_product_slider').length){
        if($('.o_carousel_product_indicators').length){
            $('.o_carousel_product_indicators').removeClass('o_carousel_product_indicators');
        }
}
});