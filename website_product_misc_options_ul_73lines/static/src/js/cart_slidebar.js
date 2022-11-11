odoo.define('website_product_misc_options_ul_73lines.cart_slidebar.js', function (require) {
'use strict';

const { _t } = require('web.core');
const publicWidget = require('web.public.widget');

publicWidget.registry.CategoriesDrawerCart = publicWidget.Widget.extend({
    selector: '#wrapwrap',
    init: function () {
        this._super.apply(this, arguments);
        this.$backdropcart = $('<div class="modal-backdrop filter-sideabr-back show d-block"/>');
        $('.my_cart_sidebar').on('click', this._onClickDrawerToggleCart.bind(this));
    },
    _onClickDrawerToggleCart: function (ev) {
        ev.preventDefault();
        if (this.$('#sidebar_cart_lines').hasClass('open')) {
            this.$('#sidebar_cart_lines').removeClass('open');
            console.log('ttttt');
            $('body').removeClass('modal-open');
            $('#wrapwrap').css('z-index', 0);
            this.$backdropcart.remove();
        } else {
            this.$backdropcart.appendTo('body');
            this.$('#sidebar_cart_lines').addClass('open');
            this.$backdropcart.on('click', this._onClickDrawerToggleCart.bind(this));
            $('body').addClass('modal-open');
            $('#wrapwrap').css('z-index', 'unset');
        }
        this.$('.categories-filter-drawer-item').toggleClass('show d-none');
    },
});
});
