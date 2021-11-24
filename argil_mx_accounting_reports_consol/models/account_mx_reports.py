# -*- encoding: utf-8 -*-
#    Copyright (c) 2014 Argil Consulting - http://www.argil.mx
############################################################################
#    Coded by: Israel Cruz Argil (israel.cruz@argil.mx)
############################################################################

from odoo.tools.float_utils import float_round as round
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _


class AccountMonthlyBalanceWizard(models.TransientModel):
    _name = "account.monthly_balance_wizard"
    _description = "Generador de Balanza de Comprobacion"


    def _get_period_id(self):
        period = self.env['account.period'].search([('date_start', '<=', fields.Date.today()), ('date_stop', '>=', fields.Date.today()), ('company_id', '=', self.env.user.company_id.id)], limit=1)
        self.period_id = period and period[0] or False
        
    
    chart_account_id  = fields.Many2one('account.account', string='Chart of Account', 
                                        help='Select Charts of Accounts', required=True, 
                                        domain = [('parent_id','=',False)], 
                                        default=lambda self: self.env['account.account'].search([('parent_id','=',False),('company_id','=',self.env.user.company_id.id)], limit=1))
    company_id        = fields.Many2one('res.company', string='Company', change_default=True,
                            required=True, readonly=True,
                            default = lambda self: self.env.user.company_id)
    
    period_id          = fields.Many2one('account.period', string = 'Periodo', required=True,
                                        default=lambda self: self.env['account.period'].search([('date_start', '<=', fields.Date.today()), ('date_stop', '>=', fields.Date.today()), ('company_id', '=', self.env.user.company_id.id),('special','=',False)], limit=1))
    partner_breakdown  = fields.Boolean('Desglosar Empresas', default=False)
    output             = fields.Selection([
                                            ('list_view','Vista Lista'), 
                                            ('pdf','PDF'), 
                                        ], string = 'Salida',required=True, default='list_view')
    
        


class AccountMonthlyBalanceHeader(models.Model):
    _name = "account.monthly_balance_header"
    _description = "Header Balanza Mensual"

    create_uid  = fields.Many2one('res.users', string='Usuario', readonly=True)
    period_name = fields.Char(string='Periodo', size=64, readonly=True)
    date        = fields.Date(string='Fecha', readonly=True)
    line_ids    = fields.One2many('account.monthly_balance', 'header_id', string='Lines')
    
    _order = 'period_name asc'


class AccountMonthlyBalance(models.Model):
    _name = "account.monthly_balance"
    _description = "Account Chart Monthly Balance"


    header_id       = fields.Many2one('account.monthly_balance_header', string='Header', readonly=True)
    company_name    = fields.Char(string='Compañia', size=64, readonly=True)
    period_name     = fields.Char(string='Periodo·', size=64, readonly=True)                
    period_id       = fields.Many2one('account.period', string='Periodo', readonly=True)
    account_id      = fields.Many2one('account.account', string='Cuenta Contable', readonly=True)
    account_code    = fields.Char(string='Codigo', size=64, readonly=True)
    account_name    = fields.Char(string='Descripcion', size=1200, readonly=True)
    account_level   = fields.Integer(string='Nivel', readonly=True)
    account_type    = fields.Char(string='Tipo', size=64, readonly=True)
    account_internal_type = fields.Char(string='Tipo Interno', size=64, readonly=True)
    account_nature  = fields.Char(string='Naturaleza', size=64, readonly=True)
    account_sign    = fields.Integer(string='Signo', readonly=True)
    initial_balance = fields.Float(string='Saldo Inicial', readonly=True, digits='Account')
    debit           = fields.Float(string='Cargos', readonly=True, digits='Account')
    credit          = fields.Float(string='Abonos', readonly=True, digits='Account')
    balance         = fields.Float(string='Saldo del Periodo', readonly=True, digits='Account')
    ending_balance  = fields.Float(string='Saldo Acumulado', readonly=True, digits='Account')
    moves           = fields.Boolean(string='Con Movimientos', readonly=True)
    create_uid      = fields.Many2one('res.users', string='Created by', readonly=True)
    partner_id      = fields.Many2one('res.partner', string='Empresa', readonly=True, required=False)
    partner_name    = fields.Char(string='Empresa·', size=128, readonly=True, required=False)
    order_code      = fields.Char(string='Codigo orden', size=64, readonly=True)
    
    _order = 'order_code, account_level, partner_name asc'

                    
class AccountAccountLinesHeader(models.Model):
    _name = "account.account_lines_header"
    _description ="Encabezado de Auxiliares (para reporte)"

    create_uid      = fields.Many2one('res.users', string='Usuario', readonly=True)
    account_id      = fields.Many2one('account.account', string='Cuenta Contable', readonly=True)
    period_id_start = fields.Many2one('account.period', string='Periodo Inicial', readonly=True)
    period_id_end   = fields.Many2one('account.period', string='Periodo Final', readonly=True)
    partner_id      = fields.Many2one('res.partner', string='Empresa', readonly=True)
    product_id      = fields.Many2one('product.product', 'Producto', readonly=True)
    debit_sum       = fields.Float(string='Cargos', readonly=True, digits='Account')
    credit_sum      = fields.Float(string='Abonos', readonly=True, digits='Account')
    line_ids        = fields.One2many('account.account_lines', 'header_id', string='Lines')



