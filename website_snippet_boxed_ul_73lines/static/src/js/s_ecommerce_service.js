odoo.define('s.ecommerce.service.73lines.editor', function(require) {
    'use strict';

    var options = require('web_editor.snippets.options');

    options.registry.js_s_ecommerce_service = options.Class.extend({

        view_type : function(type, value) {
            var self = this;
            if (value == 'h') {
                console.info(self.$target.find(".ttcontent_inner"))
//                self.$target.find(".ttcontent_inner").addClass('col-md-3');
                self.$target.find(".v-12").addClass('col-md-3');
                self.$target.find(".v-12").removeClass('col-md-12');
                self.$target.find(".ttcontent_inner").addClass('col-md-12');
                self.$target.find(".ttcontent_inner").css({
                    //'border' : '1px solid #f0f0f0',
                    'padding' : '10px'
                });
                self.$target.find(".block_content > div").css({
                    //'border-bottom' : '1px solid #f0f0f0',
                    //'float' : 'unset',
                    //'padding' : '0px'
                });
            }
            if (value == 'v') {
                self.$target.find(".v-12").addClass('col-md-12');
                self.$target.find(".ttcontent_inner").removeClass('col-md-3');
                self.$target.find(".block_content > div").css({
                    'border-bottom' : '1px solid #f0f0f0',
                    'float' : 'left',
                    'padding' : '20px 0'
                });
                self.$target.find(".ttcontent_inner").css({
                    'border' : '0px',
                    'padding' : '0px'
                });
            }
        },

    });
});
