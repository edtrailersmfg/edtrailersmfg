odoo.define('website_product_misc_options_ul_73lines.filter_slidebar.js.js', function (require) {
'use strict';

const { _t } = require('web.core');
const publicWidget = require('web.public.widget');

publicWidget.registry.CategoriesDrawer = publicWidget.Widget.extend({
    selector: '.o_wsale_products_main_row',
    init: function () {
        this._super.apply(this, arguments);
        this.$backdrop = $('<div class="modal-backdrop filter-sideabr-back show d-block"/>');
        $('.categories-filter-drawer-toggle').on('click', this._onClickDrawerToggle.bind(this));
    },
    _onClickDrawerToggle: function (ev) {
        ev.preventDefault();
        if (this.$('#products_grid_before').hasClass('open')) {
            this.$('#products_grid_before').removeClass('open');
            $('body').removeClass('modal-open');
            $('#wrapwrap').css('z-index', 0);
            this.$backdrop.remove();
        } else {
            this.$backdrop.appendTo('body');
            this.$('#products_grid_before').addClass('open');
            this.$backdrop.on('click', this._onClickDrawerToggle.bind(this));
            $('body').addClass('modal-open');
            $('#wrapwrap').css('z-index', 'unset');
        }
        this.$('.categories-filter-drawer-item').toggleClass('show d-none');
    },
});

});
