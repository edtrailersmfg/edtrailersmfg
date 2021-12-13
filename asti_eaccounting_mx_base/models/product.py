# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

"""
class ProductCategory(models.Model):
    _inherit = "product.category"

    property_account_income_categ_id2 = fields.Many2one('account.account', company_dependent=True,
        string="Ingresos de Contado", 
        domain=[('deprecated', '=', False),('internal_type','=','other')],
        help="This account will be used for invoices when there is no Payment Term defined or Invoice Date equal to Date Due.")

class ProductTemplate(models.Model):
    _inherit = "product.template"

    property_account_income_id2 = fields.Many2one('account.account', company_dependent=True,
        string="Ingresos de Contado",
        domain=[('deprecated', '=', False),('internal_type','=','other')],
        help="This account will be used for invoices when there is no Payment Term defined or Invoice Date equal to Date Due.")
"""

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: