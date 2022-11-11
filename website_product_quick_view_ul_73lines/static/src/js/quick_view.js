odoo.define('website_product_quick_view_ul_73lines.quick_view', require => {
    'use strict';

    const core = require('web.core');
    const publicWidget = require('web.public.widget');
    const Dialog = require('web.Dialog');
    var ajax = require('web.ajax');
    const _t = core._t;
    require('website_sale.website_sale');

    publicWidget.registry.WebsiteSale.include({
        _handleAdd: function ($form) {
            return this._super.apply(this, arguments).then(() => {
                console.log('after add to cart',$('.modal-dialog'), $('.modal-dialog').data())
                if($('.modal-dialog').length && $('.modal-dialog').data('dialog_data')){
                    $('.modal-dialog').data('dialog_data').close()
                }
            });
        },
    });

    publicWidget.registry.shopPageQuickView = publicWidget.Widget.extend({
        selector: '.oe_website_sale',
        events: {
            'click .shop-page-quick-view': '_onClick'
        },
        _onClick: function(ev){
            var self = this;
            var dialog = new Dialog(this, {
                title: _t("Quick View"),
                renderFooter: false,
                size: 'large',
            }).open();
            dialog.opened().then(function () {
                dialog.$modal.find('.modal-dialog').addClass('modal-dialog-centered ul_quick_modal');
                dialog.$modal.find('.modal-dialog').data('dialog_data', dialog);
                var productID = $(ev.currentTarget).data('product_id');
                ajax.jsonRpc('/shop/quick/view', 'call', {
                'options': {
                    productID: productID,
                }
                }).then(data => {
                    console.log(data,'.atatat',dialog)
                    dialog.$el.append(data)
                    self.trigger_up('widgets_start_request', {
                        $target: dialog.$el,
                    });
                })
            });
        },
    });
});