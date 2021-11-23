from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

class AccountTax(models.Model):
    _inherit = 'account.tax'

    use_tax_cash_basis = fields.Boolean('Reclasificar en Pago/Cobro', 
                                        help='Seleccione si desea que se agreguen las partidas de reclasificación de impuestos' + \
                                             'al momento del registro del Cobro/Pago')
    tax_cash_basis_account = fields.Many2one('account.account', string='Cuenta Impuesto Pagado/Cobrado', 
                                             domain=[('deprecated', '=', False),('internal_type','=','other')], 
                                             help='Cuenta a usar para la reclasificación del Impuesto Efectivamente Cobrado/Pagado')
    tax_cash_basis_account_diff_debit = fields.Many2one('account.account', string='Cuenta Diferencia (Cargo) x T.C.', 
                                             domain=[('deprecated', '=', False),('internal_type','=','other')], 
                                             help="Cuenta a usar para pagos de Factura en Moneda extranjera"
                                                  "donde el día de pago es diferente a la fecha de factura y"
                                                  "tiene el parámetro de Reclasificación basado en TC Fecha"
                                                  "de Pago. La diferencia (por TC) del monto del impuesto se"
                                                  "cargará a esta cuenta.")
    tax_cash_basis_account_diff_credit = fields.Many2one('account.account', string='Cuenta Diferencia (Abono) x T.C.', 
                                             domain=[('deprecated', '=', False),('internal_type','=','other')], 
                                             help="Cuenta a usar para pagos de Factura en Moneda extranjera"
                                                  "donde el día de pago es diferente a la fecha de factura y"
                                                  "tiene el parámetro de Reclasificación basado en TC Fecha"
                                                  "de Pago. La diferencia (por TC) del monto del impuesto se"
                                                  "abonará a esta cuenta.")
    
class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    amount_base      = fields.Float(string='Base (DIOT)', help='Monto base sin impuestos...')
    tax_id_secondary = fields.Many2one('account.tax', string='Impuesto DIOT', help='Impuesto para esta partida')
    not_move_diot    = fields.Boolean('No Tomar para Diot',
                                      help='Si se activa este campo, aunque la partida tenga información relacionada a Proveedores (DIOT) no se tomará en cuenta para el reporte de la DIOT...')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('tax_base_amount', False):
                vals['amount_base'] = vals['tax_base_amount']
            #if vals.get('tax_line_id', False):
            #    vals['tax_id_secondary'] = vals['tax_line_id']
            
        #_logger.info("vals_list: %s" % vals_list)
        
        return super(AccountMoveLine, self).create(vals_list)
        
    
    @api.onchange('account_id')
    def onchange_tax_secondary(self):
        tax_acc = False
        if self.account_id:
            tax_acc = self.env['account.tax'].search([('tax_cash_basis_account', '=', self.account_id.id)], limit=1)
        self.tax_id_secondary = self.account_id and tax_acc and tax_acc.id or False

    
    def write(self, vals):
        res = super(AccountMoveLine, self).write(vals)
        for line in self:
            if line.tax_id_secondary and line.tax_id_secondary.type_tax_use == 'purchase':
                cat_tax = line.tax_id_secondary.tax_category_id
                if cat_tax and cat_tax.name in ('IVA', 'IVA-EXENTO') and line.amount_base <= 0 and\
                        not line.not_move_diot:
                    raise ValidationError(_('Las líneas con impuesto de Compra necesitan un valor en el Monto Base...'))
        return res
