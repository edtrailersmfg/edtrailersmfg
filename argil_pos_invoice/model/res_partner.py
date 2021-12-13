# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError


class res_partner(models.Model):
    _inherit = 'res.partner'
    """
	Adds check to indicate Partner is General Public
    """

    invoice_2_general_public = fields.Boolean(string='Facturar a Publico en General', help="Check this if this Customer will be invoiced as General Public")
    use_as_general_public    = fields.Boolean(string='Comodin Facturacion Publico en General', help="Check this if this Customer will be used to create Daily Invoice for General Public")
    
    @api.constrains('use_as_general_public')
    def _check_use_as_general_public(self):        
        for record in self:
            if record.use_as_general_public:
                res = self.search([('use_as_general_public', '=', 1), ('id','!=', record.id)])
                if res:
                    raise UserError(_("Error ! You can have only one Partner checked to Use for General Public Invoice..."))
        return True

    @api.onchange('use_as_general_public')
    def on_change_use_as_general_public(self):
        res = {}
        if self.use_as_general_public:
            self.invoice_2_general_public = False    
            
    @api.constrains('vat')
    def _constraint_uniq_vat(self):
       if self.is_company and self.vat:
            other_partner = self.search([('vat','=',self.vat),('id','!=',self.id),('is_company','=',True)])
            if other_partner:
                raise UserError(_("Error!\nEl RFC ya existe en la Base de Datos"))# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: