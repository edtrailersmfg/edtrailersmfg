odoo.define('website_snippet_boxed_ul_73lines.s_counter_text', function (require) {
    'use strict';
    var ajax = require('web.ajax');
    var core = require('web.core');
    var s_options = require('web_editor.snippets.options');

    var QWeb = core.qweb;

    ajax.loadXML('/website_snippet_boxed_ul_73lines/static/src/xml/s_state_counter_setting.xml', QWeb);

    s_options.registry.js_state_section = s_options.Class.extend({
        events: {
            "click .state_opt": "state_opt",
        },
        start: function () {
            var self = this;
        },
        state_opt: function (type, value, $li) {
            var self = this;
            var event;

            event = self.$target.find('.odometer')[0];
            self.$modal = $(QWeb.render("s_counter_text"));
            self.$modal.appendTo('body').modal();

            $(".state_text").click(function () {
                event = self.$target.find('.odometer')[0];
            });
            $(".number_st").on('change', function () {
                var text_box_val = $(this).val();
                event.setAttribute("data-number", text_box_val);
            });
            $(".duration_st").on('change', function () {
                var text_box_val = $(this).val();
                event.setAttribute("data-duration", text_box_val);
            });
        },
    });
});
