# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import time


# Fiscal Year
class AccountFiscalYear(models.Model):
    _name = "account.fiscalyear"
    _description = "Account Fiscalyear - Dummy"
    
    
    name = fields.Char(required=True, index=True)
    company_id = fields.Many2one('res.company', string='Compañía', required=True,
                default=lambda self: self.env.user.company_id.id)
    date_start = fields.Date(string='Fecha Inicial', required=True, 
                             states={'done': [('readonly', True)]}, 
                             index=True, default=fields.Date.context_today)
    date_stop  = fields.Date(string='Fecha Final', required=True, 
                             states={'done': [('readonly', True)]}, 
                             index=True, default=fields.Date.context_today)
    period_ids = fields.One2many('account.period', 'fiscalyear_id', 
                                 string='Periodos', readonly=True)
    state = fields.Selection([('draft','Open'), ('done', 'Closed')], string='Estado', 
                             index=True, readonly=True, default='draft',
                             copy=False)

    _order = "name, date_start"
    _sql_constraints = [
        ('name_company_uniq', 'unique (name,company_id)', 'El nombre del Ejercicio Fiscal debe ser único por Compañía !')
    ]
    
    
    @api.onchange('name')
    def _onchange_name(self):
        try:
            ejercicio = int(self.name)
            if ejercicio < 2017 and ejercicio > 2050:
                warning = {'title': 'Advertencia !',
                           'message' : _("No puede crear periodos anteriores a 2017 o mayores de 2050")}
                self.name=''
                return {'warning' : warning}
            self.date_start = date(ejercicio, 1, 1)
            self.date_stop = date(ejercicio, 12, 31)
        except:
            return
    
    
    @api.model
    def create(self, vals):
        res = super(AccountFiscalYear, self).create(vals)
        res.create_period()
        return res
    
    
    def create_period(self):
        period_obj = self.env['account.period']
        for fy in self:
            if fy.period_ids:
                raise ValidationError(_("Aviso !\n\nNo se pueden crear periodos porque este Ejercicio Fiscal ya tiene Periodos definidos"))
            period_obj.create({
                    'name':  "%s%s" % ('13/', fy.date_stop.year),
                    'date_start': fy.date_stop,
                    'date_stop': fy.date_stop,
                    'special': True,
                    'fiscalyear_id': fy.id,
                })
            
            ds = fy.date_start
            while ds < fy.date_stop:
                de = ds + relativedelta(months=1, days=-1)
                if de > fy.date_stop:
                    de = fy.date_stop

                period_obj.create({
                    'name'      : ds.strftime('%m/%Y'),
                    'date_start' : ds,
                    'date_stop'   : de,
                    'fiscalyear_id': fy.id,
                })
                ds = ds + relativedelta(months=1)
        return True

    
    
    def close_fiscalyear(self):
        self.ensure_one()
        self.period_ids.write({'state': 'done'})
        self.write({'state': 'done'})
        
    
    def reopen_fiscalyear(self):
        self.ensure_one()
        self.write({'state': 'draft'})        
    
    
    
    def find(self, dt=None, exception=True):
        res = self.finds(dt, exception)
        return res and res[0] or False

    
    def finds(self, dt=None, exception=True):
        if not dt:
            dt = fields.Date.context_today(self)
        args = [('date_start', '<=' ,dt), ('date_stop', '>=', dt)]        
        if self._context.get('company_id', False):
            company_id = self._context['company_id']
        else:
            company_id = self.env.user.company_id.id
        args.append(('company_id', '=', company_id))
        ids = [x.id for x in self.search(args)]
        return ids



