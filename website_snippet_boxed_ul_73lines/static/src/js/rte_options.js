odoo.define('website_snippet_boxed_ul_73lines.options', function (require) {
'use strict';

var core = require('web.core');
var ajax = require('web.ajax');
var base = require('web_editor.base');
var widgets = require('web_editor.widget');
var rte = require('web_editor.rte');
var summernote = require('web_editor.rte.summernote');

var QWeb = core.qweb;
var _t = core._t;

var renderer = $.summernote.renderer;
var tplIconButton = renderer.getTemplate().iconButton;
var tplDropdown = renderer.getTemplate().dropdown;
var fn_tplPopovers = renderer.tplPopovers;

renderer.tplPopovers = function (lang, options) {
    var $popover = $(fn_tplPopovers.call(this, lang, options));
    $popover.find('.btn-group:has([data-value="fa-spin"])').append(
    	tplIconButton('fa fa-circle', {
	        title: _t('Circle'),
	        event: 'imageShape',
	        value: 'img-circle'
	    }));
    
    $popover.find('.btn-group:has([data-value="fa-spin"])').append(
        	tplIconButton('fa fa-square', {
    	        title: _t('Square'),
    	        event: 'imageShape',
    	        value: 'img-rounded'
    	    }));
    
    $popover.find('.btn-group:has([data-value="fa-spin"])').append(
        	tplIconButton('fa fa-sun-o', {
    	        title: _t('Shadow'),
    	        event: 'imageShape',
    	        value: 'shadow'
    	    }));
    
    
    $popover.find('.btn-group:has([data-value="fa-spin"])').append(
        	tplIconButton('fa fa-picture-o', {
    	        title: _t('Thumbnail'),
    	        event: 'codeview',
    	    }));
    
    // Color background Fa
//    var $popover = $(fn_tplPopovers.call(this, lang, options));
    var $imagePopover = $popover.find('.note-image-popover');
    var $backColor = $('<div class="btn-group"/>');
    $backColor.insertBefore($imagePopover.find('.btn-group:first'));
    
    var dropdown_con = [
        '<li><a data-event="backColor" data-value="">'+_t('None')+'</a></li>',
        '<li><a data-event="backColor" data-value="bg-primary">'+_t('Primary')+'</a></li>',
        '<li><a data-event="backColor" data-value="bg-success">'+_t('Success')+'</a></li>',
        '<li><a data-event="backColor" data-value="bg-warning">'+_t('Warning')+'</a></li>',
        '<li><a data-event="backColor" data-value="bg-danger">'+_t('Danger')+'</a></li>',
    ];
    
    var $back_button = $(tplIconButton('fa fa-plus', {
        title: _t('Background Color'),
        dropdown: tplDropdown(dropdown_con)
    })).appendTo($backColor);
    
	return $popover;
	
	
};
	



});