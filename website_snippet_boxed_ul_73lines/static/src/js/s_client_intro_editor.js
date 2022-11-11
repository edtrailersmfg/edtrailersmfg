odoo.define('snippet_theme.s_client_intro',function(require) {
    'use strict';

    var s_options = require('web_editor.snippets.options');

    s_options.registry.s_client_intro = s_options.Class.extend({
        start : function() {
            var self = this;
            self.add_btn_edit_slide();
        },

        add_btn_edit_slide : function() {
            var self = this;
            self.$overlay
                    .find(".oe_options")
                    .after(
                            '<a href="#" class="btn btn-default btn-sm btn-showSlide" title="Lock slide" style="width: auto; padding: 0 5px;"><i class="fa fa-toggle-off"></i>  Edit Slide</a> ');
            self.$overlay.on('click', '.btn-showSlide',
                    _.bind(this.toggle_slide, this));
        },

        toggle_slide : function() {
            var a = this.$overlay
                    .find(".btn-showSlide"), i = a
                    .find("i"), t = this.$target, s = t
                    .find(".slide");
            if (!t.hasClass("showSlide")) {
                t.addClass("showSlide");
                i.addClass("fa-toggle-on").removeClass(
                        "fa-toggle-off");
                i.css("color", "#FFF");
                s.addClass("visible");
            } else {
                t.removeClass("showSlide");
                i.removeClass("fa-toggle-on").addClass(
                        "fa-toggle-off");
                i.css("color", "");
                s.removeClass("visible");
            }
        },
        clean_for_save : function() {
            this.$target.removeClass("showSlide").find(
                    ".slide").removeClass("visible");
        },
    });
});