class AccountAccountLines(models.Model):
    _name = "account.account_lines"
    _description = "Auxiliar de Cuentas"


    header_id         = fields.Many2one('account.account_lines_header', string='Header', readonly=True, ondelete='cascade')
    name              = fields.Char(string='Concepto Partida', size=1200, readonly=True)
    ref               = fields.Char(string='Referencia Partida', size=1200, readonly=True)
    move_id           = fields.Many2one('account.move', string='Póliza', readonly=True)
    user_id           = fields.Many2one('res.users', string='Usuario', readonly=True)
    journal_id        = fields.Many2one('account.journal', string='Diario', readonly=True)
    period_id         = fields.Many2one('account.period', string='Periodo', readonly=True)
    fiscalyear_id     = fields.Many2one('account.fiscalyear', string='Periodo Anual', 
                                        related='period_id.fiscalyear_id', store=False, readonly=True)
    account_id        = fields.Many2one('account.account', string='Cuenta Contable', readonly=True)
    account_type_id   = fields.Many2one('account.account.type', string='Tipo Cuenta', readonly=True)
    move_date         = fields.Date(string='Fecha Póliza', readonly=True)
    move_name         = fields.Char(string='Póliza No.', size=1200, readonly=True)
    move_ref          = fields.Char(string='Referencia Póliza', size=1200, readonly=True)
    period_name       = fields.Char(string='xPeriodo Mensual', size=1200, readonly=True)
    fiscalyear_name   = fields.Char(string='xPeriodo Anual', size=1200, readonly=True)
    account_code      = fields.Char(string='Codigo Cuenta', size=1200, readonly=True)
    account_name      = fields.Char(string='Descripcion Cuenta', size=1200, readonly=True)
    account_level     = fields.Integer(string='Nivel', readonly=True)
    account_type      = fields.Char(string='xTipo Cuenta', size=1200, readonly=True)
    account_sign      = fields.Integer(string='Signo', readonly=True)
    journal_name      = fields.Char(string='xDiario', size=1200, readonly=True)
    initial_balance   = fields.Float(string='Saldo Inicial', readonly=True, digits='Account')
    debit             = fields.Float(string='Cargos', readonly=True, digits='Account')
    credit            = fields.Float(string='Abonos', readonly=True, digits='Account')
    ending_balance    = fields.Float(string='Saldo Final', readonly=True, digits='Account')
    partner_id        = fields.Many2one('res.partner', string='Empresa', readonly=True)
    product_id        = fields.Many2one('product.product', string='Producto', readonly=True)
    qty               = fields.Float(string='Cantidad', readonly=True)
    sequence          = fields.Integer(string='Seq', readonly=True)
    amount_currency   = fields.Float(string='Monto M.E.', readonly=True, help="Monto en Moneda Extranjera", digits='Account')
    currency_id       = fields.Many2one('res.currency', string='Moneda', readonly=True)
    
    _order = 'sequence, period_name, move_date, account_code'



class AccountAccountLinesWizard(models.TransientModel):
    _name = "account.account_lines_wizard"
    _description = "Auxiliar de Cuentas"

    company_id      = fields.Many2one('res.company', string='Company', readonly=True,
                                     default = lambda self: self.env.user.company_id)
    fiscalyear_id   = fields.Many2one('account.fiscalyear', string='Periodo Anual',
                                     default=lambda self: self.env['account.fiscalyear'].search([('date_start', '<=', fields.Date.today()), ('date_stop', '>=', fields.Date.today()), ('company_id', '=', self.env.user.company_id.id)], limit=1))
    period_id_start = fields.Many2one('account.period', string='Periodo Inicial',
                                     default=lambda self: self.env['account.period'].search([('date_start', '<=', fields.Date.today()), ('date_stop', '>=', fields.Date.today()), ('company_id', '=', self.env.user.company_id.id),('special','=',False)], limit=1))
    period_id_stop  = fields.Many2one('account.period', string='Periodo Final',
                                     default=lambda self: self.env['account.period'].search([('date_start', '<=', fields.Date.today()), ('date_stop', '>=', fields.Date.today()), ('company_id', '=', self.env.user.company_id.id),('special','=',False)], limit=1))
    account_id      = fields.Many2one('account.account', string='Cuenta Contable')
    partner_id      = fields.Many2one('res.partner', string='Empresa')
    product_id      = fields.Many2one('product.product', string='Producto')
    output          = fields.Selection([
                                    ('list_view','Vista Lista'), 
                                    ('pdf','PDF'), 
                                ], string='Salida',required=True, default='list_view')



# Configurador de reportes basados en la Balanza de Comprobacion Mensual
#
class AccountMXReportDefinition(models.Model):
    _name = "account.mx_report_definition"
    _description = "Definición de Reportes basados en Balanza de Comprobación"

    @api.model
    def name_get(self):
        reads = self.read(['name','parent_id'])
        res = []
        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = record['parent_id'][1]+' / '+name
            res.append((record['id'], name))
        return res

    @api.model
    def _name_get_fnc(self):
        res = self.name_get()
        return dict(res)

    
    name              = fields.Char(string='Nombre', size=64, required=True)
    complete_name     = fields.Char(string='Nombre Completo', size=300, store=True, compute='_name_get_fnc')
    parent_id         = fields.Many2one('account.mx_report_definition',string='Parent Category', index=True)
    child_id          = fields.One2many('account.mx_report_definition', 'parent_id', string='Childs')
    sequence          = fields.Integer(string='Secuencia', help="Determina el orden en que se muestran los registros...")
    type              = fields.Selection([
                                        ('sum','Acumula'), 
                                        ('detail','Detalle'), 
                                    ], string='Tipo',required=True, default='sum')
    sign              = fields.Selection([
                                    ('positive', 'Positivo'), 
                                    ('negative', 'Negativo'), 
                                ], string='Signo',required=True, default='positive')
    print_group_sum   = fields.Boolean(string='Titulo de Grupo', help="Indica si se imprime el título del grupo de reporte...")
    print_report_sum  = fields.Boolean(string='Suma Final', help="Indica si se imprime la sumatoria total del reporte...")
    internal_group    = fields.Char(string='Grupo Interno', size=64, required=True)
    initial_balance   = fields.Boolean(string='Saldo Inicial Acum.')
    debit_and_credit  = fields.Boolean(string='Cargos y Abonos')
    ending_balance    = fields.Boolean(string='Saldo Final Acum.')
    debit_credit_ending_balance= fields.Boolean(string='Saldo Final Periodo')
    account_ids       = fields.Many2many('account.account', 'account_account_mx_reports_rel', 'mx_report_definition_id', 'account_id', string='Accounts')
    report_id         = fields.Many2one('account.mx_report_definition',string='Usar Reporte')
    report_id_use_resume = fields.Boolean(string='Solo Resultado', help="Si activa este campo solo se obtendra el resultado del reporte, de lo contrario se obtendra el detalle de las cuentas y/o subreportes incluidos.")
    report_id_account = fields.Char(string='Cuenta', size=64, help="Indique el numero de cuenta a mostrar en el reporte")
    report_id_label   = fields.Char(string='Descripcion', size=64, help="Indique la descripcion de la cuenta a mostrar en el reporte")
    report_id_show_result= fields.Boolean(string='Mostrar Resultado', help="Active esta casilla si desea que se muestre el resultado del subreporte")
    active            = fields.Boolean(string='Activo', default=True)
    account_entries   = fields.Boolean(string='Desglosar Movimientos')
    
    _order = 'sequence'


    @api.constrains('parent_id')
    def _check_parent_id_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_('Error ! You cannot create recursive reports.'))
        return True
    
    @api.constrains('report_id')
    def _check_report_id_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_('Error ! You cannot create recursive reports.'))
        return True    
    


