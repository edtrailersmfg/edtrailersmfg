odoo.define('website_carousel_base_ul_73lines.dynamic_product_snippet_options', function (require) {
    'use strict';

    const options = require('web_editor.snippets.options');
    const s_dynamic_snippet_carousel_options = require('website.s_dynamic_snippet_carousel_options');
    const s_dynamic_snippet_options = require('website.s_dynamic_snippet_options');
    var wUtils = require('website.utils');

    s_dynamic_snippet_options.include({
        _computeWidgetVisibility: function (widgetName, params) {
            if(!this.custom_snippet_carousel){
                if (widgetName === 'product_category_opt' || widgetName === 'blog_category_opt' || widgetName === 'brand_category_opt' || widgetName === 'product_category_carousel_opt' || widgetName === 'client_category_opt') {
                    return false;
                }
            } else {
                if (widgetName === 'filter_opt'){
                    return false;
                }
            }
            return this._super.apply(this, arguments);
        },
    });

    const DynamicProductsSnippetOptions = s_dynamic_snippet_carousel_options.extend({
        init: function(){
            this._super.apply(this, arguments);
            this.custom_snippet_carousel = true;
        },

        _refreshPublicWidgets: function () {
            var self = this;

            return this._super.apply(this, arguments).then(() => {
                const template = this._getCurrentTemplate();
                console.log(self.$target.get(0).dataset);
                if(this.$target.get(0).dataset['disableOptions']){
                 _.each(this.$target.get(0).dataset['disableOptions'].split(','), function(val){
                    console.log(val,'VAL')
                    self.$el.find('[data-attribute-name="'+ val +'"]').addClass('d-none');
                 });
             }
                this.$target.find('.missing_option_warning').toggleClass(
                    'd-none',
                    !!template
                );
            });
        },

        _renderDynamicFilterTemplatesSelector: async function (uiFragment) {
            const dynamicFilterTemplates = await this._fetchDynamicFilterTemplates();
            this.dynamicFilterTemplates = {};
            var snippet_identifier = this.$target.get(0).dataset.snippet_identifier;
            for (let index in dynamicFilterTemplates) {
                if(dynamicFilterTemplates[index].name.includes(snippet_identifier)){
                    this.dynamicFilterTemplates[dynamicFilterTemplates[index].key] = dynamicFilterTemplates[index];
                }
            }
            if (dynamicFilterTemplates.length > 0) {
                var snippet_identifier = this.$target.get(0).dataset.snippet_identifier;
                for (let index in dynamicFilterTemplates) {
                    if(dynamicFilterTemplates[index].name.includes(snippet_identifier)){
                        this.dynamicFilterTemplates[dynamicFilterTemplates[index].key] = dynamicFilterTemplates[index];
                    }
                }
                setTimeout(() => {
                    this._refreshPublicWidgets();
                });
            } else {
                this._refreshPublicWidgets();
            }
            const templatesSelectorEl = uiFragment.querySelector('[data-name="template_opt"]');
            return this._renderSelectUserValueWidgetButtons(templatesSelectorEl, this.dynamicFilterTemplates);
        },

        _fetchDynamicFilters: function () {
            return this._rpc({route: '/website/snippet/options_filters', params: {
                model_name: this.$target.get(0).dataset['object_name'],
                search_domain: this.contextualFilterDomain,
            }});
        },

        _fetchDynamicFilterTemplates: function () {
            const filter = this.$target.get(0).dataset['object_name'];
            return filter ? this._rpc({route: '/website/custom/snippet/filter_templates', params: {
                filter_name: filter.replaceAll('.', '_'),
            }}) : [];
        },

        _renderSelectUserValueWidgetButtons: async function (selectUserValueWidgetElement, data) {
            if(this.custom_snippet_carousel && selectUserValueWidgetElement.getAttribute('data-name') == 'filter_opt'){
                return false;
            } else {
                this._super.apply(this, arguments);
            }
        },

        async updateUIVisibility() {
            const groupingMessage = this.el.querySelector('.o_grouping_message');
            if(groupingMessage){
                await this._super(...arguments);
            }
        },

        _setOptionsDefaultValues: function () {
            this._super.apply(this, arguments);
            this._setOptionValue('rowSize', 1);
            this._setOptionValue('numberOfElements', this.$target.get(0).dataset['numberOfElements']);
        },
    });

    return DynamicProductsSnippetOptions;
});