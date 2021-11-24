# -*- coding: utf-8 -*-
##############################################################################
#
#   Original by Odoo SA
#   Forked by:
#   2016 - Argil Consulting SA de CV
#    (<http://www.argil.mx>)
##############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
# ---------------------------------------------------------
# Account Entries Models
# ---------------------------------------------------------

class account_model(models.Model):
    _name = "account.model"
    _description = "Account Model for Account Move Subscription"

    name        = fields.Char(string='Model Name', required=True, help="This is a model for recurring accounting entries")
    journal_id  = fields.Many2one('account.journal', 'Journal', required=True)
    company_id  = fields.Many2one('res.company', related='journal_id.company_id', string='Company', store=True, readonly=True)
    lines_id    = fields.One2many('account.model.line', 'model_id', string='Model Entries', copy=True)
    legend      = fields.Text(string='Legend', readonly=True,
                             default=_('You can specify year, month and date in the name of the model using the following labels:\n\n%(year)s: To Specify Year \n%(month)s: To Specify Month \n%(date)s: Current Date\n\ne.g. My model on %(date)s'))
    notes       = fields.Text(string='Notes')

    
class account_model_line(models.Model):
    _name = "account.model.line"
    _description = "Account Model Entries"

    name        = fields.Char(string='Name', required=True)
    sequence    = fields.Integer(string='Sequence', required=True, help="The sequence field is used to order the resources from lower sequences to higher ones.")
    quantity    = fields.Float(string='Quantity', digits='Account', help="The optional quantity on entries.")
    debit       = fields.Float(string='Debit', digits='Account')
    credit      = fields.Float(string='Credit', digits='Account')
    account_id  = fields.Many2one('account.account', string='Account', required=True, ondelete="cascade")
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account', ondelete="cascade")
    model_id    = fields.Many2one('account.model', string='Model', required=True, ondelete="cascade", index=True)
    amount_currency = fields.Float(string='Amount Currency', help="The amount expressed in an optional other currency.")
    currency_id = fields.Many2one('res.currency', string='Currency')
    partner_id  = fields.Many2one('res.partner', string='Partner')
    date_maturity = fields.Selection([('today','Today''s Date'), 
                                      ('partner','Partner Payment Term')], string='Maturity Date', 
                                     help="The maturity date of the generated entries for this model. You can choose between the creation date or the creation date of the entries plus the partner payment terms.")

    _order = 'sequence'
    _sql_constraints = [
        ('credit_debit1', 'CHECK (credit*debit=0)',  'Wrong credit or debit value in model, they must be positive!'),
        ('credit_debit2', 'CHECK (credit+debit>=0)', 'Wrong credit or debit value in model, they must be positive!'),
    ]



# ---------------------------------------------------------
# Account Subscription
# ---------------------------------------------------------


class account_subscription(models.Model):
    _name = "account.subscription"
    _description = "Account Subscription"

    name        = fields.Char(string='Name', required=True)
    ref         = fields.Char(string='Reference')
    model_id    = fields.Many2one('account.model', 'Model', required=True)
    date_start  = fields.Date(string='Start Date', required=True, default=fields.Date.context_today)
    period_total = fields.Integer(string='Number of Periods', required=True, default=12)
    period_nbr  = fields.Integer(string='Period', required=True, default=1)
    period_type = fields.Selection([('day','days'),
                                    ('month','month'),
                                    ('year','year')], string='Period Type', required=True, default='month')
    state       = fields.Selection([('draft','Draft'),
                                    ('running','Running'),
                                    ('done','Done')], string='Status', default='draft',
                                   required=True, readonly=True, copy=False)
    lines_id    = fields.One2many('account.subscription.line', 'subscription_id', 'Subscription Lines', copy=True)


class account_subscription_line(models.Model):
    _name = "account.subscription.line"
    _description = "Account Subscription Line"

    subscription_id = fields.Many2one('account.subscription', string='Subscription', required=True, index=True)
    date            = fields.Date(string='Date', required=True)
    move_id         = fields.Many2one('account.move', string='Entry')

    _rec_name = 'date'


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:    