# Clase donde se generan reportes configurados en la clase anterior
#
class AccountMXReportData(models.Model):
    _name = "account.mx_report_data"
    _description = "Datos para Reportes Financieros Configurables"

    report_id         = fields.Many2one('account.mx_report_definition', string='Reporte')
    report_group      = fields.Char(string='Grupo', size=64)
    report_section    = fields.Char(string='Seccion', size=64)
    sequence          = fields.Integer(string='Sequence')
    report_sign       = fields.Float(string='Signo en Reporte')
    account_sign      = fields.Float(string='Signo para Saldo')
    account_code      = fields.Char(string='Cuenta', size=64)
    account_name      = fields.Char(string='Descripcion', size=128)
    period_id         = fields.Many2one('account.period', string='Periodo')
    account_id        = fields.Many2one('account.account', string='Cuenta Contable')
    initial_balance   = fields.Float(string='Saldo Inicial')
    debit             = fields.Float(string='Cargos')
    credit            = fields.Float(string='Abonos')
    ending_balance    = fields.Float(string='Saldo Acumulado')
    debit_credit_ending_balance= fields.Float(string='Saldo Periodo')
    account_entries   = fields.Boolean(string='Desglosar Movimientos')
    account_id_line   = fields.One2many('account.mx_report_data.line', 'data_id', string='Partidas Contables', readonly=True)

    _order = 'sequence, account_code'

                    
# # # # # # # # # # # # # # # # # # # # #
class AccountMXReportDataLine(models.Model):
    _name = "account.mx_report_data.line"
    _description = "Reportes Financieros - Auxiliar de Cuentas"


    data_id         = fields.Many2one('account.mx_report_data', string='Data', readonly=True)
    name            = fields.Char(string='No se usa', size=64, readonly=True)
    move_id         = fields.Many2one('account.move', string='Poliza', readonly=True)
    user_id         = fields.Many2one('res.users', string='Usuario', readonly=True)
    journal_id      = fields.Many2one('account.journal', string='Diario', readonly=True)
    period_id       = fields.Many2one('account.period', string='Periodo', readonly=True)
    fiscalyear_id   = fields.Many2one('account.fiscalyear', string='Periodo Anual', readonly=True)
    account_id      = fields.Many2one('account.account', string='Cuenta Contable', readonly=True)
    account_type_id = fields.Many2one('account.account.type', string='Tipo Cuenta', readonly=True)
    move_date       = fields.Date(string='Fecha Poliza', readonly=True)
    move_name       = fields.Char(string='Poliza No.', size=120, readonly=True)
    move_ref        = fields.Char(string='Referencia', size=120, readonly=True)
    period_name     = fields.Char(string='xPeriodo Mensual', size=120, readonly=True)
    fiscalyear_name = fields.Char(string='xPeriodo Anual', size=120, readonly=True)
    account_code    = fields.Char(string='Codigo Cuenta', size=60, readonly=True)
    account_name    = fields.Char(string='Descripcion Cuenta', size=120, readonly=True)
    account_level   = fields.Integer(string='Nivel', readonly=True)
    account_type    = fields.Char(string='xTipo Cuenta', size=60, readonly=True)
    account_sign    = fields.Integer(string='Signo', readonly=True)
    journal_name    = fields.Char(string='xDiario', size=60, readonly=True)
    initial_balance = fields.Float(string='Saldo Inicial', readonly=True)
    debit           = fields.Float(string='Cargos', readonly=True)
    credit          = fields.Float(string='Abonos', readonly=True)
    ending_balance  = fields.Float(string='Saldo Final', readonly=True)
    partner_id      = fields.Many2one('res.partner', string='Empresa', readonly=True)
    product_id      = fields.Many2one('product.product', string='Producto', readonly=True)
    qty             = fields.Float(string='Cantidad', readonly=True)
    sequence        = fields.Integer(string='Seq', readonly=True)
    amount_currency = fields.Float(string='Monto M.E.', readonly=True, help="Monto en Moneda Extranjera")
    currency_id     = fields.Many2one('res.currency', string='Moneda', readonly=True)


    _order = 'sequence, period_name, move_date, account_code'


# # # # # # # # # # # # # # # # # # # # #
class AccountMXReportDataWizard(models.TransientModel):
    _name = "account.mx_report_data_wizard"
    _description = "Generador de Reporte Financiero"

    report_id    = fields.Many2one('account.mx_report_definition', string='Reporte Contable', required=True)
    period_id    = fields.Many2one('account.period', string='Periodo', required=True)
    report_type  = fields.Selection([('xls','XLS'),('pdf','PDF')
                                        ], string='Tipo', default='pdf')
    print_detail = fields.Boolean(string='Imprimir Detalle', help='Permite Imprimir en el Reporte el detalle de Movimientos.')
