odoo.define('website_carousel_base_ul_73lines.dynamic_product_snippet', function (require) {
'use strict';

    const config = require('web.config');
    const core = require('web.core');
    const publicWidget = require('web.public.widget');
    const DynamicSnippetCarousel = require('website.s_dynamic_snippet_carousel');
    var _t = core._t;
    const {Markup} = require('web.utils');
    var Dialog = require('web.Dialog');
    var ajax = require('web.ajax');

    const DynamicBaseProductsSnippet = DynamicSnippetCarousel.extend({
        read_events: {
            'click .o_quick_view_popup': '_onClickProductQuickView',
        },
        async _fetchData() {
            if (this._isConfigComplete()) {
                var classList = this.$target.get(0).classList;
                var tempClass = this.$el.get(0).dataset.templateKey
                for(var i=0; i < classList.length; i++){
                    if(classList[i].includes('dynamic_filter_template_')){
                        this.$target.removeClass(classList[i]);
                        this.$target.addClass(tempClass.split('.')[1])
                    }else{
                        this.$target.addClass(tempClass.split('.')[1])
                    }
                }
                const filterFragments = await this._rpc({
                    'route': '/website/custom/snippet/products',
                    'params': {
                        'filter_id': parseInt(this.$el.get(0).dataset.filterId),
                        'template_key': this.$el.get(0).dataset.templateKey,
                        'limit': parseInt(this.$el.get(0).dataset.numberOfRecords),
                        'search_domain': this._getSearchDomain()
                    },
                });
                if(filterFragments){
                    this.data = filterFragments.map(Markup);
                } else {
                    return new Promise((resolve) => {
                        this.data = [];
                        resolve();
                    });
                }

            } else {
                return new Promise((resolve) => {
                    this.data = [];
                    resolve();
                });
            }
        },
        _isConfigComplete: function() {
            return this._super.apply(this, arguments) && this.$el.get(0).dataset.filterId !== undefined;
        },
        _getQWebRenderOptions: function () {
            return {
                chunkSize: parseInt(
                    config.device.isMobile
                        ? this.$target[0].dataset.numberOfElementsSmallDevices
                        : this.$target[0].dataset.numberOfElements
                ),
                rowSize: this.$target[0].dataset.rowSize,
                data: this.data,
                uniqueId: this.uniqueId
            };
        },
    });

    return DynamicBaseProductsSnippet;
});