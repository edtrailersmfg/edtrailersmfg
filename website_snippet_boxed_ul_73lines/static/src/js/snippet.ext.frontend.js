odoo.define('website_snippet_boxed_ul_73lines.ext.frontend', function (require) {
    'use strict';

    var s_animation = require('website.content.snippets.animation');
    var session = require('web.session');

    s_animation.registry.s_media_block.include({
        selector: ".s_media_block",

        create_youtube_video: function () {
            return this.YTPlayer_video.apply(this, arguments);
        },

        stop_video: function () {
            this._super.apply(this, arguments);
            this.$target.find('.yt_video_container').remove();
        },
    });
});
