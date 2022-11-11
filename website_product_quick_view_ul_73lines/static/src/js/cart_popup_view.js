odoo.define('website_product_quick_view_ul_73lines.cart_popup_view', require => {
    'use strict';

    const core = require('web.core');
    const publicWidget = require('web.public.widget');
    const Dialog = require('web.Dialog');
    var ajax = require('web.ajax');
    const _t = core._t;
    require('website_sale.website_sale');

    publicWidget.registry.shopPageCartView = publicWidget.Widget.extend({
        selector: '.oe_website_sale',
        events: {
            'click .shop-page-cart-view': '_onClick'
        },
        _onClick: function(ev){
            var self = this;
            var dialog = new Dialog(this, {
                title: _t("Add to Cart"),
                renderFooter: false,
                size: 'medium',
            }).open();
            dialog.opened().then(function () {
                dialog.$modal.find('.modal-dialog').addClass('modal-dialog-centered ul_cart_modal');
                dialog.$modal.find('.modal-dialog').data('dialog_data', dialog);
                var productCartID = $(ev.currentTarget).data('product_id');
                ajax.jsonRpc('/shop/cart/view', 'call', {
                'options': {
                    productCartID: productCartID,
                }
                }).then(data => {
                    dialog.$el.append(data)
                    self.trigger_up('widgets_start_request', {
                        $target: dialog.$el,
                    });
                })
            });
        },
    });
});