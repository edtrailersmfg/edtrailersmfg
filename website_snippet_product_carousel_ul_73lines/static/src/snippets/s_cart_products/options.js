odoo.define('website_snippet_product_carousel_ul_73lines.dynamic_product_snippet_options', function (require) {
'use strict';

const options = require('web_editor.snippets.options');
const session = require('web.session');
const DynamicBaseProductsSnippetOptions = require('website_carousel_base_ul_73lines.dynamic_product_snippet_options');
var wUtils = require('website.utils');

const DynamicProductsSnippetOptions = DynamicBaseProductsSnippetOptions.extend({
    events: _.extend({}, options.Class.prototype.events || {}, {
        'click .config_button': '_onClickConfigButton',
        'click .hover_effect_btn': '_onClickHoverButton',
        'click .grid_view_btn': '_onClickGridButton',
        'click [data-name="product_category_opt"]': '_onClickProductCategoryButton',
    }),
    //--------------------------------------------------------------------------
    // Options
    //--------------------------------------------------------------------------

    /**
     * @see this.selectClass for parameters
     */
    init: function () {
        this._super.apply(this, arguments);
        this.renderedProductCategory = {};
    },
    start: function(){
        this._super.apply(this, arguments);
        var config_buttons = this.$el.find('.config_button');
        var self = this;
        this.$el.find('.config_button').each( function(index){
            var className = $(this).data('toggleClass');
            if(self.$target.hasClass(className)){
                $(this).addClass('active');
            }
        });
    },
    _onClickProductCategoryButton: function(){
        var titleText = this.$el.find('[data-name="product_category_opt"]').find('we-toggler').text().trim();
        if(this.$target.find('.product_title').length != 0){
            this.$target.find('.product_title').text(titleText);
        }else{
            this.$target.prepend('<div class="container mb16"><div class="headline"><h2 class="product_title">' + titleText + '</h2><hr class="mt8 mb16"/></div></div>');
        }
    },

    _refreshPublicWidgets: function(){
        this._super.apply(this, arguments);
        this._onClickProductCategoryButton();
    },

    onBuilt: function () {
        this._super.apply(this, arguments);
        this._rpc({
        model: 'ir.model.data',
        method: 'search_read',
        kwargs: {
         domain: [['module', '=', 'website_snippet_product_carousel_ul_73lines'], ['model', '=', 'website.snippet.filter']],
            fields: ['id', 'res_id','model','module'],
        }
        }).then((data) => {
             this.$target.addClass('oe_website_sale');
        });
    },
    _computeWidgetVisibility: function (widgetName, params) {
        if (widgetName === 'filter_opt' || widgetName === 'blog_category_opt' || widgetName === 'brand_category_opt' || widgetName === 'product_category_carousel_opt' || widgetName === 'client_category_opt' || widgetName === 'event_carousel_opt') {
            return false;
        }
        return this._super.apply(this, arguments);
    },
    _onClickConfigButton: function(e){
        var toggleClassName = $(e.currentTarget).data('toggleClass');
        this.$target.toggleClass(toggleClassName);
        $(e.currentTarget).toggleClass('active');
    },
    _onClickGridButton: function(e){
        var toggleClassName = $(e.currentTarget).data('toggleClass');
        this.$target.toggleClass(toggleClassName);
        $(e.currentTarget).toggleClass('active');
    },
    _onClickHoverButton: function(e){
        var toggleClassName = $(e.currentTarget).data('toggleClass');
        this.$target.toggleClass(toggleClassName);
        $(e.currentTarget).toggleClass('active');
    },
    _fetchProductCategory: function () {
        var object_name = this.$target.get(0).dataset.object_name;
        return this._rpc({
            model: 'website.snippet.filter',
            method: 'search_read',
            kwargs: {
                domain: [['filter_id.model_id', '=', object_name], ['website_id', '=', session.website_id]],
                fields: ['name','id'],
            }
        });
    },
    _renderCustomXML: function (uiFragment) {
        return Promise.all([this._super.apply(this, arguments), this._renderProductCategorySelector(uiFragment)]);
    },

    _renderProductCategorySelector: async function (uiFragment) {
        const renderedProductCategory = await this._fetchProductCategory();
        for (let index in renderedProductCategory) {
            this.renderedProductCategory[renderedProductCategory[index].id] = renderedProductCategory[index];
        }
        const productCategoriesEl = uiFragment.querySelector('[data-name="product_category_opt"]');
        return this._renderSelectCustomUserValueWidgetButtons(productCategoriesEl, this.renderedProductCategory,'custom_product_filter');
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
options.registry.dynamic_product_snippet = DynamicProductsSnippetOptions;
return DynamicProductsSnippetOptions;

});
