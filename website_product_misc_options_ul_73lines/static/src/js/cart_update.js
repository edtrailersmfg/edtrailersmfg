odoo.define('website_product_misc_options_ul_73lines.cart_update', function (require) {
'use strict';

    const wUtils = require('website.utils');
    const utils = require('website_sale.utils');

    var publicWidget = require('web.public.widget');
    var core = require('web.core');
    var _t = core._t;
    require('website_sale.website_sale');

    publicWidget.registry.websiteSaleSideBarCart = publicWidget.Widget.extend({
         selector: '#sidebar_cart_lines',
         events: {
            'click #clear_cart': '_onClearCart'
         },
         init: function(){
            this._super.apply(this, arguments);
         },

         start: function () {
            this._super.apply(this, arguments);
            core.bus.on('cart_sidebar_updated', this, this._setData);
            this._setData();
         },

         _setData: function(){
            this._rpc({
                route: "/shop/cart/sidebar",
            }).then(function (data) {
                 if($("#sidebar_cart_lines").length){
                    $("#sidebar_cart_lines").find("#sidebar_js_cart_lines").html(data['cart_lines']).removeClass('alert alert-info');
                    $("#sidebar_cart_lines").find("#sidebar_short_cart_summary").html(data['short_cart_summary']).removeClass('alert alert-info');
                }
            });
         },

         _onClearCart: function(e){
            e.preventDefault();
            this._rpc({
                route: '/shop/clear/cart'
            }).then( () => {
                return this._setData();
            }).then(() => {
                if($("#cart_products").length){
                    $("#cart_products").find('tr').find('.js_quantity').val(0).trigger('change');
                }
            });
         },
    });

    publicWidget.registry.WebsiteSale.include({
        _onClickAdd: function (ev) {
            this._super.apply(this, arguments).then( function(){
                core.bus.trigger('cart_sidebar_updated')
            });
        }
    });

    const originalFunction = utils.updateCartNavBar;
    utils.updateCartNavBar = function (data) {
        originalFunction.apply(this, [data]);
        if($("#sidebar_cart_lines").length){
            $("#sidebar_js_cart_lines").first().html(data['website_sale.cart_lines']);
            $("#sidebar_cart_lines").find("#sidebar_short_cart_summary").html(data['website_sale.short_cart_summary_sidebar']);
        }
    };

    return utils;
});