"""
    @api.multi
    def get_info(self):

        context = dict(self._context.copy() or {})

        data = context and context.get('active_ids', []) or []

        if self.report_id and self.report_id.id:

            self._cr.execute(""" """
            
            ---- Agregado para desglose de Partidas usado en el reporte
            
            drop function if exists f_get_mx_report_data_entries
            (x_account_id integer, x_period_id_start integer, x_period_id_stop integer);

            CREATE OR REPLACE FUNCTION f_get_mx_report_data_entries
            (x_account_id integer, x_period_id_start integer, x_period_id_stop integer)
            RETURNS TABLE(
            id integer,
            create_uid integer,
            create_date date,
            write_date date,
            write_uid integer,
            name varchar(64),
            move_id integer,
            user_id integer,
            journal_id integer,
            period_id integer,
            fiscalyear_id integer,
            account_id integer,
            account_type_id integer,
            move_date date,
            move_name varchar(120),
            move_ref varchar(120),
            period_name  varchar(120),
            fiscalyear_name varchar(120),
            account_code varchar(60),
            account_name varchar(120),
            account_level integer,
            account_type varchar(60),
            account_sign integer,
            journal_name varchar(60),
            initial_balance float,
            debit float, 
            credit float,
            ending_balance float,
            partner_id integer,
            product_id integer,
            qty float,
            sequence integer,
            amount_currency float,
            currency_id integer) 


            AS
            $BODY$
            DECLARE
                _cursor CURSOR FOR 
                    SELECT zx.id, zx.initial_balance, zx.debit, zx.credit, zx.ending_balance, zx.account_sign, zx.period_name, zx.move_date 
                        from report_data_entries zx order by zx.period_name, zx.move_date;
                _result record;
                last_balance float = 0;
                orden int = 0;
                _fiscalyear_id integer;
            BEGIN

                select fiscal.id into _fiscalyear_id
                from account_fiscalyear fiscal where fiscal.id = (select account_period.fiscalyear_id from account_period where account_period.id = $2);


                select 
                case date_part('month', period.date_start)
                    when 1 then 
                    account_type.sign * 
                    (select COALESCE(sum(line.debit), 0.00) -  COALESCE(sum(line.credit), 0.00)
                    from account_move move, account_move_line line, account_journal journal
                    where move.id = line.move_id and move.state='posted' 
                    --and line.state='valid' 
                    and line.account_id in (select f_account_child_ids(account.id))
                    and line.journal_id = journal.id and journal.type='situation'
                    and line.period_id = period.id
                    )
                    else
                        account_type.sign * 
                        (select COALESCE(sum(line.debit), 0.00) -  COALESCE(sum(line.credit), 0.00)
                        from account_move move, account_move_line line, account_journal journal
                        where move.id = line.move_id and move.state='posted' 
                        --and line.state='valid' 
                        and line.account_id in (select f_account_child_ids(account.id))
                        and line.journal_id = journal.id --and journal.type='situation'
                        and line.period_id in 
                        (select xperiodo.id from account_period xperiodo 
                          where xperiodo.fiscalyear_id=fiscalyear.id 
                        and xperiodo.name < period.name 
                        )
                    )
                    end::float
                    --initial_balance
                
                from account_period period, account_fiscalyear fiscalyear,
                account_account account,
                account_account_type account_type
                where account.id in (select f_account_child_ids($1))
                and account.active = True
                and period.id=$2
                and account.user_type=account_type.id 
                and period.fiscalyear_id = fiscalyear.id
                into last_balance;

                drop table if exists report_data_entries;


                create table report_data_entries AS 
                select move_line.id * 1000 + period.id as id, move.name as name, move.date move_date, move.name move_name, move.ref move_ref, period.name period_name, 
                fiscalyear.name fiscalyear_name, account.code account_code, account.name account_name, account.level account_level, account_type.name account_type,  
                account_type.sign account_sign,
                account.id account_id, account_type.id account_type_id,
                journal.name journal_name,
                move.id move_id, 
                move.create_uid user_id,
                journal.id journal_id,
                period.id period_id,
                fiscalyear.id fiscalyear_id,
                0.00::float initial_balance,
                coalesce(move_line.debit, 0.0)::float debit,
                coalesce(move_line.credit, 0.0)::float credit,
                0.00::float ending_balance,
                move_line.partner_id,
                move_line.product_id,
                move_line.quantity::float qty,
                0::integer as sequence,
                move_line.amount_currency::float amount_currency,
                move_line.currency_id
                from account_move move, account_move_line move_line, account_period period, account_fiscalyear fiscalyear,
                account_account account, account_account_type account_type,  account_journal journal
                where 
                move.id = move_line.move_id and move.state='posted' and
                move_line.period_id = period.id and --move_line.state='valid' and
                fiscalyear.id = period.fiscalyear_id and
                move_line.account_id = account.id and
                account.user_type = account_type.id and
                journal.id = move_line.journal_id and journal.type <> 'situation' 
                and account.id  in (select f_account_child_ids($1))
                and period.date_start >= (select _periodo1.date_start from account_period _periodo1 where _periodo1.id=$2)
                and period.date_stop  <= (select _periodo2.date_stop from account_period _periodo2 where _periodo2.id=$3)

                order by period.name, move.date;



                FOR _record IN _cursor
                LOOP
                    orden = orden + 1;
                    update report_data_entries xx
                    set sequence = orden,
                        initial_balance = last_balance, 
                        ending_balance = last_balance + 
                            (xx.account_sign * (xx.debit - xx.credit))
                    where xx.id=_record.id;

                    last_balance = last_balance + (_record.account_sign * (_record.debit - _record.credit));
                END LOOP;
    
                return query 
                    select  zz.id, 
                    zz.user_id create_uid, 
                    current_date create_date, 
                    current_date write_date, 
                     zz.user_id write_uid, 
                     zz.name, 
                     zz.move_id, 
                     zz.user_id, 
                     zz.journal_id, 
                     zz.period_id, 
                     zz.fiscalyear_id,
                     zz.account_id, 
                     zz.account_type_id, 
                     zz.move_date, 
                     zz.move_name, 
                     zz.move_ref, 
                        zz.period_name, 
                        zz.fiscalyear_name, 
                        zz.account_code, 
                        zz.account_name, 
                        zz.account_level,   
                        zz.account_type, 
                        zz.account_sign, 
                        zz.journal_name, 
                        zz.initial_balance, 
                        zz.debit, 
                        zz.credit, 
                        zz.ending_balance, 
                        zz.partner_id, 
                        zz.product_id, 
                        zz.qty, 
                        zz.sequence, 
                        zz.amount_currency, 
                        zz.currency_id
                    from report_data_entries zz
                    order by sequence, period_name, move_date;


            END
            $BODY$
            LANGUAGE 'plpgsql' ;

            -- Ejemplo de uso:
            -- select * from f_get_mx_report_data_entries(11875, 13, 13);
            -- Donde:
            --      11875 = Cuenta contable (ID)
            --      13 => ID del Periodo Inicial
            --      13 => ID del Periodo Final
            -----------------------------------------
            
                drop function if exists f_get_mx_report_data_detail_line
                (x_report_id integer, x_period_id integer, x_uid integer, x_parent_id integer, x_parent_group varchar(64));


                CREATE OR REPLACE FUNCTION f_get_mx_report_data_detail_line
                --(x_report_definition_id integer)
                ()
                RETURNS boolean
                AS
                $BODY$

                DECLARE
                _cursor2 CURSOR FOR 
                    SELECT _z.id, _z.account_id, _z.period_id
                    from account_mx_report_data _z
                    where _z.account_entries;
                _result2 record;

                BEGIN
                    FOR _record2 IN _cursor2
                    LOOP
                        insert into account_mx_report_data_line
                            (data_id, name, move_id, user_id, journal_id, 
                            period_id, fiscalyear_id, account_id, account_type_id, move_date,
                            move_name, move_ref, period_name, fiscalyear_name, account_code,
                            account_name, account_level, account_type, account_sign, journal_name,
                            initial_balance, debit, credit, ending_balance, partner_id,
                            product_id, qty, sequence, amount_currency, currency_id)
                        select 
                            _record2.id, name, move_id, user_id, journal_id, 
                            period_id, fiscalyear_id, account_id, account_type_id, move_date,
                            move_name, move_ref, period_name, fiscalyear_name, account_code,
                            account_name, account_level, account_type, account_sign, journal_name,
                            initial_balance, debit, credit, ending_balance, partner_id,
                            product_id, qty, sequence, amount_currency, currency_id
                            from f_get_mx_report_data_entries(_record2.account_id, _record2.period_id, _record2.period_id);
                    END LOOP;

                    return true;

                END
                $BODY$
                LANGUAGE 'plpgsql';
            
            
                drop function if exists f_get_mx_report_data_detail
                (x_report_id integer, x_period_id integer, x_uid integer, x_parent_id integer, x_parent_group varchar(64));


                CREATE OR REPLACE FUNCTION f_get_mx_report_data_detail
                (x_report_id integer, x_period_id integer, x_uid integer, 
                x_parent_id integer, x_parent_group varchar(64))
                RETURNS TABLE
                (
                create_uid integer,
                create_date timestamp,
                write_date timestamp,
                write_uid integer,
                report_id integer,
                report_group varchar(64),
                report_section varchar(64),
                sequence integer,
                report_sign float,
                account_sign float,
                account_id integer,
                account_code varchar(64),
                account_name varchar(128),
                period_id integer,
                initial_balance float,
                debit float, 
                credit float, 
                account_entries boolean) 

                AS
                $BODY$

                BEGIN

                    return query 
                    select 
                        x_uid, LOCALTIMESTAMP, LOCALTIMESTAMP, x_uid,
                        subreport.parent_id,
                        case char_length(x_parent_group) 
                        when 0 then subreport.internal_group 
                        else x_parent_group
                        end,
                        subreport.name,
                        subreport.sequence,
                        case subreport.sign
                        when 'positive' then 1.0
                        else -1.0
                        end::float,
                        account_type.sign::float, 
                        account.id,
                        account.code, 
                        account.name, 
                        period.id,

                        case date_part('month', period.date_start)
                        when 1 then 
                            account_type.sign * 
                            (select COALESCE(sum(line.debit), 0.00) -  COALESCE(sum(line.credit), 0.00)
                            from account_move move, account_move_line line, account_journal journal
                            where move.id = line.move_id and move.state='posted' 
                            --and line.state='valid' 
                            and line.account_id in (select f_account_child_ids(account.id))
                            and line.journal_id = journal.id and journal.type='situation'
                            and line.period_id = period.id
                            )
                        else
                            account_type.sign * 
                            (select COALESCE(sum(line.debit), 0.00) -  COALESCE(sum(line.credit), 0.00)
                            from account_move move, account_move_line line, account_journal journal
                            where move.id = line.move_id and move.state='posted' 
                            --and line.state='valid' 
                            and line.account_id in (select f_account_child_ids(account.id))
                            and line.journal_id = journal.id 
                            and line.period_id in 
                                (select xperiodo.id from account_period xperiodo 
                                where xperiodo.fiscalyear_id= (select fiscalyear.id from account_fiscalyear fiscalyear where period.fiscalyear_id = fiscalyear.id)
                                and xperiodo.name < period.name 
                                )
                            )
                        end::float,
                        (select COALESCE(sum(line.debit), 0.00) 
                        from account_move move, account_move_line line, account_journal journal
                        where move.id = line.move_id and move.state='posted' 
                        --and line.state='valid' 
                        and line.account_id in (select f_account_child_ids(account.id))
                        and line.journal_id = journal.id and journal.type<>'situation'
                        and line.period_id = period.id)::float
                        ,
                        (select COALESCE(sum(line.credit), 0.00) 
                        from account_move move, account_move_line line, account_journal journal
                        where move.id = line.move_id and move.state='posted' 
                        --and line.state='valid' 
                        and line.account_id in (select f_account_child_ids(account.id))
                        and line.journal_id = journal.id and journal.type<>'situation'
                        and line.period_id = period.id)::float,
                        subreport.account_entries
                        
                        from account_period period, 
                        account_mx_report_definition subreport 
                            left join account_account_mx_reports_rel subreport_accounts on subreport_accounts.mx_report_definition_id = subreport.id
                            left join account_account account on subreport_accounts.account_id = account.id
                            left join account_account_type account_type on account.user_type=account_type.id    
                        where period.id=x_period_id and
                        case x_parent_id 
                        when 0 then subreport.id = x_report_id
                        else subreport.parent_id = x_parent_id
                        end
                        order by subreport.parent_id, subreport.sequence, account.code;




                END
                $BODY$
                LANGUAGE 'plpgsql';

                --select * from f_get_mx_report_data_detail(14, 24, 1, 2)

                drop function if exists f_get_mx_report_data
                (x_report_id integer, x_period_id integer, x_uid integer);


                CREATE OR REPLACE FUNCTION f_get_mx_report_data
                (x_report_id integer, x_period_id integer, x_uid integer)
                RETURNS boolean 

                AS
                $BODY$

                DECLARE
                _cursor CURSOR FOR 
                    SELECT _a.id, _a.report_id, _a.parent_id, _a.name as report_section, case _a.sign when 'positive' then 1.0::float else -1.00::float end sign,
                    _a.sequence, _a.report_id_use_resume, _a.report_id_account, _a.report_id_label, _a.report_id_show_result, _a.internal_group     
                    from account_mx_report_definition _a 
                        where _a.parent_id = x_report_id 
                        order by _a.sequence;
                _result record;

                BEGIN
                    delete from account_mx_report_data;
                    delete from account_mx_report_data_line;
                    FOR _record IN _cursor
                    LOOP
                        insert into account_mx_report_data
                        (
                            create_uid, create_date, write_date, write_uid,
                        report_id, report_group, report_section, sequence, report_sign, account_sign, 
                        account_code, account_name, account_id, account_entries,
                        period_id, 
                        initial_balance, debit, credit, ending_balance, debit_credit_ending_balance
                            )

                        select 
                        create_uid, create_date, write_date, write_uid,
                        report_id, report_group, report_section, sequence, report_sign, account_sign, 
                        account_code, account_name, account_id, account_entries,
                        period_id, 
                        initial_balance, debit, credit,
                        (initial_balance  + account_sign * (debit - credit)) ending_balance,
                        (account_sign * (debit - credit)) debit_credit_ending_balance
                        from f_get_mx_report_data_detail(_record.id, x_period_id, x_uid, 0, '');
                        
                        IF _record.report_id is not null THEN
                            --RAISE NOTICE 'Hay un subreporte para % y la casilla resumido está en %', _record.report_section, _record.report_id_use_resume;
    
                            IF not _record.report_id_use_resume THEN
                                --RAISE NOTICE 'Entramos a generar el detalle del subreporte';
                                insert into account_mx_report_data
                                (
                                create_uid, create_date, write_date, write_uid,
                                report_id, report_group, report_section, sequence, report_sign, account_sign, 
                                account_code, account_name, --account_id, 
                                period_id, 
                                initial_balance, debit, credit, ending_balance, debit_credit_ending_balance
                                )
                                select 
                                create_uid, create_date, write_date, write_uid,
                                report_id, report_group, report_section, sequence, report_sign, account_sign, 
                                account_code, account_name, --account_id, 
                                period_id, 
                                initial_balance, debit, credit,
                                (initial_balance  + account_sign * (debit - credit)) ending_balance,
                                (account_sign * (debit - credit)) debit_credit_ending_balance               
                                from f_get_mx_report_data_detail(0, x_period_id, x_uid, _record.report_id, _record.internal_group);
                            ELSE
                                --RAISE NOTICE 'Generando solo el resultado del subreporte';
                                insert into account_mx_report_data
                                (
                                create_uid, create_date, write_date, write_uid,
                                report_id, report_group, report_section, sequence, report_sign, account_sign, 
                                account_code, account_name, --account_id, 
                                period_id, 
                                initial_balance, debit, credit, ending_balance, debit_credit_ending_balance
                                )
                                select 
                                create_uid, create_date, write_date, write_uid,
                                _record.parent_id as report_id, report_group, _record.report_section report_section, _record.sequence as sequence, _record.sign as report_sign, 1 as account_sign, 
                                _record.report_id_account::varchar(64) as account_code, _record.report_id_label::varchar(64) as account_name, period_id, 
                                --sum(initial_balance) initial_balance, sum(debit) debit, sum(credit) credit,
                               sum(initial_balance * report_sign) as initial_balance, 0.0::float as debit, 0.0::float as credit,
                                sum(report_sign * (initial_balance  + account_sign * (debit - credit))) ending_balance,
                                sum(report_sign * account_sign * (debit - credit)) debit_credit_ending_balance
                                from f_get_mx_report_data_detail(0, x_period_id, x_uid, _record.report_id, _record.internal_group)
                                group by 
                                create_uid, create_date, write_date, write_uid,
                                report_id, report_group, period_id;         
                            END IF;
                        END IF;

                    END LOOP;

                    return true;

                END
                $BODY$
                LANGUAGE 'plpgsql';
                select * from f_get_mx_report_data(""" """ + str(self.report_id.id) + "," + str(self.period_id.id) + "," +  str(self._uid) + ")")

            data = filter(None, map(lambda x:x[0], self._cr.fetchall()))
            if not data[0]:
                raise UserError(_('Error trying to get info for this report, please verify your configuration and try again.'))

            self._cr.execute("select * from f_get_mx_report_data_detail_line();")
            values = self.env['account.mx_report_data'].search([('id', '!=', 0)])
            ################### REPORTE JASPER REPORTS >>>>>>>>>>>>>>>
            # cr.execute('delete from print_move_jasper_mx;')
            # report_jasper_id = self.pool.get('print.move.jasper.mx').create(cr, uid, {}, context=None)
            # print "################ REPORTE >>>>>>> jasper >> ", report_jasper_id
            
            if values:
                report_mx = self.env['account.mx_report_data']
                initial_balance_global = 0.0
                debit_global = 0.0
                credit_global = 0.0
                ending_balance_global = 0.0
                debit_credit_ending_balance_global = 0.0
                report_group_list = []
                self._cr.execute("select report_group from account_mx_report_data;")
                report_group_cr = self._cr.fetchall()
                for rp in report_group_cr:
                    if rp[0] not in report_group_list:
                        report_group_list.append(rp[0])
                if  params.print_detail:
                    for report in report_group_list:
                        ids_to_update = report_mx.search([('report_group','=',str(report))])

                        initial_balance = 0.0
                        debit = 0.0
                        credit = 0.0
                        ending_balance = 0.0
                        debit_credit_ending_balance = 0.0

                        self._cr.execute(""" """select sum(initial_balance) from account_mx_report_data where id in %s""" """,(tuple(ids_to_update),))
                        initial_balance_cr = self._cr.fetchall()
                        if initial_balance_cr:
                            initial_balance = initial_balance_cr[0][0] if initial_balance_cr[0][0] != None else 0.0
                        self._cr.execute(""" """select sum(debit) from account_mx_report_data where id in %s""" """ ,(tuple(ids_to_update),))
                        debit_cr = self._cr.fetchall()
                        if debit_cr:
                            debit = debit_cr[0][0] if debit_cr[0][0] != None else 0.0
                        self._cr.execute(""" """select sum(credit) from account_mx_report_data where id in %s""" """ ,(tuple(ids_to_update),))
                        credit_cr = self._cr.fetchall()
                        if credit_cr:
                            credit = credit_cr[0][0] if credit_cr[0][0] != None else 0.0
                        self._cr.execute(""" """select sum(ending_balance) from account_mx_report_data where id in %s""" """ ,(tuple(ids_to_update),))
                        ending_balance_cr = self._cr.fetchall()
                        if ending_balance_cr:
                            ending_balance = ending_balance_cr[0][0] if ending_balance_cr[0][0] != None else 0.0
                        
                        self._cr.execute(""" """select sum(debit_credit_ending_balance) from account_mx_report_data where id in %s""" """ ,(tuple(ids_to_update),))
                        debit_credit_ending_balance_cr = self._cr.fetchall()
                        if debit_credit_ending_balance_cr:
                            debit_credit_ending_balance = debit_credit_ending_balance_cr[0][0] if debit_credit_ending_balance_cr[0][0] != None else 0.0
                        # for line in report.account_id_line:
                        #     initial_balance += line.initial_balance
                        #     debit += line.debit
                        #     credit += line.credit
                        #     ending_balance += line.ending_balance

                        # report.write({'jasper_report_id':report_jasper_id,
                        ctx = self._context.copy()
                        ctx.update({'ids':ids_to_update,'_ids':ids_to_update})
                        report_mx.with_context(ctx).write({
                            'initial_balance_sum': initial_balance,
                            'debit_sum': debit,
                            'credit_sum': credit,
                            'ending_balance_sum': ending_balance,
                            'debit_credit_ending_balance_sum': debit_credit_ending_balance,
                            })
                        ############### GLOBALES
                    ########## ACTUALIZANDO LOS DATOS GLOBALES
                    self._cr.execute(""" """select sum(initial_balance*report_sign) from account_mx_report_data where id in %s""" """,(tuple(values),))
                    initial_balance_global_cr = self._cr.fetchall()
                    if initial_balance_global_cr:
                        initial_balance_global = initial_balance_global_cr[0][0] if initial_balance_global_cr[0][0] != None else 0.0
                    self._cr.execute(""" """select sum(debit*report_sign) from account_mx_report_data where id in %s""" """ ,(tuple(values),))
                    debit_global_cr = self._cr.fetchall()
                    if debit_global_cr:
                        debit_global = debit_global_cr[0][0] if debit_global_cr[0][0] != None else 0.0
                    self._cr.execute(""" """select sum(credit*report_sign) from account_mx_report_data where id in %s""" """ ,(tuple(values),))
                    credit_global_cr = self._cr.fetchall()
                    if credit_global_cr:
                        credit_global = credit_global_cr[0][0] if credit_global_cr[0][0] != None else 0.0
                    self._cr.execute(""" """select sum(ending_balance*report_sign) from account_mx_report_data where id in %s""" """ ,(tuple(values),))
                    ending_balance_global_cr = self._cr.fetchall()
                    if ending_balance_global_cr:
                        ending_balance_global = ending_balance_global_cr[0][0] if ending_balance_global_cr[0][0] != None else 0.0
                    
                    self._cr.execute(""" """select sum(debit_credit_ending_balance*report_sign) from account_mx_report_data where id in %s""" """ ,(tuple(values),))
                    debit_credit_ending_balance_global_cr = self._cr.fetchall()
                    if debit_credit_ending_balance_global_cr:
                        debit_credit_ending_balance_global = debit_credit_ending_balance_global_cr[0][0] if debit_credit_ending_balance_global_cr[0][0] != None else 0.0
                    ctx.update({'ids':values,'_ids':values})
                    report_mx.with_context(ctx).write({
                        'initial_balance_global': initial_balance_global,
                        'debit_global': debit_global,
                        'credit_global': credit_global,
                        'ending_balance_global': ending_balance_global,
                        'debit_credit_ending_balance_global': debit_credit_ending_balance_global,
                        })


                    # for report in report_mx.browse(cr, uid, values, context=None):
                    #     initial_balance = 0.0
                    #     debit = 0.0
                    #     credit = 0.0
                    #     ending_balance = 0.0
                    #     debit_credit_ending_balance = 0.0

                    #     cr.execute(""" """select sum(initial_balance) from account_mx_report_data where report_group = %s and id in %s""" """,(report.report_group,tuple(values)))
                    #     initial_balance_cr = cr.fetchall()
                    #     if initial_balance_cr:
                    #         initial_balance = initial_balance_cr[0][0] if initial_balance_cr[0][0] != None else 0.0
                    #     cr.execute(""" """select sum(debit) from account_mx_report_data where report_group = %s and id in %s""" """ ,(report.report_group,tuple(values)))
                    #     debit_cr = cr.fetchall()
                    #     if debit_cr:
                    #         debit = debit_cr[0][0] if debit_cr[0][0] != None else 0.0
                    #     cr.execute(""" """select sum(credit) from account_mx_report_data where report_group = %s and id in %s""" """ ,(report.report_group,tuple(values)))
                    #     credit_cr = cr.fetchall()
                    #     if credit_cr:
                    #         credit = credit_cr[0][0] if credit_cr[0][0] != None else 0.0
                    #     cr.execute(""" """select sum(ending_balance) from account_mx_report_data where report_group = %s and id in %s""" """ ,(report.report_group,tuple(values)))
                    #     ending_balance_cr = cr.fetchall()
                    #     if ending_balance_cr:
                    #         ending_balance = ending_balance_cr[0][0] if ending_balance_cr[0][0] != None else 0.0
                        
                    #     cr.execute(""" """select sum(debit_credit_ending_balance) from account_mx_report_data where report_group = %s and id in %s""" """ ,(report.report_group,tuple(values)))
                    #     debit_credit_ending_balance_cr = cr.fetchall()
                    #     if debit_credit_ending_balance_cr:
                    #         debit_credit_ending_balance = debit_credit_ending_balance_cr[0][0] if debit_credit_ending_balance_cr[0][0] != None else 0.0
                    #     # for line in report.account_id_line:
                    #     #     initial_balance += line.initial_balance
                    #     #     debit += line.debit
                    #     #     credit += line.credit
                    #     #     ending_balance += line.ending_balance

                    #     # report.write({'jasper_report_id':report_jasper_id,
                    #     report.write({
                    #         'initial_balance_sum': initial_balance,
                    #         'debit_sum': debit,
                    #         'credit_sum': credit,
                    #         'ending_balance_sum': ending_balance,
                    #         'debit_credit_ending_balance_sum': debit_credit_ending_balance,
                    #         })
                    #     ############### GLOBALES

                    #     cr.execute(""" """select sum(initial_balance*report_sign) from account_mx_report_data where id in %s""" """,(tuple(values),))
                    #     initial_balance_global_cr = cr.fetchall()
                    #     if initial_balance_global_cr:
                    #         initial_balance_global = initial_balance_global_cr[0][0] if initial_balance_global_cr[0][0] != None else 0.0
                    #     cr.execute(""" """select sum(debit*report_sign) from account_mx_report_data where id in %s""" """ ,(tuple(values),))
                    #     debit_global_cr = cr.fetchall()
                    #     if debit_global_cr:
                    #         debit_global = debit_global_cr[0][0] if debit_global_cr[0][0] != None else 0.0
                    #     cr.execute(""" """select sum(credit*report_sign) from account_mx_report_data where id in %s""" """ ,(tuple(values),))
                    #     credit_global_cr = cr.fetchall()
                    #     if credit_global_cr:
                    #         credit_global = credit_global_cr[0][0] if credit_global_cr[0][0] != None else 0.0
                    #     cr.execute(""" """select sum(ending_balance*report_sign) from account_mx_report_data where id in %s""" """ ,(tuple(values),))
                    #     ending_balance_global_cr = cr.fetchall()
                    #     if ending_balance_global_cr:
                    #         ending_balance_global = ending_balance_global_cr[0][0] if ending_balance_global_cr[0][0] != None else 0.0
                        
                    #     cr.execute(""" """select sum(debit_credit_ending_balance*report_sign) from account_mx_report_data where id in %s""" """ ,(tuple(values),))
                    #     debit_credit_ending_balance_global_cr = cr.fetchall()
                    #     if debit_credit_ending_balance_global_cr:
                    #         debit_credit_ending_balance_global = debit_credit_ending_balance_global_cr[0][0] if debit_credit_ending_balance_global_cr[0][0] != None else 0.0
                    #     report_mx.write(cr, uid, values, {
                    #         'initial_balance_global': initial_balance_global,
                    #         'debit_global': debit_global,
                    #         'credit_global': credit_global,
                    #         'ending_balance_global': ending_balance_global,
                    #         'debit_credit_ending_balance_global': debit_credit_ending_balance_global,
                    #         }, context=None)

                    value = {
                        'type'          : 'ir.actions.report.xml',
                        'report_name'   : 'ht_reportes_contables_pdf' if self.report_type == 'pdf' else 'ht_reportes_contables_xls',
        #                'jasper_output' : params.report_type,
                        'datas'         : {
                                            'model' : 'account.mx_report_data',
                                            'ids'   : values,
        #                                    'report_type'   : params.report_type,
        #                                    'jasper_output' : params.report_type,
                                            }
                            }
                else:
                    value = {
                            'type'          : 'ir.actions.report.xml',
                            'report_name'   : 'ht_reportes_contables_pdf_not_detail' if self.report_type == 'pdf' else 'ht_reportes_contables_xls_not_detail',
            #                'jasper_output' : params.report_type,
                            'datas'         : {
                                                'model' : 'account.mx_report_data',
                                                'ids'   : values,
            #                                    'report_type'   : params.report_type,
            #                                    'jasper_output' : params.report_type,
                                                }
                                } 

        return value



class AccountMXReportData(models.Model):
    _inherit ='account.mx_report_data'
    
    initial_balance_sum = fields.Float(string='Saldo Inicial', digits=(14,2))
    debit_sum           = fields.Float(string='Cargos', digits=(14,2))
    credit_sum          = fields.Float(string='Abonos', digits=(14,2))
    ending_balance_sum  = fields.Float(string='Saldo Final', digits=(14,2))
    debit_credit_ending_balance_sum = fields.Float(string='Saldo del Periodo', digits=(14,2))
    initial_balance_global = fields.Float(string='Saldo Inicial Global', digits=(14,2))
    debit_global        = fields.Float(string='Cargos Global', digits=(14,2))
    credit_global       = fields.Float(string='Abonos Global', digits=(14,2))
    ending_balance_global = fields.Float(string='Saldo Final Global', digits=(14,2))
    debit_credit_ending_balance_global = fields.Float(string='Saldo del Periodo Global', digits=(14,2))
    

"""


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
