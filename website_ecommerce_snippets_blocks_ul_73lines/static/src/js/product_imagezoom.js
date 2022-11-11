odoo.define('website_product_image_zoom.product_imagezoom', function(require) {
"use strict";

    require('web.dom_ready');
    require('website_sale.website_sale');
    var publicWidget = require('web.public.widget');
    const {qweb, _t, _lt} = require('web.core');
    const weSnippetEditor = require('web_editor.snippet.editor');
    const ajax = require('web.ajax');

    weSnippetEditor.SnippetsMenu.include({
        async start() {
            await this._super(...arguments);
            if($('.pswp').length > 0) {
                var gallery = $('.pswp').data('instance');
                if(gallery){
                    gallery.close();
                }
                $('.pswp').removeAttr('class').addClass('pswp')
            }
        },
    });


});
