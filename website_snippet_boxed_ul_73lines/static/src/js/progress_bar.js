odoo.define('website_snippet_boxed_ul_73lines.s_progress_bar', function (require) {
    'use strict';
    var ajax = require('web.ajax');
    var core = require('web.core');
    var s_options = require('web_editor.snippets.options');

    var QWeb = core.qweb;
    ajax.loadXML('/website_snippet_boxed_ul_73lines/static/src/xml/progress_bar.xml', QWeb);

    s_options.registry.js_progress_bar = s_options.Class.extend({
        events: {
            "click .progress_bar": "progress_opt",
        },
        start: function(){
            var self = this;
        },
        progress_opt: function (type, value, $li) {
            var self = this;
            self.$modal = $(QWeb.render("website_snippet_boxed_ul_73lines.progress_bar"));
            self.$modal.appendTo('body').modal();

            // var field_names = ['src'];
            var event = this.$target.find('.progress_bar_1');
            var event_pr = this.$target.find('.progress_content');
            var change_color;

            $('.color_active').change(function() {
                change_color=$(this).val();
                event_pr.attr('data-active', change_color);
            });
            $('.color_nonactive').change(function() {
                change_color=$(this).val();
                event_pr.attr('data-nonactive', change_color);
            });
            $(".progress1").on('change',function(){
                var text_box_val = $(this).val();
                if ($(text_box_val.length) != 0){
                    event_pr.attr('data-percentage', text_box_val);
                    event.html(text_box_val);
                }
            });
        },
    });
});
