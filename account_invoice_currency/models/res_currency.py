# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError
import time

class ResCurrency(models.Model):
    _inherit = "res.currency"

    
    def _get_rates2(self, company, date):
        self.env['res.currency.rate'].flush(['rate', 'currency_id', 'company_id', 'name'])
        query = """SELECT c.id,
                          COALESCE((SELECT r.rate2 FROM res_currency_rate r
                                  WHERE r.currency_id = c.id AND r.name <= %s
                                    AND (r.company_id IS NULL OR r.company_id = %s)
                               ORDER BY r.company_id, r.name DESC
                                  LIMIT 1), 1.0) AS rate2
                   FROM res_currency c
                   WHERE c.id IN %s"""
        self._cr.execute(query, (date, company.id, tuple(self.ids)))
        currency_rates = dict(self._cr.fetchall())
        return currency_rates
    
    @api.depends('rate_ids.rate')
    def _compute_current_rate(self):
        super(ResCurrency, self)._compute_current_rate()
        date = self._context.get('date') or fields.Date.today()
        company = self.env['res.company'].browse(self._context.get('company_id')) or self.env.company
        # the subquery selects the last rate before 'date' for the given currency/company
        currency_rates = self._get_rates2(company, date)
        for currency in self:
            currency.rate2 = currency_rates.get(currency.id) or 1.0


    #rate = fields.Float(compute='_compute_current_rate', string='T.C. Actual', #digits=(22, 16),
    #                    help='Este es el tipo de cambio actual de la moneda.')
    rate2   = fields.Float(compute="_compute_current_rate", string='T.C. Actual', digits=0,
                           compute_sudo=False, store=True)

    
    def _select_companies_rates(self):
        return """
            SELECT
                r.currency_id,
                COALESCE(r.company_id, c.id) as company_id,
                r.rate, r.rate2,
                r.name AS date_start,
                (SELECT name FROM res_currency_rate r2
                 WHERE r2.name > r.name AND
                       r2.currency_id = r.currency_id AND
                       (r2.company_id is null or r2.company_id = c.id)
                 ORDER BY r2.name ASC
                 LIMIT 1) AS date_end
            FROM res_currency_rate r
            JOIN res_company c ON (r.company_id is null or r.company_id = c.id)
        """

class ResCurrencyRate(models.Model):
    _inherit = "res.currency.rate"
    
    #rate = fields.Float(digits=(22, 16), default=1.0, 
    #                    help='Este es el tipo de cambio actual de la moneda. Si deja vacío este campo entonces será calculado en base al campo 1/T.C.')
    rate2 = fields.Float(string='T.C. Actual', digits=0,
                         required=False)
    
    
    
    @api.model
    def create(self, vals):
        if 'rate2' in vals and not vals['rate2'] and not vals['rate']:
            raise UserError(_("Error!\nNo se especificó el Tipo de Cambio"))
        if 'rate2' in vals and vals['rate2']:
            vals.update({'rate': 1.0  / vals['rate2']})
        elif vals['rate']:
            vals.update({'rate2': round(1.0  / vals['rate'], 4)})
        return super(ResCurrencyRate, self).create(vals)

    
    
    def write(self, vals):
        if 'rate2' in vals and vals['rate2']:
            vals.update({'rate': 1.0 / vals['rate2']})
        elif 'rate' in vals and vals['rate']:
            vals.update({'rate2': round(1.0 / vals['rate'], 4)})
        return super(ResCurrencyRate, self).write(vals)
