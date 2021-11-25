# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

# Products => We need flags for some process
class product_template(models.Model):
    _inherit ='product.template'

    import_vat = fields.Boolean(string='Es IVA Importaciones', 
                                help='Active si este producto lo usará para IVA de Importaciones')


    @api.onchange('import_vat')
    def _onchange_import_vat(self):
        if self.import_vat:
            self.taxes_id = False
            self.supplier_taxes_id = False
    
    @api.constrains('import_vat')
    def _check_import_vat(self):
        for record in self: 
            if record.import_vat and not (record.type=='service' and not record.sale_ok and record.purchase_ok):
                raise ValidationError(_('El producto está marcado que será usado como IVA de Importaciones pero debe ser Tipo = Servicio y marcado como "Se puede comprar"'))
            if record.import_vat:
                res = self.search([('import_vat', '=', 1)])
                if res and res[0] and res[0].id != record.id:
                    raise ValidationError(_('Error ! No puede tener mas de un producto definido como IVA Importaciones'))                
        return
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