# Account Period
class AccountPeriod(models.Model):
    _name = "account.period"
    _description = "Account Periods - Dummy"
    
    
    @api.depends('name')
    def _get_name2(self):
        for rec in self:
            rec.name2 = rec.name[-4:]+ '-' + rec.name[:2]
    
    fiscalyear_id =  fields.Many2one('account.fiscalyear', string='Ejercicio Fiscal', 
                                     required=True, ondelete="cascade")
    name = fields.Char(string='Periodo', required=True, index=True)
    name2 = fields.Char(compute='_get_name2' ,string='Periodo.', store=True)
    special = fields.Boolean(string='Mes de Ajustes', required=False)
    company_id = fields.Many2one('res.company', string='Compañía', required=True,
                default=lambda self: self.env.user.company_id.id)
    date_start = fields.Date(string='Inicio', required=True, 
                            states={'done': [('readonly', True)]}, 
                            index=True, default=fields.Date.context_today)
    date_stop  = fields.Date(string='Final', required=True, 
                           states={'done': [('readonly', True)]}, index=True, 
                           default=fields.Date.context_today)
    state = fields.Selection([('draft','Abierto'),('done', 'Cerrado')], 
                             string='Estado', index=True, readonly=True, 
                             default='draft', copy=False)

    _order = "date_start, special desc"

    _sql_constraints = [
        ('name_company_uniq', 'unique (name,company_id)', 'El nombre del periodo debe ser único por Compañía !')
    ]

    
    @api.returns('self')
    def next(self, period, step):
        ids = self.search([('date_start','>',period.date_start)])
        if len(ids)>=step:
            return ids[step-1]
        return False

    @api.returns('self')
    def find(self, dt=None):
        #if context is None: context = {}
        if not dt:
            dt = fields.Date.context_today(self)
        args = [('date_start', '<=' ,dt), ('date_stop', '>=', dt)]
        if self._context.get('company_id', False):
            args.append(('company_id', '=', self._context['company_id']))
        else:
            args.append(('company_id', '=', self.env.user.company_id.id))
        result = []
        if self._context.get('account_period_prefer_normal', True):
            # look for non-special periods first, and fallback to all if no result is found
            result = self.search(args + [('special', '=', False)])
        if not result:
            result = self.search(args)
        if not result:
            model, action_id = self.env['ir.model.data'].get_object_reference('account', 'action_account_period')
            raise ValidationError(_('No hay Periodo definido para esta fecha: %s.\nPor favor revise los periodos') % dt)
        return result

    
    def action_draft(self):
        for period in self:
            if period.fiscalyear_id.state == 'done':
                raise ValidationError(_('No puede re-abrir el periodo cuando el Ejercicio Fiscal al que pertenece se encuentra Cerrado.'))
        self.write({'state':'draft'})
        #self._cr.execute('update account_period set state=%s where id in %s', (mode, tuple(self._ids),))
        #self.invalidate_cache()
        return True

    
    def write(self, vals):
        if 'company_id' in vals:
            move_lines = self.env['account.move.line'].search([('period_id', 'in', self._ids)])
            if move_lines:
                raise ValidationError(_('Este Diario contiene partidas para este Periodo, por tanto no es posible modificar el campo Compañía.'))
        return super(AccountPeriod, self).write(vals)

    
    def build_ctx_periods(self, period_from_id, period_to_id):
        if period_from_id == period_to_id:
            return [period_from_id]
        period_from = self.browse(period_from_id)
        period_date_start = period_from.date_start
        company1_id = period_from.company_id.id
        period_to = self.browse(period_to_id)
        period_date_stop = period_to.date_stop
        company2_id = period_to.company_id.id
        if company1_id != company2_id:
            raise ValidationError(_('You should choose the periods that belong to the same company.'))
        if period_date_start > period_date_stop:
            raise ValidationError(_('Start period should precede then end period.'))

        if period_from.special:
            return [x.id for x in self.search([('date_start', '>=', period_date_start), ('date_stop', '<=', period_date_stop)])]
        return [x.id for x in self.search([('date_start', '>=', period_date_start), ('date_stop', '<=', period_date_stop), ('special', '=', False)])]

    
# Close Account Period Wizard
class AccountPeriodClose(models.TransientModel):
    _name = "account.period.close"
    _description = "Asistente para Cierre de Mes"

    sure = fields.Boolean(string='Cerrar Periodo')


    def data_save(self):
        context = dict(self._context or {})
        period_ids = context.get('active_ids', [])
        if self.sure:
            account_move_ids = self.env['account.move'].search([('period_id', 'in', period_ids), ('state', '=', "draft")])
            if account_move_ids:
                raise ValidationError(_('Para poder Cerrar un Periodo es necesario que todas las pólizas en dicho periodo se encuentren Confirmadas.'))
            periods = self.env['account.period'].browse(period_ids)
            periods.write({'state':'done'})

        return {'type': 'ir.actions.act_window_close'}

