# -*- encoding: utf-8 -*-

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class xsdvalidation_handler_wizard(models.TransientModel):
    _name = 'xsdvalidation.handler.wizard'
    _description = 'Wizard para validación XSD'
    
    error_filename  = fields.Char(string='Error filename', size=20, required=True)
    error_file      = fields.Binary(string='Detalles del error')
    sample_xmlname  = fields.Char(string='Sample XML Name', size=128, required=True)
    sample_xml      = fields.Binary(string='XML con validación fallida')


