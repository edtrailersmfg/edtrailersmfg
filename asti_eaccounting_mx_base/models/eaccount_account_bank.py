# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class bank_eaccount(models.Model):
    _name = 'eaccount.bank.account'
    _description = u'Versión simplificada para cuentas bancarias'
    
    
    name        = fields.Char()
    """
    bank_id     = fields.Many2one('res.bank', string='Banco', required=True)
    currency_id = fields.Many2one('res.currency', string='Moneda')
    account_id  = fields.Many2one('account.account', string='Cuenta Contable')

    def name_get(self):
        res = []
        for el in self:
            cad = (el.code and '[' + el.code + '] - ' or '') + (el.account_id and el.account_id.name or '') + (el.bank_id and el.bank_id.name or '')
            cad = cad or u'No se encontró el registro'
            res.append((el.id, cad))
        return res

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=20):
        args = args or []
        domain = []
        if not (name == '' and operator == 'ilike'):
            args += ['|','|',
                     ('code', 'ilike', name),
                     ('bank_id.name', 'ilike', name),
                     ('account_id.name', 'ilike', name)]
        result = self.search(domain + args, limit=limit)
        res = result.name_get()
        return res

    """


class partner_bank_fit(models.Model):
    _inherit = 'res.partner.bank'

    bank_id     = fields.Many2one('res.bank', string='Banco', required=True) # Contabilidad 1.3

    def name_get(self):
        res = []
        for el in self:
            cad = (el.bank_id.name or '') + (el.acc_number and ' [Cta: ' + el.acc_number + ']' or '') + (el.partner_id and (' - ' + el.partner_id.name) or '')
            cad = cad or u'No se encontró el registro'
            res.append((el.id, cad))
        return res

    
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=20):
        args = args or []
        domain = []
        if not (name == '' and operator == 'ilike'):
            args += ['|','|',
                     ('acc_number', 'ilike', name),
                     ('bank_id.name', 'ilike', name),
                     ('partner_id.name', 'ilike', name)]
        result = self.search(domain + args, limit=limit)
        res = result.name_get()
        return res    


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: