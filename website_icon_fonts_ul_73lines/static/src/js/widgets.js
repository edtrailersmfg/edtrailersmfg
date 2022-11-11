/*
    Part of Odoo Module Developed by 73lines
    See LICENSE file for full copyright and licensing details.
*/
odoo.define('website_icon_fonts_ul_73lines.widgets', function (require) {
    'use strict';

    var core = require('web.core');
    var ajax = require('web.ajax');
    var Dialog = require('web.Dialog');
    var Widget = require('web.Widget');
    var base = require('web_editor.base');
    var qweb = core.qweb;
    var _t = core._t;
    var currentIcon, editable, all_fa_list, all_pe_list, all_emo_list, all_ti_list;

    ajax.loadXML('/website_icon_fonts_ul_73lines/static/src/xml/editor.xml', qweb);

    Dialog = Dialog.extend({
        init: function (parent, options) {
            options = options || {};
            this._super(parent, _.extend({}, {
                buttons: [
                    {text: _t("Discard"), close: true}
                ]
            }, options));

            this.destroyAction = "cancel";

            var self = this;
            this.opened().then(function () {
                self.$('input:first').focus();
            });
            this.on("closed", this, function () {
                this.trigger(this.destroyAction, this.final_data || null);
            });
        },
        save: function () {
            this.destroyAction = "save";
            this.close();
        },
    });

//    var fn_boutton_update = eventHandler.modules.popover.button.update;
//    eventHandler.modules.popover.button.update = function ($container, oStyle) {
//        fn_boutton_update.call(this, $container, oStyle);
//        if ($(oStyle.image)[0]) {
//            currentIcon = $(oStyle.image)[0];
//        }
//    };
//
//    var fn_attach = eventHandler.attach;
//    eventHandler.attach = function (oLayoutInfo, options) {
//        fn_attach.call(this, oLayoutInfo, options);
//        editable = oLayoutInfo.editor();
//    };

// *** Common Dialog That Include All Fonts Tabs ***
    var FontIconDialog = Dialog.extend({
        template: 'icon_fonts.dialog.all-fonts',
        init: function (parent, options, $editable, media) {
            this._super(parent, _.extend({}, {
                title: _t("Select Icons"),
            }, options));
            this.options = options || {};
            if (this.options.wysiwyg.odooEditor.editable) {
                this.$editable = this.options.wysiwyg.odooEditor.editable;
            }
            this.media = media;
        },
        start: function () {
            var self = this;
            this.$modal.addClass('font-icons-dialog');
            this.$modal.find('.modal-dialog').addClass('o_select_font_icons_dialog');
            this.faDialog = new faDialog(this, this.media, this.options);
            this.faDialog.appendTo(this.$("#editor-fa-icons"));

            this.peDialog = new peDialog(this, this.media, this.options);
            this.peDialog.appendTo(this.$("#editor-pe-icons"));

            this.emoDialog = new emoDialog(this, this.media, this.options);
            this.emoDialog.appendTo(this.$("#editor-emo-icons"));

            this.tiDialog = new tiDialog(this, this.media, this.options);
            this.tiDialog.appendTo(this.$("#editor-ti-icons"));

            this.active = this.faDialog;

            this.$('a[data-toggle="tab"]').on('shown.bs.tab', function (event) {
                if ($(event.target).is('[href="#editor-fa-icons"]')) {
                    self.active = self.faDialog;
                    self.$('li.search, li.previous, li.next').removeClass("hidden");
                } else if ($(event.target).is('[href="#editor-pe-icons"]')) {
                    self.active = self.peDialog;
                    self.$('li.search, li.previous, li.next').removeClass("hidden");
                } else if ($(event.target).is('[href="#editor-emo-icons"]')) {
                    self.active = self.emoDialog;
                    self.$('li.search, li.previous, li.next').removeClass("hidden");
                } else if ($(event.target).is('[href="#editor-ti-icons"]')) {
                    self.active = self.tiDialog;
                    self.$('li.search, li.previous, li.next').removeClass("hidden");
                }
            });
            return this._super.apply(this, arguments);
        },
    });

    var cacheCssSelectors = {};
    var getCssSelectors = function (filter) {
        var css = [];
        if (cacheCssSelectors[filter]) {
            return cacheCssSelectors[filter];
        }
        var sheets = document.styleSheets;
        for (var i = 0; i < sheets.length; i++) {
            var rules;
            if (sheets[i].rules) {
                rules = sheets[i].rules;
            } else {
                //try...catch because Firefox not able to enumerate document.styleSheets[].cssRules[] for cross-domain stylesheets.
                try {
                    rules = sheets[i].cssRules;
                } catch (e) {
                    console.warn("Can't read the css rules of: " + sheets[i].href, e);
                    continue;
                }
            }
            if (rules) {
                for (var r = 0; r < rules.length; r++) {
                    var selectorText = rules[r].selectorText;
                    if (selectorText) {
                        selectorText = selectorText.split(/\s*,\s*/);
                        var data = null;
                        for (var s = 0; s < selectorText.length; s++) {
                            var match = selectorText[s].match(filter);
                            if (match) {
                                var clean = match[1].slice(1).replace(/::?before$/, '');
                                if (!data) {
                                    data = [match[1], rules[r].cssText.replace(/(^.*\{\s*)|(\s*\}\s*$)/g, ''), clean, [clean]];
                                } else {
                                    data[3].push(clean);
                                }
                            }
                        }
                        if (data) {
                            css.push(data);
                        }
                    }
                }
            }
        }
        return cacheCssSelectors[filter] = css;
    };

// ***************************************************************************
// Font Awesome Icons -- http://fontawesome.io/icons/
// ***************************************************************************
// *****************************fa***Start***fa*******************************

    var faIcons = [{'base': 'fa', 'parser': /(?=^|\s)(\.fa-[0-9a-z_-]+::?before)/i}];

    var computeFonts_fa = _.once(function () {
        _.each(faIcons, function (data) {
            data.cssData = getCssSelectors(data.parser);
            data.alias = [];
            data.icons = _.map(data.cssData, function (css) {
                data.alias.push.apply(data.alias, css[3]);
                return css[2];
            });
        });
    });

    var faDialog = Widget.extend({
        template: 'icon_fonts.dialog.fa-icons',
        events: _.extend({}, Dialog.prototype.events, {
            'click .all-font-icons-icon': function (e) {
                e.preventDefault();
                e.stopPropagation();
                $(".all-font-icons-icon").removeClass("selected-font-icon");
                $(e.target).addClass("selected-font-icon");
            },
            'dblclick .all-font-icons-icon': function () {
                this.save();
            },
            'keydown.dismiss.bs.modal': function () {
            },
        }),

        init: function (parent, media, options) {
            this._super.apply(this, arguments);
            this.parent = parent;
            this.options = options;
            this.media = media[0];
            if (editable) {
                this.$editable = editable;
            }
            computeFonts_fa();
        },

        start: function () {
            return this._super.apply(this, arguments);
        },

        save: function () {
            var self = this;
            var style = this.media.attributes.style ? this.media.attributes.style.value : '';
            var classes = (this.media.className || "").split(/\s+/);
            var classes1 = (this.$el.find('span.selected-font-icon')[0].className || "").split(/\s+/);
            var new_classes = _.without(classes1, 'all-font-icons-icon', 'selected-font-icon')
            var ignore_classes_fa = _.intersection(all_fa_list, classes);
            var ignore_classes_pe = _.intersection(all_pe_list, classes);
            var ignore_classes_emo = _.intersection(all_emo_list, classes);
            var ignore_classes_ti = _.intersection(all_ti_list, classes);
            var ignore_classes = _.union(ignore_classes_fa, ignore_classes_pe, ignore_classes_emo, ignore_classes_ti);
            ignore_classes.push('fa');
            var old_classes = _.difference(classes, ignore_classes);
            var final_classes = _.union(old_classes, new_classes);
            $(this.media).attr("class", _.compact(final_classes).join(' ')).attr("style", style);
            this.options.wysiwyg.odooEditor.historyStep();
            $('.font-icons-dialog').modal('toggle');
        },

        renderElement: function () { // extract list of font (like awesome) from the cheatsheet.
            this.iconsFaParser = faIcons;
            this.icons_fa = _.flatten(_.map(faIcons, function (data) {
                return data.icons;
            }));
            all_fa_list = this.icons_fa;
            this._super.apply(this, arguments);
        },

        clear: function () {
            this.media.className = this.media.className.replace(/(^|\s)(fa(\s|$)|fa-[^\s]*)/g, ' ');
        },

    });

// *******************************fa***End***fa*******************************


// ***************************************************************************
// Stroke Icons -- http://themes-pixeden.com/font-demos/7-stroke/
// ***************************************************************************
// *****************************pe***Start***pe*******************************

    var peIcons = [{'base': '', 'parser': /(?=^|\s)(\.pe-7s-[0-9a-z_-]+::?before)/i}];

    var computeFonts_pe = _.once(function () {
        _.each(peIcons, function (data) {
            data.cssData = getCssSelectors(data.parser);
            data.alias = [];
            data.icons = _.map(data.cssData, function (css) {
                data.alias.push.apply(data.alias, css[3]);
                return css[2];
            });
        });
    });

    var peDialog = Widget.extend({
        template: 'icon_fonts.dialog.pe-icons',
        events: _.extend({}, Dialog.prototype.events, {
            'click .all-font-icons-icon': function (e) {
                e.preventDefault();
                e.stopPropagation();
                $(".all-font-icons-icon").removeClass("selected-font-icon");
                $(e.target).addClass("selected-font-icon");
            },
            'dblclick .all-font-icons-icon': function () {
                this.save();
            },
            'keydown.dismiss.bs.modal': function () {
            },
        }),

        init: function (parent, media, options) {
            this._super.apply(this, arguments);
            this.parent = parent;
            this.media = media[0];
            this.options = options;
            if (editable) {
                this.$editable = editable;
            }
            computeFonts_pe();
        },

        start: function () {
            return this._super.apply(this, arguments);
        },

        save: function () {
            var self = this;
            var style = this.media.attributes.style ? this.media.attributes.style.value : '';
            var classes = (this.media.className || "").split(/\s+/);
            var classes1 = (this.$el.find('span.selected-font-icon')[0].className || "").split(/\s+/);
            var new_classes = _.without(classes1, 'all-font-icons-icon', 'selected-font-icon')
            var ignore_classes_fa = _.intersection(all_fa_list, classes);
            var ignore_classes_pe = _.intersection(all_pe_list, classes);
            var ignore_classes_emo = _.intersection(all_emo_list, classes);
            var ignore_classes_ti = _.intersection(all_ti_list, classes);
            var ignore_classes = _.union(ignore_classes_fa, ignore_classes_pe, ignore_classes_emo, ignore_classes_ti);
            var old_classes = _.difference(classes, ignore_classes);
            var final_classes = _.union(old_classes, new_classes);
            final_classes.push('fa-500px');
            $(this.media).attr("class", _.compact(final_classes).join(' ')).attr("style", style);
            this.options.wysiwyg.odooEditor.historyStep();
            $('.font-icons-dialog').modal('toggle');
        },

        renderElement: function () { // extract list of font (like awesome) from the cheatsheet.
            this.iconsPeParser = peIcons;
            this.icons_pe = _.flatten(_.map(peIcons, function (data) {
                return data.icons;
            }));
            all_pe_list = this.icons_pe;
            this._super.apply(this, arguments);
        },

        clear: function () {
            this.media.className = this.media.className.replace(/(^|\s)(pe-7s-[^\s]*)/g, ' ');
        },

    });

// *******************************pe***End***pe*******************************


// ***************************************************************************
// Fontelico Icons -- https://github.com/fontello/fontelico.font/
// ***************************************************************************
// ****************************emo***Start***emo******************************

    var emoIcons = [{'base': '', 'parser': /(?=^|\s)(\.icon-[0-9a-z_-]+::?before)/i}];

    var computeFonts_emo = _.once(function () {
        _.each(emoIcons, function (data) {
            data.cssData = getCssSelectors(data.parser);
            data.alias = [];
            data.icons = _.map(data.cssData, function (css) {
                data.alias.push.apply(data.alias, css[3]);
                return css[2];
            });
        });
    });

    var emoDialog = Widget.extend({
        template: 'icon_fonts.dialog.emo-icons',
        events: _.extend({}, Dialog.prototype.events, {
            'click .all-font-icons-icon': function (e) {
                e.preventDefault();
                e.stopPropagation();
                $(".all-font-icons-icon").removeClass("selected-font-icon");
                $(e.target).addClass("selected-font-icon");
            },
            'dblclick .all-font-icons-icon': function () {
                this.save();
            },
            'keydown.dismiss.bs.modal': function () {
            },
        }),

        init: function (parent, media, options) {
            this._super.apply(this, arguments);
            this.parent = parent;
            this.media = media[0];
            this.options = options;
            if (editable) {
                this.$editable = editable;
            }
            computeFonts_emo();
        },

        start: function () {
            return this._super.apply(this, arguments);
        },

        save: function () {
            var self = this;
            var style = this.media.attributes.style ? this.media.attributes.style.value : '';
            var classes = (this.media.className || "").split(/\s+/);
            var classes1 = (this.$el.find('span.selected-font-icon')[0].className || "").split(/\s+/);
            var new_classes = _.without(classes1, 'all-font-icons-icon', 'selected-font-icon')
            var ignore_classes_fa = _.intersection(all_fa_list, classes);
            var ignore_classes_pe = _.intersection(all_pe_list, classes);
            var ignore_classes_emo = _.intersection(all_emo_list, classes);
            var ignore_classes_ti = _.intersection(all_ti_list, classes);
            var ignore_classes = _.union(ignore_classes_fa, ignore_classes_pe, ignore_classes_emo, ignore_classes_ti);
            var old_classes = _.difference(classes, ignore_classes);
            var final_classes = _.union(old_classes, new_classes);
            final_classes.push('fa-500px');
            $(this.media).attr("class", _.compact(final_classes).join(' ')).attr("style", style);
            this.options.wysiwyg.odooEditor.historyStep();
            $('.font-icons-dialog').modal('toggle');
        },

        renderElement: function () { // extract list of font (like awesome) from the cheatsheet.
            this.iconsEmoParser = emoIcons;
            this.icons_emo = _.flatten(_.map(emoIcons, function (data) {
                return data.icons;
            }));
            all_emo_list = this.icons_emo;
            this._super.apply(this, arguments);
        },

        clear: function () {
            this.media.className = this.media.className.replace(/(^|\s)(icon-[^\s]*)/g, ' ');
        },

    });

// ****************************emo***Start***emo******************************

// ***************************************************************************
// Tabler Icons -- https://github.com/tabler/tabler-icons
// ***************************************************************************
// *****************************ti***Start***ti*******************************

    var tiIcons = [{'base': 'ti', 'parser': /(?=^|\s)(\.ti-[0-9a-z_-]+::?before)/i}];

    var computeFonts_ti = _.once(function () {
        _.each(tiIcons, function (data) {
            data.cssData = getCssSelectors(data.parser);
            data.alias = [];
            data.icons = _.map(data.cssData, function (css) {
                data.alias.push.apply(data.alias, css[3]);
                return css[2];
            });
        });
    });

    var tiDialog = Widget.extend({
        template: 'icon_fonts.dialog.ti-icons',
        events: _.extend({}, Dialog.prototype.events, {
            'click .all-font-icons-icon': function (e) {
                e.preventDefault();
                e.stopPropagation();
                $(".all-font-icons-icon").removeClass("selected-font-icon");
                $(e.target).addClass("selected-font-icon");
            },
            'dblclick .all-font-icons-icon': function () {
                this.save();
            },
            'keydown.dismiss.bs.modal': function () {
            },
        }),

        init: function (parent, media, options) {
            this._super.apply(this, arguments);
            this.parent = parent;
            this.media = media[0];
            this.options = options;
            if (editable) {
                this.$editable = editable;
            }
            computeFonts_ti();
        },

        start: function () {
            return this._super.apply(this, arguments);
        },

        save: function () {
            var self = this;
            var style = this.media.attributes.style ? this.media.attributes.style.value : '';
            var classes = (this.media.className || "").split(/\s+/);
            var classes1 = (this.$el.find('span.selected-font-icon')[0].className || "").split(/\s+/);
            var new_classes = _.without(classes1, 'all-font-icons-icon', 'selected-font-icon')
            var ignore_classes_fa = _.intersection(all_fa_list, classes);
            var ignore_classes_pe = _.intersection(all_pe_list, classes);
            var ignore_classes_emo = _.intersection(all_emo_list, classes);
            var ignore_classes_ti = _.intersection(all_ti_list, classes);
            var ignore_classes = _.union(ignore_classes_fa, ignore_classes_pe, ignore_classes_emo, ignore_classes_ti);
            var old_classes = _.difference(classes, ignore_classes);
            var final_classes = _.union(old_classes, new_classes);
            final_classes.push('fa-500px');
            $(this.media).attr("class", _.compact(final_classes).join(' ')).attr("style", style);
            this.options.wysiwyg.odooEditor.historyStep();
            $('.font-icons-dialog').modal('toggle');
        },

        renderElement: function () { // extract list of font (like awesome) from the cheatsheet.
            this.iconsTiParser = tiIcons;
            this.icons_ti = _.flatten(_.map(tiIcons, function (data) {
                return data.icons;
            }));
            all_ti_list = this.icons_ti;
            this._super.apply(this, arguments);
        },

        clear: function () {
            this.media.className = this.media.className.replace(/(^|\s)(ti(\s|$)|ti-[^\s]*)/g, ' ');
        },

    });

// *******************************ti***End***ti*******************************

    return {
        Dialog: Dialog,
        FontIconDialog: FontIconDialog,
    };

});
