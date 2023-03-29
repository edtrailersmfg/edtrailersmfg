# -*- coding: utf-8 -*-

from odoo import api, fields, models, _, tools
from odoo.exceptions import ValidationError

### HERENCIA ###

class ProductTemplate(models.Model):
    _name = 'product.template'
    _inherit ='product.template'

    sat_product_id = fields.Many2one('sat.producto','Clave Producto SAT')
    no_identity_type = fields.Selection([('none','No Aplica'),
                                         ('default_code','Referencia Interna'),
                                         ('barcode','Codigo de Barras'), #Odoo 8 y Open 7 --> EAN13
                                         ('manual','Otro')
                                         ],'Tipo de Identificacion',
                                         default='default_code',
                                         help='Este Campo definira si se añadira o no el Valor NoIdentificacion en los Conceptos del XML.\nDescripcion por parte del SAT:\nEste campo puede registrar el Numero de Parte, Identificador del Producto o Servicio, la Clave del Producto, SKU del Producto..')

    no_identity_other = fields.Char('No. Identificacion Manual', size=100, help='Ingresa manualmente el No. Identificador')

    sat_tax_obj = fields.Selection(
        selection=[('01', '[ 01 ] No objeto de impuesto'), 
                   ('02', '[ 02 ] Sí objeto de impuesto'), 
                   ('03', '[ 03 ] Sí objeto del impuesto y no obligado al desglose'),],
        string='Objeto de Impuestos', default = '02')
    
class UomUom(models.Model):
    _inherit ='uom.uom'

    sat_uom_id = fields.Many2one('sat.udm','Clave SAT')

    
class ProductCategory(models.Model):
    _inherit ='product.category'

    sat_product_id = fields.Many2one('sat.producto','Clave Producto SAT')



