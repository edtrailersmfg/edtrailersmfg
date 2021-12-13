# -*- encoding: utf-8 -*-
#

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from lxml import etree as et
import base64

class account_fit(models.Model):
    _inherit = 'account.account'

    sat_code_id     = fields.Many2one('sat.account.code', 'Código agrupador SAT')
    take_for_xml    = fields.Boolean(string='Considerar para XML', default=False,
                                     help='Si esta casilla esta seleccionada la cuenta será incluida en el catálogo de cuentas generado para la contabilidad electrónica.')
    in_debt         = fields.Boolean(string='Deudora', default=True)
    in_cred         = fields.Boolean(string='Acreedora')
    first_period_id = fields.Many2one('account.period', 'Primer periodo reportado', help='Periodo en que la cuenta fue reportada por primera vez ante el SAT. Ningún XML generado con un periodo anterior incluirá esta cuenta.')
    #rfc             = fields.Char(string='RFC', size=15)
    #apply_in_check  = fields.Boolean(string='Cheque')
    #apply_in_trans  = fields.Boolean(string='Transferencia')
    #apply_in_cfdi   = fields.Boolean(string='Comprobante CFDI')
    #apply_in_other  = fields.Boolean(string='Comp. otro')
    #apply_in_forgn  = fields.Boolean(string='Comp. extranjero')
    #apply_in_paymth = fields.Boolean(string='Método de pago')
    #eaccount_account_ids = fields.One2many('eaccount.bank.account', 'account_id', 'Cuentas Bancarias para CE')
        

    @api.onchange('in_debt')
    def on_change_debt(self):
        self.in_cred = not self.in_debt
        
    @api.onchange('in_cred')
    def on_change_cred(self):
        self.in_debt = not self.in_cred    
        
    def launch_period_chooser(self):
        if not len(self._context['active_ids']):
            raise UserError(_('No ha seleccionado cuentas contables para procesar.'))
        return {
            'type': 'ir.actions.act_window',
             'res_model': 'period.chooser',
             'view_mode': 'form',
             'view_type': 'form',
             'target': 'new',
             'name': 'Contabilidad Electrónica - Catálogo de cuentas',
             'context': {'active_ids': self._context['active_ids']}
            }

    """
    @api.model
    def create(self, vals):
        accountsFlag = True
        if vals.get('rfc', False):
            for acc in vals.get('eaccount_account_ids', []):
                if acc[2]:
                    accountsFlag = False
                    break

            if accountsFlag:
                raise UserError(_('Datos incompletos.\nAl asignar un RFC debe asignar cuentas bancarias.'))
        accountsFlag = False
        if 'eaccount_account_ids' in vals.keys():
            for acc in vals['eaccount_account_ids']:
                if acc[2]:
                    accountsFlag = True
                    break

            if accountsFlag and not vals.get('rfc', False):
                raise UserError(_('Datos incompletos\nAl asignar un cuentas bancarias debe asignar un RFC.'))
        return super(account_fit, self).create(vals)

    """

class period_chooser(models.TransientModel):
    _name = 'period.chooser'
    _description ="Seleccionador de Periodos"
    
    period_id = fields.Many2one('account.period', string='Periodo a generar', required=True)

    def generate_xml(self):
        wizard_vals = { 'xml_target': 'accounts_catalog',
                        'month': self.period_id.date_start[5:7],
                        'year': int(self.period_id.date_start[0:4])}
        wizId = self.env['files.generator.wizard'].create(wizard_vals)
        return wizId.process_file(account_ids=self._context['active_ids'])

