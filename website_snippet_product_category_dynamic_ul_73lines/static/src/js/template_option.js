odoo.define('website_snippet_product_category_dynamic_ul_73lines.template_option', function (require) {
'use strict';

var core = require('web.core');
var wUtils = require('website.utils');
var publicWidget = require('web.public.widget');

var _t = core._t;

publicWidget.registry.js_get_block = publicWidget.Widget.extend({
    selector: '.js_get_block',
    disabledInEditableMode: false,

    /**
     * @override
     */
    start: function () {
        var self = this;
        const data = self.$target[0].dataset;
        const template = data.template;
        const object = data.object;

        var prom = new Promise(function (resolve) {
            self._rpc({
                route: '/snippet/get_template_data',
                params: {
                    template: template,
                    object: object,
                },
            }).then(function (data) {
                var $category = $(data);
                self.$target.html($category);
                resolve();
            }).guardedCatch(function () {
                if (self.editableMode) {
                    self.$target.append($('<p/>', {
                        class: 'text-danger',
                        text: _t("An error occured with category block. If the problem persists, please consider deleting it and adding a new one"),
                    }));
                }
                resolve();
            });
        });
        return Promise.all([this._super.apply(this, arguments), prom]);
    },
    /**
     * @override
     */
    destroy: function () {
        this.$target.empty();
        this._super.apply(this, arguments);
    },
});
});
