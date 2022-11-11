odoo.define('website_snippet_product_carousel_ul_73lines.dynamic_product_snippet', function (require) {
'use strict';

const config = require('web.config');
const core = require('web.core');
const publicWidget = require('web.public.widget');
const DynamicSnippetCarousel = require('website_carousel_base_ul_73lines.dynamic_product_snippet');
var _t = core._t;
var wSaleUtils = require('website_sale.utils');
var Dialog = require('web.Dialog');
var ajax = require('web.ajax');

const DynamicProductsSnippet = DynamicSnippetCarousel.extend({
    xmlDependencies: ['/website_snippet_product_carousel_ul_73lines/static/src/snippets/s_cart_products/000.xml',
    '/website/static/src/snippets/s_dynamic_snippet/000.xml'],
    selector: '.custom_dynamic_product_snippet',
    read_events: _.extend(DynamicSnippetCarousel.prototype.read_events, {
        'click .js_add_cart': '_onAddToCart',
    }),
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
        if(this.$target.hasClass('grid_active')){
            this.template_key = 'website.s_dynamic_snippet.grid';
            this._fetchData();
        }else{
            this.template_key = 'website_snippet_product_carousel_ul_73lines.carousel';
            this._fetchData();
        }
    },
    _onAddToCart: function (ev) {
        var self = this;
        var $card = $(ev.currentTarget).closest('form');
        this._rpc({
            route: "/shop/cart/update_json",
            params: {
                product_id: $card.find('input[data-product-id]').data('product-id'),
                add_qty: 1
            },
        }).then(function (data) {
            var $navButton = $('header .o_wsale_my_cart').first();
            var fetch = self._fetchData();
            var animation = wSaleUtils.animateClone($navButton, $(ev.currentTarget).closest('form'), 25, 40);
            Promise.all([fetch, animation]).then(function (values) {
                wSaleUtils.updateCartNavBar(data);
                self._render();
            });
        });
    },
    _onClickProductQuickView: function(ev){
        var self = this;
        var productID = $(ev.currentTarget).data('productId');
        var dialog = new Dialog(this, { title: _t("Quick View") });
        dialog.opened().then(function () {
            dialog.$modal.find('.modal-dialog').addClass('modal-dialog-centered ul_quick_modal');
            dialog.$footer.remove();
            ajax.jsonRpc('/get/product_quick_view', 'call', {
            'options': {
                productID: productID,
            }
            }).then(data => {
                dialog.$el.append(data);
                var urlRegex = /(\?(?:|.*&)(?:u|url|body)=)(.*?)(&|#|$)/;
                var titleRegex = /(\?(?:|.*&)(?:title|text|subject)=)(.*?)(&|#|$)/;

                var title = encodeURIComponent($('title').text());
                dialog.$el.find('a').each(function () {
                    var $a = $(this);
                    var url = $a.data('url');
                    $a.attr('href', function (i, href) {
                        return href.replace(urlRegex, function (match, a, b, c) {
                            return a + url + c;
                        }).replace(titleRegex, function (match, a, b, c) {
                            if ($a.hasClass('s_share_whatsapp')) {
                                return a + title + url + c;
                            }
                            return a + title + c;
                        });
                    });
                    if ($a.attr('target') && $a.attr('target').match(/_blank/i) && !$a.closest('.o_editable').length) {
                        $a.on('click', function () {
                            window.open(this.href, '', 'menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=550,width=600');
                            return false;
                        });
                    }
                });
            });
        });
        dialog.open();
    },

});
publicWidget.registry.dynamic_product_snippet = DynamicProductsSnippet;
return DynamicProductsSnippet;

});
