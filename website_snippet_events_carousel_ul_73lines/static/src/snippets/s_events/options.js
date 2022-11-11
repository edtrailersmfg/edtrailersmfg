odoo.define('website_snippet_events_carousel_ul_73lines.s_dynamic_snippet_event_options', function (require) {
'use strict';

const options = require('web_editor.snippets.options');
const DynamicBaseProductsSnippetOptions = require('website_carousel_base_ul_73lines.dynamic_product_snippet_options');
var wUtils = require('website.utils');


const DynamicSnippetEventOptions = DynamicBaseProductsSnippetOptions.extend({
 events: _.extend({}, options.Class.prototype.events || {}, {
            'click [data-selector="custom_event_filter"]': '_onClickEventFilterButton',
}),
    //--------------------------------------------------------------------------
    // Options
    //--------------------------------------------------------------------------

    /**
     * @see this.selectClass for parameters
     */
    init: function () {
        this._super.apply(this, arguments);
        this.renderedBlogs = {};
    },
    _onClickEventFilterButton: function(e){
        var titleText = this.$el.find('[data-name="event_carousel_opt"]').find('we-toggler').text().trim();
        if(this.$target.find('.event_filter_title').length != 0){
            this.$target.find('.event_filter_title').text(titleText);
        }else{
            this.$target.prepend('<div class="container mb16"><div class="headline"><h2 class="event_filter_title">' + titleText + '</h2><hr class="mt8 mb16"/></div></div>');
        }
    },
    onBuilt: function () {
        this._super.apply(this, arguments);
             this._rpc({
                 model: 'ir.model.data',
                 method: 'search_read',
                 kwargs: {
                     domain: [['module', '=', 'website_snippet_events_carousel_ul_73lines'], ['model', '=', 'website.snippet.filter']],
                        fields: ['id', 'res_id','model','module'],
                 }
             }).then((data) => {
                 //this.$target.get(0).dataset.filterId = data[0].res_id;
             });
    },
    _computeWidgetVisibility: function (widgetName, params) {
        if (widgetName === 'filter_opt' || widgetName === 'blog_category_opt' || widgetName === 'brand_category_opt' || widgetName === 'product_category_opt' || widgetName === 'client_category_opt' || widgetName === 'product_category_carousel_opt') {
            return false;
        }
        return this._super.apply(this, arguments);
    },

    _fetchCategory: function () {
        var object_name = this.$target.get(0).dataset.object_name;
        return this._rpc({
            model: 'website.snippet.filter',
            method: 'search_read',
            kwargs: {
                domain: [['filter_id.model_id', '=', object_name]],
                fields: ['name','id'],
            }
        });

    },
    _renderCustomXML: function (uiFragment) {
        return Promise.all([this._super.apply(this, arguments), this._renderCategorySelector(uiFragment)]);
    },
    _renderCategorySelector: async function (uiFragment) {
        const renderedBlogs = await this._fetchCategory();
        for (let index in renderedBlogs) {
            this.renderedBlogs[renderedBlogs[index].id] = renderedBlogs[index];
        }
        const blogCategoriesEl = uiFragment.querySelector('[data-name="event_carousel_opt"]');
        return this._renderSelectCustomUserValueWidgetButtons(blogCategoriesEl, this.renderedBlogs,'custom_event_filter');
    },
    _renderSelectCustomUserValueWidgetButtons: async function (selectUserValueWidgetElement, data, selector) {
        for (let id in data) {
            const button = document.createElement('we-button');
            button.dataset.selectDataAttribute = id;
            button.dataset.selector = selector;
            button.innerHTML = data[id].name;
            selectUserValueWidgetElement.appendChild(button);
        }
    },
});
options.registry.dynamic_snippet_event = DynamicSnippetEventOptions;

return DynamicSnippetEventOptions;

});
