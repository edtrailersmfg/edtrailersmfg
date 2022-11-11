odoo.define('website_snippet_client_carousel_ul_73lines.s_blogs_options', function (require) {
'use strict';

const config = require('web.config');
const core = require('web.core');
const publicWidget = require('web.public.widget');
const DynamicSnippetCarousel = require('website_carousel_base_ul_73lines.dynamic_product_snippet');

const DynamicSnippetBlogs = DynamicSnippetCarousel.extend({
    xmlDependencies: ['/website_snippet_client_carousel_ul_73lines/static/src/snippets/s_clients/000.xml'],
    selector: '.custom_snippet_clients',

    start: function() {
        this._super.apply(this, arguments);
        var width = $(window).width();
        if(width == 768){
            this.$target[0].dataset.numberOfElements = 2;
        }else if( width == 979 ){
            this.$target[0].dataset.numberOfElements = 2;
        }else if( width == 1024 ){
            this.$target[0].dataset.numberOfElements = 3;
        }else if( width == 479 ){
            this.$target[0].dataset.numberOfElements = 1;
        }else if( width == 320 ){
            this.$target[0].dataset.numberOfElements = 1;
        }
            this.template_key = 'website_snippet_client_carousel_ul_73lines.client';
            this._fetchData();
    },


});
publicWidget.registry.dynamic_snippet_clients = DynamicSnippetBlogs;
return DynamicSnippetBlogs;
});
