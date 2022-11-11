odoo.define('website_customize_theme_ecommerce_ul_73lines.wishlist123', function (require) {
"use strict";

var publicWidget = require('web.public.widget');
var wSaleUtils = require('website_sale.utils');
var VariantMixin = require('sale.VariantMixin');

publicWidget.registry.ProductWishlist.include({

    _removeWish: function (e, deferred_redirect) {
        if($('.ul-wishlist-section').length == 0){
            var tr = $(e.currentTarget).parents('tr');
            $(tr).hide();
        }else{
            var tr = $(e.currentTarget).parent().parent().parent().parent().parent().find('.wish_list_config');
            if(!$('.ul-wishlist-section').find('#b2b_wish').is(':checked') || $(e.currentTarget).hasClass('o_wish_rm')){
            $(tr).parent().parent().hide();
            }

        }
        var wish = tr.attr('data-wish-id');
        var product = tr.attr('data-product-id');
        var self = this;
        this._rpc({
            route: '/shop/wishlist/remove/' + wish,
        }).then(function () {
            var remove_pro = self.wishlistProductIDs
            var removeIndex = remove_pro.indexOf(parseInt(product));
            remove_pro.splice(removeIndex, 1);
             self.wishlistProductIDs  = remove_pro
              self._updateWishlistView();

        });

        this.wishlistProductIDs = _.without(this.wishlistProductIDs, product);
        if (this.wishlistProductIDs.length === 0) {
            if (deferred_redirect) {
                deferred_redirect.then(function () {
                    self._redirectNoWish();
                });
            }
        }
        this._updateWishlistView();
    },

    _addOrMoveWish: function (e) {
    var self = this;
        var $navButton = $('header .o_wsale_my_cart').first();
        if($('.ul-wishlist-section').length == 0){
            var tr = $(e.currentTarget).parents('tr');
            var product = tr.data('product-id');
        }else{
            var tr = $(e.currentTarget).parent().parent().parent().parent().parent().find('.wish_list_config');
            var product = tr.attr('data-product-id');
        }

        $('.o_wsale_my_cart').removeClass('d-none');
        wSaleUtils.animateClone($navButton, tr, 25, 40);
        if ($('#b2b_wish').is(':checked')) {
            return this._addToCart(product, tr.find('add_qty').val() || 1);
        } else {
            var adding_deffered = this._addToCart(product, tr.find('add_qty').val() || 1);
            this._removeWish(e, adding_deffered);
            return adding_deffered;
        }
    },

    _addToCart: function (productID, qty) {
        const $tr = this.$(`.wish_list_config[data-product-id="${productID}"]`);
        const productTrackingInfo = $tr.data('product-tracking-info');
        if (productTrackingInfo) {
            productTrackingInfo.quantity = qty;
            $tr.trigger('add_to_cart_event', [productTrackingInfo]);
        }
        return this._rpc({
            route: "/shop/cart/update_json",
            params: {
                product_id: parseInt(productID, 10),
                add_qty: parseInt(qty, 10),
                display: false,
            },
        }).then(function (resp) {
            if (resp.warning) {
                if (! $('#data_warning').length) {
                    $('.wishlist-section').prepend('<div class="mt16 alert alert-danger alert-dismissable" role="alert" id="data_warning"></div>');
                }
                var cart_alert = $('.wishlist-section').parent().find('#data_warning');
                cart_alert.html('<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button> ' + resp.warning);
            }
            $('.my_cart_quantity').html(resp.cart_quantity || '<i class="fa fa-warning" /> ');
        });
    },

    _onClickWishRemove: function (ev) {
        this._removeWish(ev, false);
    },

    _onClickWishAdd: function (ev) {
        var self = this;
        this.$('.wishlist-section .o_wish_add').addClass('disabled');
        this._addOrMoveWish(ev).then(function () {
            self.$('.wishlist-section .o_wish_add').removeClass('disabled');

        });
    },
});

});


