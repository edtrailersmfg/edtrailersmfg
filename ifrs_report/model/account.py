# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, release
from odoo.exceptions import UserError, ValidationError
import datetime
import time
import logging
_logger = logging.getLogger(__name__)


class AccountPeriod(models.Model):
    _inherit = 'account.period'

    def _get_period_days(self, init_period, last_period):
        # TODO: ERASE LINE BEFORE GO-LIVE
        if type(init_period) == int:
            init_period = self.browse(init_period)
        if type(last_period) == int:
            last_period = self.browse(last_period)
        date_start = init_period.date_start
        date_stop = last_period.date_stop
        #date_start = datetime.datetime.strptime(date_start, '%Y-%m-%d')
        #date_stop = datetime.datetime.strptime(date_stop, '%Y-%m-%d')
        return (date_stop - date_start).days + 1

    
    def previous(self, period_id, step=1):
        period = self.browse(period_id)
        ids = [x.id for x in self.search([('date_stop', '<=', period.date_start),
                                         ('special', '=', False),
                                         ('company_id', '=', self.env.user.company_id.id)])]
        if len(ids) >= step:
            return ids[-step]

    def find_special_period(self, fy_id):
        fy_obj = self.env['account.fiscalyear']
        res = self.search([('fiscalyear_id', '=', fy_id), ('special', '=', True)])
        if res:
            return res[0].id
        fy_brw = fy_obj.browse(fy_id)
        raise UserError(_('Error !\n\nNo existe periodo especial en %s') % (fy_brw.name,))


class AccountFiscalyear(models.Model):
    _inherit = "account.fiscalyear"

    def _get_fy_period_ids(self, special=False):
        domain = special and [('fiscalyear_id', '=', self.id)] or [('fiscalyear_id', '=', self.id),('special', '=', special)]
        res = self.env['account.period'].search(domain)
        xres = [x.id for x in res]
        # if len(xres) not in (1,13):
        #     raise UserError(_('Error !\n\nPuede que no tenga configurado correctamente los Periodos en el Año Fiscal (Deben existir 12 periodos y un periodo especial de Cierre)'))
        return  xres

    def _get_fy_periods(self, fiscalyear_id, special=False):
        fiscal_br = self.browse(fiscalyear_id)
        return len(fiscal_br._get_fy_period_ids(special=special))

    def _get_fy_month(self, fiscalyear_id, period_id, special=False):
        if period_id == int:   
            ap_brw = self.env['account.period'].browse(period_id)
            start_date = ap_brw.date_start
        else:
            start_date = period_id.date_start
        return time.strptime(str(start_date), '%Y-%m-%d').tm_mon


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"    
    
    
    def _query_get2(self):
        query = super(AccountMoveLine, self)._query_get2()
        context = self.env.context.copy()
        #_logger.info("AccountMoveLine => context: %s" % context)
        if context.get('analytic', False):
            list_analytic_ids = context.get('analytic')
            analytic_ids = self.env['account.analytic.account'].search([('parent_id', 'child_of', list_analytic_ids)])
            if analytic_ids:
                query += 'AND l.analytic_account_id in (%s)' % (
                    ','.join([str(x.id) for x in analytic_ids]))
        #_logger.info("\nquery: \n%s" % query)
        return query
