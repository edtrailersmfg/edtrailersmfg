odoo.define('website.theme_options', function (require) {
'use strict';

    var website_theme = require('website.theme');

    website_theme.include({
        _onChange: function (ev) {
            var self = this;

            // Checkout the option that changed
            var $option = $(ev.currentTarget);
            var $options = $option;
            var checked = $option.is(':checked');

            // If it was enabled, enable/disable the related input (see data-enable,
            // data-disable) and retain the ones that actually changed
            if (checked) {
                var $inputs;
                // Input to enable
                $inputs = this._getInputs($option.data('enable'));
                $options = $options.add($inputs.filter(':not(:checked)'));
                $inputs.prop('checked', true);
                // Input to disable
                $inputs = this._getInputs($option.data('disable'));
                $options = $options.add($inputs.filter(':checked'));
                $inputs.prop('checked', false);
            }
            var optionNames = _.uniq(_.map($options, function (option) {
                return option.name;
            }));
            $options = this.$inputs.filter(function (i, input) {
                return _.contains(optionNames, input.name);
            });

            // Look at all options to see if they are enabled or disabled
            var $enable = $options.filter('[data-xmlid]:checked');
            var $disable = $options.filter('[data-xmlid]:not(:checked)');

            this._setActive();

            // Update the style according to the whole set of options
            self._processChange($options).then(function () {
                self._updateStyle(
                    self._getXMLIDs($enable),
                    self._getXMLIDs($disable),
                    $option.data('reload')
                );
            });
        },
    })
});
