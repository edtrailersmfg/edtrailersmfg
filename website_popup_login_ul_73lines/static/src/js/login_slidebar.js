odoo.define('website_popup_login_ul_73lines.login_slidebar.js', function (require) {
'use strict';

const { _t } = require('web.core');
const publicWidget = require('web.public.widget');

publicWidget.registry.SidebarLogin = publicWidget.Widget.extend({
    selector: '#wrapwrap',
    init: function () {
        this._super.apply(this, arguments);
        this.$backdrop = $('<div class="modal-backdrop filter-sideabr-back show d-block"/>');
        $('.my_login_sidebar').on('click', this._onClickDrawerToggleLogin.bind(this));
    },
    _onClickDrawerToggleLogin: function (ev) {
        ev.preventDefault();
        if (this.$('#website_sidebar_login_ul_73lines').hasClass('open')) {
            this.$('#website_sidebar_login_ul_73lines').removeClass('open');
            $('body').removeClass('modal-open');
            $('header').removeClass('sidebar-login-model');
            $('#wrapwrap').css('z-index', 0);
            this.$backdrop.remove();
        } else {
            this.$backdrop.appendTo('body');
            this.$('#website_sidebar_login_ul_73lines').addClass('open');
            this.$backdrop.on('click', this._onClickDrawerToggleLogin.bind(this));
            $('body').addClass('modal-open');
            $('header').addClass('sidebar-login-model');
            $('#wrapwrap').css('z-index', 'unset');
        }
        this.$('.categories-filter-drawer-item').toggleClass('show d-none');
    },
});

});
