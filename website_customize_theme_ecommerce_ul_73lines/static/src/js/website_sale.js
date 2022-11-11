odoo.define('website_customize_theme_ecommerce_ul_73lines.website_sale', require => {
    'use strict';

    const core = require('web.core');
    const publicWidget = require('web.public.widget');
    const Dialog = require('web.Dialog');
    var ajax = require('web.ajax');
    const _t = core._t;
    require('website_sale.website_sale');

    publicWidget.registry.WebsiteSale.include({
        events: _.extend({}, publicWidget.registry.WebsiteSale.prototype.events, {
            'change ul.on_change_product_attribute input': '_onShopPageAttributeChange',
            //'mouseover ul.on_change_product_attribute input': '_onShopPageAttributeChange',
        }),

        _onShopPageAttributeChange: function(e){
            var productId = $(e.currentTarget).data('productId');
            var attr = $(e.currentTarget).val();
            var $component = $(e.currentTarget).closest('.js_attributes');
            $component.find('label').removeClass('active');
            $(e.currentTarget).closest('label').addClass('active');
            return ajax.jsonRpc('/shop/onchange/variant', 'call', {
                product_id: productId,
                attribute_id: attr.split('-')[0],
                product_attribute_value_id: attr.split('-')[1],
            }).then((res) => {
                $(e.currentTarget).closest('form').find('img').attr('src', res);
            });
        },
    });
});