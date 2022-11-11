//odoo.define('website_snippet_boxed_ul_73lines.ext.editor', function (require) {
//    'use strict';
//
//    var ajax = require('web.ajax');
//    var core = require('web.core');
//
//    ajax.loadXML('/website_snippet_boxed_ul_73lines/static/src/xml/s_media_block_modal_ext.xml', core.qweb);
//});

odoo.define('website_snippet_boxed_ul_73lines.ext.editor', function (require) {
    'use strict';

    require('web.dom_ready');
    var ajax = require('web.ajax');
    var core = require('web.core');
    const weSnippetEditor = require('web_editor.snippet.editor');

    ajax.loadXML('/website_snippet_boxed_ul_73lines/static/src/xml/s_media_block_modal_ext.xml', core.qweb);

    weSnippetEditor.SnippetsMenu.include({
        async start() {
            await this._super(...arguments);
            if(this.$body.find('[data-snippet="s_presentation_page"]').length){
                this.$body.find('#wrapwrap').css({'overflow': 'auto'})
            }
        }
    });

});

