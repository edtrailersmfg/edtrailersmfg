odoo.define('website_snippet_boxed_ul_73lines.s_bar_chart', function (require) {
    'use strict';
    var ajax = require('web.ajax');
    var core = require('web.core');
    var s_options = require('web_editor.snippets.options');

    var QWeb = core.qweb;
    ajax.loadXML('/website_snippet_boxed_ul_73lines/static/src/xml/bar_chart.xml', QWeb);

    s_options.registry.js_bar_chart = s_options.Class.extend({
        events: {
            "click .bar_chart": "bar_opt",
        },
        start: function () {
            var self = this;
        },
        bar_opt: function (type, value, $li) {
            var self = this;
            self.$modal = $(QWeb.render("website_snippet_boxed_ul_73lines.bar_chart"));
            self.$modal.appendTo('body').modal();

            var event = this.$target.find('.progress');
            var event_pr = this.$target.find('.progress_content');
            var change_color;
            $('.color_active').change(
                function () {
                    change_color = $(this).val();
                    event_pr.attr('data-active', change_color);
                    var style = event_pr.attr('style');
                    if (style)
                        event_pr.attr('style', style
                            + ' background-color:'
                            + change_color + ';');
                    else
                        event_pr.attr('style',
                            ' background-color:' + change_color + ';');
                });
            $('.color_nonactive').change(
                function () {
                    change_color = $(this).val();
                    event_pr.attr('data-nonactive', change_color);
                    var style =event_pr.attr('style');
                    if (style)
                        event.attr('style', style
                            + ' background-color:'
                            + change_color + ';');
                    else
                        event.attr('style', ' background-color:'
                            + change_color + ';');
                });
            $(".progress1").on('change', function () {
                var text_box_val = (event_pr.parent().height() * $(this).val()) / 100;
                if ($(text_box_val.length) != 0) {
                    event_pr.attr('aria-valuenow', $(this).val());
                    var style = event_pr.attr('style');
                    if (style)
                        event_pr.attr('style', style
                            + ' height:'
                            + text_box_val + 'px;');
                    else
                        event_pr.attr('style',
                            ' height:' + text_box_val + 'px;');
                }
            });
        },
    });

    require('web.dom_ready');
    $(".bar_chart").appear(function () {
        var bar_chart = $(this).find('.progress-bar-striped');
        var bar_chart_height = (bar_chart.parent().height() * $(this).find('.progress-bar-striped')) / 100;
        bar_chart.css({
            'height': bar_chart_height + 'px',
            'background-color': bar_chart.attr('data-active')
        });
        $(this).find("#myBar").html(bar_chart.attr('aria-valuenow') + '%')
    });
});
