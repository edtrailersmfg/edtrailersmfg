odoo.define('website_icon_fonts_ul_73lines.icon_option', function(require){
    'use strict';
    const options = require('web_editor.snippets.options');
    var widgets = require('website_icon_fonts_ul_73lines.widgets');

    options.registry.replace_icons_73lines = options.SnippetOptionWidget.extend({
        events: {
            'click': '_onClick',
        },
        start: function(){
            this._super.apply(this, arguments);
        },

        _onClick: function(){
            new widgets.FontIconDialog(this, this.options, this.$el, this.$target).open();
        },
    });

});