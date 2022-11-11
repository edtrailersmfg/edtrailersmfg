odoo.define('website_product_image_zoom.search_suggestion', function(require) {
"use strict";

    require('web.dom_ready');
    require('website_sale.website_sale');
    var SearchBar = require('@website/snippets/s_searchbar/000')[Symbol.for("default")];
    const ajax = require('web.ajax');
    const {qweb, _t, _lt} = require('web.core');
    var publicWidget = require('web.public.widget');
    ajax.loadXML('/website_ecommerce_snippets_blocks_ul_73lines/static/src/snippets/search_suggestion_inherit.xml', qweb);

    publicWidget.registry.searchBar.include({
        xmlDependencies: ['/website_ecommerce_snippets_blocks_ul_73lines/static/src/snippets/search_suggestion_inherit.xml'],

        _render: function (res) {
            if (res && this.limit) {
                const results = res['results'];
                this.is_category = !(_.isEmpty(_.find(results, function(val){
                    return val.website_url && val.website_url.startsWith('/shop/category');
                })));
                this.is_products = !(_.isEmpty(_.find(results, function(val){
                    return val.website_url && !val.website_url.startsWith('/shop/category');
                })));
            }
            this._super.apply(this, arguments);
        },
    });

    $(document).on('click', '.product_detail_img', function(elem) {
        if($('body').hasClass('editor_enable')) { return; }
        if($('.pswp').length < 1) { return; }
        var $itemdata = []
        var $image = $(elem.currentTarget).parents('.col-md-6').find('.carousel-inner').children();
        var $index_current = $(elem.currentTarget).parents('.col-md-6').find('li.active').data('slide-to');
        _.each($image, function (elem) {
            var $image_src = $(elem).find('.product_detail_img').attr('src')
            $itemdata.push({'src': $image_src,'w': 0,'h': 0,})
        });
        var pswpElement = document.querySelectorAll('.pswp')[0];
        var items = $itemdata;
        var options = {
            index: $index_current,
        };
        var gallery = new PhotoSwipe(pswpElement, PhotoSwipeUI_Default, items, options);
        gallery.listen('gettingData', function(index, item) {
            if (item.w < 1 || item.h < 1) { // unknown size
                var img = new Image();
                img.onload = function() { // will get size after load
                item.w = this.width; // set image width
                item.h = this.height; // set image height
                   gallery.invalidateCurrItems(); // reinit Items
                   gallery.updateSize(true); // reinit Items
                }
            img.src = item.src; // let's download image
            }
        });
        gallery.init();
        $('.pswp').data('instance', gallery);
    });
});