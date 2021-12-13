# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError



class product_uom(models.Model):
    _inherit = 'uom.uom'
    """
	Adds check to indicate if this UoM will be used when creating Invoice from POS Tickets for Partner is General Public
    """

    use_4_invoice_general_public = fields.Boolean(string='Usar para Publico en General')
    
    
    @api.constrains('use_4_invoice_general_public')
    def _check_use_4_invoice_general_public(self):        
        for record in self:
            if record.use_4_invoice_general_public:
                res = self.search([('use_4_invoice_general_public', '=', 1)])                
                if res and res.id != record.id:
                    raise UserError(_("Error ! You can have only one Unit of Measure checked to Use for General Public Invoice..."))
        return True


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: