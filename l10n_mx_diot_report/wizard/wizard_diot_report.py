# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError, ValidationError
import base64
from datetime import date, datetime
from calendar import monthrange
from time import strftime
import tempfile
import os
from dateutil.relativedelta import *
import csv
import logging
_logger = logging.getLogger(__name__)

class wizard_account_diot_mx(models.TransientModel):
    _name = 'account.diot.report'
    _description = 'Account - DIOT Report for México'
    
    def _get_date_from(self):
        x = datetime.now().date()
        return date(x.year, x.month, 1)
    
    def _get_date_to(self):
        x = datetime.now().date()
        return date(x.year, x.month, monthrange(x.year, x.month)[1])
    
    name        = fields.Char(string='Archivo', readonly=True)
    company_id  = fields.Many2one('res.company', 'Compañía', required=True, default = lambda self: self.env.user.company_id)
    #period_id   = fields.Many2one('account.period', 'Periodo',help='Select period', required=True,
    #                             default=lambda self: self.env['account.period'].search([('date_start', '<=', fields.Date.today()), ('date_stop', '>=', fields.Date.today()), ('company_id', '=', self.env.user.company_id.id),('special','=',False)], limit=1))
    date_from   = fields.Date(string="Desde", required=True, default=_get_date_from)
    date_to   = fields.Date(string="Hasta", required=True, default=_get_date_to)
    filename    = fields.Char(string='Archivo para Revisión', size=128, readonly=True)
    filename_csv= fields.Char(string='Archivo CSV', size=128, readonly=True)
    file        = fields.Binary(string='Archivo (TXT)', readonly=True, help='Este archivo puede importarlo en el portal del SAT')
    file_csv    = fields.Binary(string='Archivo TXT', readonly=True, 
                                help='It will open in your program office, to validate numbers')
    state       = fields.Selection([('choose', 'Seleccione'), 
                                    ('get', 'Obtener'),
                                    ('not_file', 'No hay archivo')],
                                  string='Estado', default='choose')
    
    @api.onchange('date_from')
    def _onchange_date_from(self):
        self.date_to = date(self.date_from.year, self.date_from.month, monthrange(self.date_from.year, self.date_from.month)[1])
    
    ##################################################################
    def _get_columns_name(self, options):
        return [
            {},
            {'name': _('Type of Third')},
            {'name': _('Type of Operation')},
            {'name': _('VAT')},
            {'name': _('Country')},
            {'name': _('Nationality')},
            {'name': _('Paid 16%'), 'class': 'number'},
            {'name': _('Paid 16% - Non-Creditable'), 'class': 'number'},
            {'name': _('Paid 8 %'), 'class': 'number'},
            {'name': _('Paid 8 % - Non-Creditable'), 'class': 'number'},
            {'name': _('Importation 16%'), 'class': 'number'},
            {'name': _('Paid 0%'), 'class': 'number'},
            {'name': _('Exempt'), 'class': 'number'},
            {'name': _('Withheld'), 'class': 'number'},
        ]

    def create_diot(self):
        context = self.env.context
        journal_ids = []
        company_obj = self.env['res.company']
        company_ids = company_obj.search([('id','child_of', self.env.user.company_id.id)])

        ######## DATOS DE LOS IMPUESTOS A USAR PARA LA DIOT
        tag_16 = self.env.ref('l10n_mx.tag_diot_16')
        tag_non_cre = self.env.ref('l10n_mx.tag_diot_16_non_cre', raise_if_not_found=False) or self.env['account.account.tag']
        tag_8 = self.env.ref('l10n_mx.tag_diot_8', raise_if_not_found=False) or self.env['account.account.tag']
        tag_8_non_cre = self.env.ref('l10n_mx.tag_diot_8_non_cre', raise_if_not_found=False) or self.env['account.account.tag']
        tag_imp = self.env.ref('l10n_mx.tag_diot_16_imp')
        tag_imp_non_cre = self.env.ref('l10n_mx_diot_report.tag_diot_16_imp_non_cred')
        tag_imp_exento = self.env.ref('l10n_mx_diot_report.tag_diot_16_imp_exento')        
        tag_0 = self.env.ref('l10n_mx.tag_diot_0')
        tag_ret = self.env.ref('l10n_mx.tag_diot_ret')
        tag_exe = self.env.ref('l10n_mx.tag_diot_exento')
        rep_line_obj =  self.env['account.tax.repartition.line']

        purchase_tax_ids = self.env['account.tax'].search([('type_tax_use', '=', 'purchase'),
                                                           ('active','in',(True, False))]).ids
        
        diot_common_domain = ['|', ('invoice_tax_id', 'in', purchase_tax_ids), ('refund_tax_id', 'in', purchase_tax_ids)]
        
        company = self.env.company.id
        tax16 = rep_line_obj.search([('tag_ids', 'in', tag_16.ids), ('company_id', '=', company)] + diot_common_domain).mapped('tax_id')
        taxnoncre = self.env['account.tax']
        if tag_non_cre:
            taxnoncre = rep_line_obj.search([('tag_ids', 'in', tag_non_cre.ids), ('company_id', '=', company)] + diot_common_domain).mapped('tax_id')
        tax8 = self.env['account.tax']
        if tag_8:
            tax8 = rep_line_obj.search([('tag_ids', 'in', tag_8.ids), ('company_id', '=', company)] + diot_common_domain).mapped('tax_id')
        tax8_noncre = self.env['account.tax']
        if tag_8_non_cre:
            tax8_noncre = rep_line_obj.search([('tag_ids', 'in', tag_8_non_cre.ids), ('company_id', '=', company)] + diot_common_domain).mapped('tax_id')
            
        taximp = rep_line_obj.search([('tag_ids', 'in', tag_imp.ids), 
                                      ('company_id', '=', company)] + diot_common_domain).mapped('tax_id')
        taximp_non_cre = rep_line_obj.search([('tag_ids', 'in', tag_imp_non_cre.ids), 
                                              ('company_id', '=', company)] + diot_common_domain).mapped('tax_id')
        taximp_exento = rep_line_obj.search([('tag_ids', 'in', tag_imp_exento.ids), 
                                             ('company_id', '=', company)] + diot_common_domain).mapped('tax_id')
        tax0 = rep_line_obj.search([('tag_ids', 'in', tag_0.ids), ('company_id', '=', company)] + diot_common_domain).mapped('tax_id')
        tax_ret = rep_line_obj.search([('tag_ids', 'in', tag_ret.ids), ('company_id', '=', company)] + diot_common_domain).mapped('tax_id')
        tax_exe = rep_line_obj.search([('tag_ids', 'in', tag_exe.ids), ('company_id', '=', company)] + diot_common_domain).mapped('tax_id')
        
        ##################
        journals = self.env['account.journal'].search([('type','in',('cash','bank'))])
        journal_ids = journals.ids
        #for company in company_ids.filtered('tax_cash_basis_journal_id'):
        #    journal_ids.append(company.tax_cash_basis_journal_id.id)
        tax_ids = self.env['account.tax'].search([
            ('type_tax_use', '=', 'purchase'),
            ('active','in',(True, False)),
            ('tax_exigibility', '=', 'on_payment')])
        account_tax_ids = tax_ids.mapped('invoice_repartition_line_ids.account_id')
        account_tax_ids2 = taximp.mapped('invoice_repartition_line_ids.account_id')

        domain = [
            #('journal_id', 'in', journal_ids),
            ('account_id', 'not in', account_tax_ids.ids),
            ('tax_ids', 'in', tax_ids.ids),
            ('move_id.state', '=', 'posted'),
        ]
        
        date_from = self.date_from.isoformat()
        date_to = self.date_to.isoformat()
        
        sql = """
                select aml.partner_id, aml_tax_rel.account_tax_id, 
                sum(aml.debit - aml.credit)
                from account_move am
                    inner join account_move_line aml on aml.move_id=am.id
										 and aml.journal_id in (%s)
										 and aml.date between '%s' and '%s'
										 and aml.id in (SELECT account_move_line_id FROM account_move_line_account_tax_rel
														 WHERE account_tax_id IN (%s))
										 and (aml.display_type not in ('line_section','line_note') OR aml.display_type IS NULL)
										 and aml.account_id not in (%s)
										 
                    inner join account_move_line_account_tax_rel aml_tax_rel on aml_tax_rel.account_move_line_id=aml.id

                where am.state='posted'
                        AND (am.company_id in (%s) or am.company_id is null)
                GROUP BY aml.partner_id, aml_tax_rel.account_tax_id;
        """ % (', '.join([str(x) for x in journal_ids]),
               date_from, 
               date_to,
               ', '.join([str(x) for x in tax_ids.ids]),
               ', '.join([str(y) for y in account_tax_ids.ids]),
               ', '.join([str(z) for z in company_ids.ids])
              )
        self.env.cr.execute(sql)
        results = self.env.cr.fetchall()
        resultado = {}
        for res in results:
            resultado.setdefault(res[0], {}).setdefault(res[1], res[2])
        #_logger.info("resultado: %s" % resultado)
        
        #### --- IVA DE IMPORTACIONES GRAVADAS --- ####
        # No debe tener re-clasificacion en Pago
        if taximp:
            sql = """
                select vatline.partner_id, %s::integer account_tax_id,
                    round(sum(vatline.amount_base), 2) monto_base
                from account_move am
                        inner join account_move_line aml on aml.move_id=am.id
                                     and aml.date between '%s' and '%s'
                                     and (aml.display_type not in ('line_section','line_note') OR aml.display_type IS NULL)
                        inner join account_invoice_line_vatimport vatline on vatline.invoice_line_id=aml.id and vatline.line_type='iva_16_acred'
                where am.state='posted'
                    AND (am.company_id in (%s) or am.company_id is null)
                GROUP BY vatline.partner_id;
            """ % (taximp[0].id,
                #', '.join([str(x) for x in journal_ids]),
                   date_from, 
                   date_to,
                #   taximp[0].id,
                #   ', '.join([str(y) for y in account_tax_ids2.ids]),
                   ', '.join([str(z) for z in company_ids.ids])
                  )
            #_logger.info("\nsql: %s" % sql)
            self.env.cr.execute(sql)
            results = self.env.cr.fetchall()
            resultado2 = {}
            for res in results:
                resultado2.setdefault(res[0], {}).setdefault(res[1], res[2])

            for partner_id, result in resultado2.items():
                if partner_id in resultado:
                    resultado[partner_id].update(result)
                else:
                    resultado.update({partner_id : result})
        
        if taximp_non_cre:
            sql = """
                select vatline.partner_id, %s::integer account_tax_id,
                    round(sum(vatline.amount_base), 2) monto_base
                from account_move am
                        inner join account_move_line aml on aml.move_id=am.id
                                     and aml.date between '%s' and '%s'
                                     and (aml.display_type not in ('line_section','line_note') OR aml.display_type IS NULL)
                        inner join account_invoice_line_vatimport vatline on vatline.invoice_line_id=aml.id and vatline.line_type='iva_16_no_acred'
                where am.state='posted'
                    AND (am.company_id in (%s) or am.company_id is null)
                GROUP BY vatline.partner_id;
            """ % (taximp_non_cre[0].id,
                #', '.join([str(x) for x in journal_ids]),
                   date_from, 
                   date_to,
                #   taximp_non_cre[0].id,
                #   ', '.join([str(y) for y in account_tax_ids2.ids]),
                   ', '.join([str(z) for z in company_ids.ids])
                  )
            #_logger.info("\nsql: %s" % sql)
            self.env.cr.execute(sql)
            results = self.env.cr.fetchall()
            #_logger.info("resultado: %s" % resultado)
            resultado2 = {}
            for res in results:
                resultado2.setdefault(res[0], {}).setdefault(res[1], res[2])

            for partner_id, result in resultado2.items():
                if partner_id in resultado:
                    resultado[partner_id].update(result)
                else:
                    resultado.update({partner_id : result})
                
        if taximp_exento:
            sql = """
                select vatline.partner_id, %s::integer account_tax_id,
                    round(sum(vatline.amount_base), 2) monto_base
                from account_move am
                        inner join account_move_line aml on aml.move_id=am.id
                                     and aml.date between '%s' and '%s'
                                     and (aml.display_type not in ('line_section','line_note') OR aml.display_type IS NULL)
                        inner join account_invoice_line_vatimport vatline on vatline.invoice_line_id=aml.id and vatline.line_type='iva_exento'
                where am.state='posted'
                    AND (am.company_id in (%s) or am.company_id is null)
                GROUP BY vatline.partner_id;
            """ % (taximp_exento[0].id,
                #', '.join([str(x) for x in journal_ids]),
                   date_from, 
                   date_to,
                #   taximp_exento[0].id,
                #   ', '.join([str(y) for y in account_tax_ids2.ids]),
                   ', '.join([str(z) for z in company_ids.ids])
                  )
            #_logger.info("\nsql: %s" % sql)
            self.env.cr.execute(sql)
            results = self.env.cr.fetchall()
            #_logger.info("resultado: %s" % resultado)
            resultado2 = {}
            for res in results:
                resultado2.setdefault(res[0], {}).setdefault(res[1], res[2])

            for partner_id, result in resultado2.items():
                if partner_id in resultado:
                    resultado[partner_id].update(result)
                else:
                    resultado.update({partner_id : result})
        
        #### FIN: --- IVA DE IMPORTACIONES --- ####
        
        partner_obj = self.env['res.partner']
        mx_country = self.env.ref('base.mx')
        partners = {}
        partners_sin_rfc, partners_sin_reg_trib, partners_sin_datos = [], [], []
        for partner_id, result in resultado.items():
            partner = partner_obj.browse(partner_id)
            partners[partner] = result
            partner_vat = (partner.vat or '').replace('-', '').replace('_', '').replace(' ', '').upper()
            partner_tin = partner.number_fiscal_id_diot and partner.number_fiscal_id_diot.upper() or False
            # Validamos lo siguiente:
            #       No tiene Tipo Tercero o Tipo Operacion
            #       Proveedor Nacional sin RFC
            #       Proveedor Extranjero con RFC
            #       Proveedor Extranjero sin NIT (Numero de Identification Tributaria)
            if partner.country_id == mx_country and not partner.vat:
                partners_sin_rfc.append(partner_id)
                #raise UserError("El Proveedor %s no tiene definido un RFC, este es obligatorio en Proveedores Nacionales y Globales."  % partner.name)
            elif (partner.type_of_third == '05' and not partner_tin): # Extranjero sin Registro Tributario
                partners_sin_reg_trib.append(partner_id)
                #raise UserError("El Proveedor %s no tiene registrado su 'Registro Tributario', este dato es obligatorio para un Proveedor Extranjero."  % partner.name)
            elif (not partner.type_of_third or not partner.type_of_operation) or \
                 (partner.type_of_third == '05' and (not partner.country_id or not partner.number_fiscal_id_diot)):
                partners_sin_datos.append(partner_id)

        if partners_sin_rfc:
            return {
                    'name'      : u'Proveedores sin RFC',
                    'view_type' : 'form',
                    'view_mode' : 'tree,form',
                    'res_model' : 'res.partner',
                    'type'      : 'ir.actions.act_window',
                    'domain'    : [('id', 'in', partners_sin_rfc), '|', ('active', '=', False), ('active', '=', True)],
                   }
        elif partners_sin_reg_trib:
            return {
                    'name'      : u'Proveedores Extranjeros sin Registro Tributario',
                    'view_type' : 'form',
                    'view_mode' : 'tree,form',
                    'res_model' : 'res.partner',
                    'type'      : 'ir.actions.act_window',
                    'domain'    : [('id', 'in', partners_sin_reg_trib), '|', ('active', '=', False), ('active', '=', True)],
                   }        
        elif partners_sin_datos:
            return {
                    'name'      : _('Proveedores sin Datos para la DIOT (Tipo Operación, Tipo Tercero, Nacionalidad, etc.)'),
                    'view_type' : 'form',
                    'view_mode' : 'tree,form',
                    'res_model' : 'res.partner',
                    'type'      : 'ir.actions.act_window',
                    'domain'    : [('id', 'in', partners_sin_datos), '|', ('active', '=', False), ('active', '=', True)],
                   }


        sorted_partners = sorted(partners, key=lambda p: p.name or '')
        #unfold_all = context.get('print_mode') and not options.get('unfolded_lines')
        

        ##################################################
        (fileno, fname) = tempfile.mkstemp('.txt', 'tmp')
        os.close(fileno)
        f_write = open(fname, 'w')
        fcsv = csv.DictWriter(f_write, 
            ['type_of_third', 'type_of_operation',
            'vat', 'number_id_fiscal', 'foreign_name',
            'country_of_residence', 'nationality',
            'value_of_acts_or_activities_paid_at_the_rate_of_16%',
            'value_of_acts_or_activities_paid_at_the_rate_of_15%',
            'amount_of_non-creditable_VAT_paid_at_the_rate_of_16%',
            'value_of_acts_or_activities_paid_at_the_rate_of_11%_VAT',
            'value_of_acts_or_activities_paid_at_the_rate_of_10%_VAT',            
            'value_of_acts_or_activities_paid_estimulo_fiscal_frontera_norte_IVA_8%',   # UPDATE IVA 8% 
            'amount_of_non-creditable_VAT_paid_at_the_rate_of_11%',
            'amount_of_non-creditable_VAT_paid_estimulo_fiscal_frontera_norte_IVA_8%',   # UPDATE IVA 8% 
            'value_of_acts_or_activities_paid_on_import_of_goods_and_services_at_the_rate_of_16%_VAT',
            'amount_of_non-creditable_VAT_paid_by_imports_at_the_rate_of_16%',
            'value_of_acts_or_activities_paid_on_import_of_goods_and_services_at_the_rate_of_11%_VAT',
            'amount_of_non-creditable_VAT_paid_by_imports_at_the_rate_of_11%',
            'value_of_acts_or_activities_paid_on_import_of_goods_and_services_for_which_VAT_is_not_pay_(exempt)',
            'value_of_the_other_acts_or_activities_paid_at_the_rate_of_0%_VAT',
            'value_of_acts_or_activities_paid_by_those_who_do_not_pay_the_VAT_(Exempt)',
            'tax Withheld by the taxpayer',
            'vat_for_returns_discounts_and_rebates_on_purchases',
            'show_pipe', ], delimiter='|')
        
        (fileno, fname_csv) = tempfile.mkstemp('.csv', 'tmp_csv')
        os.close(fileno)
        f_write_csv = open(fname_csv, 'w')
        fcsv_csv = csv.DictWriter(f_write_csv, 
            ['type_of_third', 
             'type_of_operation',
             'vat', 
             'number_id_fiscal', 
             'foreign_name',
             'country_of_residence', 
             'nationality',
             'value_of_acts_or_activities_paid_at_the_rate_of_16%',
             'value_of_acts_or_activities_paid_at_the_rate_of_15%',
             'amount_of_non-creditable_VAT_paid_at_the_rate_of_16%',
             'value_of_acts_or_activities_paid_at_the_rate_of_11%_VAT',
             'value_of_acts_or_activities_paid_at_the_rate_of_10%_VAT',
             'value_of_acts_or_activities_paid_estimulo_fiscal_frontera_norte_IVA_8%',   # UPDATE IVA 8% 
             'amount_of_non-creditable_VAT_paid_at_the_rate_of_11%',
             'amount_of_non-creditable_VAT_paid_estimulo_fiscal_frontera_norte_IVA_8%',   # UPDATE IVA 8% 
             'value_of_acts_or_activities_paid_on_import_of_goods_and_services_at_the_rate_of_16%_VAT',
             'amount_of_non-creditable_VAT_paid_by_imports_at_the_rate_of_16%',
             'value_of_acts_or_activities_paid_on_import_of_goods_and_services_at_the_rate_of_11%_VAT',
             'amount_of_non-creditable_VAT_paid_by_imports_at_the_rate_of_11%',
             'value_of_acts_or_activities_paid_on_import_of_goods_and_services_for_which_VAT_is_not_pay_(exempt)',
             'value_of_the_other_acts_or_activities_paid_at_the_rate_of_0%_VAT',
             'value_of_acts_or_activities_paid_by_those_who_do_not_pay_the_VAT_(Exempt)',
             'tax Withheld by the taxpayer',
             'vat_for_returns_discounts_and_rebates_on_purchases',
             'show_pipe', ], delimiter=',')
        fcsv_csv.writerow(
            {'type_of_third' : 'Tipo de tercero', 
             'type_of_operation' :'Tipo de operacion', 
             'vat' : 'RFC', 
             'number_id_fiscal' : 'Numero de ID fiscal', 
             'foreign_name' : 'Nombre del extranjero',
             'country_of_residence' : 'Pais de residencia', 
             'nationality' : 'Nacionalidad',
             'value_of_acts_or_activities_paid_at_the_rate_of_16%' : 'Valor de los actos o actividades Pagados a la Tasa del 15% o 16% de IVA',
             'value_of_acts_or_activities_paid_at_the_rate_of_15%' : 'Valor de los actos o actividades Pagados a la Tasa del 15% de IVA',
             'amount_of_non-creditable_VAT_paid_at_the_rate_of_16%' : 'Monto del IVA Pagado No Acreditable a la Tasa del 15% o 16%',
             'value_of_acts_or_activities_paid_at_the_rate_of_11%_VAT' : 'Valor de los actos o actividades Pagados a la Tasa del 10% u 11% de IVA',
             'value_of_acts_or_activities_paid_at_the_rate_of_10%_VAT' : 'Valor de los actos o actividades Pagados a la Tasa del 10% de IVA',
             'value_of_acts_or_activities_paid_estimulo_fiscal_frontera_norte_IVA_8%' : 'Valor de los actos o actividades pagados sujeto al estimulo de la region fronteriza norte (IVA 8%)',  # UPDATE IVA 8%
             'amount_of_non-creditable_VAT_paid_at_the_rate_of_11%' : 'Monto del IVA Pagado No Acreditable a la Tasa del 10% u 11%',
             'amount_of_non-creditable_VAT_paid_estimulo_fiscal_frontera_norte_IVA_8%' : 'Monto del IVA Pagado No Acreditable sujeto al estimulo de la region fronteriza norte (IVA 8%)',  # UPDATE IVA 8%
             'value_of_acts_or_activities_paid_on_import_of_goods_and_services_at_the_rate_of_16%_VAT' : 'Valor de los actos o actividades Pagados en la importacion de bienes y servicios a la tasa del 15% o 16% de IVA',
             'amount_of_non-creditable_VAT_paid_by_imports_at_the_rate_of_16%' : 'Monto del IVA pagado no acreditable por la importacion a la tasa del 15% o 16%',
             'value_of_acts_or_activities_paid_on_import_of_goods_and_services_at_the_rate_of_11%_VAT' : 'Valor de los actos o actividades pagados en la importacion de bienes y servicios a la tasa del 10% u 11% de IVA',
             'amount_of_non-creditable_VAT_paid_by_imports_at_the_rate_of_11%' : 'Monto del IVA pagado no acreditable por la importacion a la tasa del 10% u 11%',
             'value_of_acts_or_activities_paid_on_import_of_goods_and_services_for_which_VAT_is_not_pay_(exempt)' : 'Valor de los actos o actividades pagados en la importacion de bienes y servicios por los que no se pagara el IVA (Exentos)',
             'value_of_the_other_acts_or_activities_paid_at_the_rate_of_0%_VAT' : 'Valor de los demas actos o actividades pagados a la tasa del 0% de IVA',
             'value_of_acts_or_activities_paid_by_those_who_do_not_pay_the_VAT_(Exempt)' : 'Valor de los actos o actividades pagados por los que no se pagara el IVA (Exentos)',
             'tax Withheld by the taxpayer' : 'IVA Retenido por el contribuyente',
             'vat_for_returns_discounts_and_rebates_on_purchases' : ' IVA correspondiente a las devoluciones, descuentos y bonificaciones'
            })
        
        sum_dic = {
            'value_of_acts_or_activities_paid_at_the_rate_of_16%' : 0,
            'amount_of_non-creditable_VAT_paid_at_the_rate_of_16%' : 0,
            'value_of_acts_or_activities_paid_estimulo_fiscal_frontera_norte_IVA_8%' : 0,
            'amount_of_non-creditable_VAT_paid_estimulo_fiscal_frontera_norte_IVA_8%' : 0,
            'value_of_acts_or_activities_paid_on_import_of_goods_and_services_at_the_rate_of_16%_VAT' : 0,
            'amount_of_non-creditable_VAT_paid_by_imports_at_the_rate_of_16%' : 0,
            'value_of_the_other_acts_or_activities_paid_at_the_rate_of_0%_VAT' : 0,
            'value_of_acts_or_activities_paid_by_those_who_do_not_pay_the_VAT_(Exempt)' : 0,
            'tax Withheld by the taxpayer' : 0,
            'value_of_acts_or_activities_paid_on_import_of_goods_and_services_for_which_VAT_is_not_pay_(exempt)': 0,
        }

        ##################################################
        for partner in sorted_partners:
            _logger.info("=== Partner: %s ===" % partner)
            p_columns = [
                partner.type_of_third or '', 
                partner.type_of_operation or '',
                partner.vat if partner.type_of_third=='04' else 'XAX010101000' if partner.type_of_third=='15' else '', 
                (partner.number_fiscal_id_diot or 'num_reg_trib' in partner._fields and partner.num_reg_trib) if partner.type_of_third=='05' else '',
                partner.name if partner.type_of_third=='05' else '',
                partner.country_id.code if partner.type_of_third=='05' else '',
                partner.country_id.nacionality if partner.type_of_third=='05' else '']
            partner_data = resultado[partner.id]
            total_tax16 = total_taximp = total_taximp_non_cre = total_taximp_exento = total_tax8 = 0
            total_tax0 = total_taxnoncre = total_tax8_noncre = 0
            exempt = 0
            withh = 0
            for tax in tax16.ids:
                total_tax16 += partner_data.get(tax, 0)
            p_columns.append(total_tax16)
            for tax in taxnoncre.ids:
                total_taxnoncre += partner_data.get(tax, 0)
            p_columns.append(total_taxnoncre)
            for tax in tax8.ids:
                total_tax8 += partner_data.get(tax, 0)
            p_columns.append(total_tax8)
            for tax in tax8_noncre.ids:
                total_tax8_noncre += partner_data.get(tax, 0)
            p_columns.append(total_tax8_noncre)
            _logger.info("taximp.ids: %s" % taximp.ids)
            _logger.info("partner_data: %s" % partner_data)
            _logger.info("partner_data.get(tax, 0): %s" % partner_data.get(tax, 0))
            for tax in taximp.ids:
                total_taximp += partner_data.get(tax, 0)
            p_columns.append(total_taximp)
            for tax in taximp_non_cre.ids:
                total_taximp_non_cre += partner_data.get(tax, 0)
            p_columns.append(total_taximp_non_cre)
            
            
            
            total_tax0 += sum([partner_data.get(tax, 0) for tax in tax0.ids])
            p_columns.append(total_tax0)
            exempt += sum([partner_data.get(exem, 0)
                           for exem in tax_exe.ids])
            p_columns.append(exempt)
            withh += sum([abs(partner_data.get(ret.id, 0) / (100 / ret.amount))
                          for ret in tax_ret])
            p_columns.append(withh)
            
            for tax in taximp_exento.ids: 
                total_taximp_exento += partner_data.get(tax, 0)
            p_columns.append(total_taximp_exento)
            
            _logger.info("p_columns: %s" % p_columns)
            
            
            fcsv.writerow({
                'type_of_third': p_columns[0],
                'type_of_operation': p_columns[1],
                'vat': p_columns[2],
                'number_id_fiscal': p_columns[3],
                'foreign_name': p_columns[4],
                'country_of_residence': p_columns[5],
                'nationality': p_columns[6],
                'value_of_acts_or_activities_paid_at_the_rate_of_16%': int(round(p_columns[7])) if p_columns[7] else "",
                'amount_of_non-creditable_VAT_paid_at_the_rate_of_16%' :  int(round(p_columns[8])) if p_columns[8] else "",
                'value_of_acts_or_activities_paid_estimulo_fiscal_frontera_norte_IVA_8%' :  int(round(p_columns[9])) if p_columns[9] else "",
                'amount_of_non-creditable_VAT_paid_estimulo_fiscal_frontera_norte_IVA_8%':  int(round(p_columns[10])) if p_columns[10] else "",
                'value_of_acts_or_activities_paid_on_import_of_goods_and_services_at_the_rate_of_16%_VAT' :  int(round(p_columns[11])) if p_columns[11] else "",
                'amount_of_non-creditable_VAT_paid_by_imports_at_the_rate_of_16%' :  int(round(p_columns[12])) if p_columns[12] else "",
                'value_of_the_other_acts_or_activities_paid_at_the_rate_of_0%_VAT' :  int(round(p_columns[13])) if p_columns[13] else "",
                'value_of_acts_or_activities_paid_by_those_who_do_not_pay_the_VAT_(Exempt)' :  int(round(p_columns[14])) if p_columns[14] else "",
                'tax Withheld by the taxpayer' :  int(round(p_columns[15])) if p_columns[15] else "",
                'value_of_acts_or_activities_paid_on_import_of_goods_and_services_for_which_VAT_is_not_pay_(exempt)' :  int(round(p_columns[16])) if p_columns[16] else "",
               })

            sum_dic.update({
                'type_of_third': 'Total',
                'value_of_acts_or_activities_paid_at_the_rate_of_16%' : sum_dic['value_of_acts_or_activities_paid_at_the_rate_of_16%'] + int(round(p_columns[7], 0)),
                'amount_of_non-creditable_VAT_paid_at_the_rate_of_16%' : sum_dic['amount_of_non-creditable_VAT_paid_at_the_rate_of_16%'] + int(round(p_columns[8], 0)),
                'value_of_acts_or_activities_paid_estimulo_fiscal_frontera_norte_IVA_8%' : sum_dic['value_of_acts_or_activities_paid_estimulo_fiscal_frontera_norte_IVA_8%'] + int(round(p_columns[9], 0)),
                'amount_of_non-creditable_VAT_paid_estimulo_fiscal_frontera_norte_IVA_8%': sum_dic['amount_of_non-creditable_VAT_paid_estimulo_fiscal_frontera_norte_IVA_8%'] + int(round(p_columns[10], 0)),
                'value_of_acts_or_activities_paid_on_import_of_goods_and_services_at_the_rate_of_16%_VAT' : sum_dic['value_of_acts_or_activities_paid_on_import_of_goods_and_services_at_the_rate_of_16%_VAT'] + int(round(p_columns[11], 0)),
                'amount_of_non-creditable_VAT_paid_by_imports_at_the_rate_of_16%' : sum_dic['amount_of_non-creditable_VAT_paid_by_imports_at_the_rate_of_16%'] + int(round(p_columns[12], 0)),
                'value_of_the_other_acts_or_activities_paid_at_the_rate_of_0%_VAT' : sum_dic['value_of_the_other_acts_or_activities_paid_at_the_rate_of_0%_VAT'] + int(round(p_columns[13], 0)),
                'value_of_acts_or_activities_paid_by_those_who_do_not_pay_the_VAT_(Exempt)' : sum_dic['value_of_acts_or_activities_paid_by_those_who_do_not_pay_the_VAT_(Exempt)'] + int(round(p_columns[14], 0)),
                'tax Withheld by the taxpayer' : sum_dic['tax Withheld by the taxpayer'] + int(round(p_columns[15], 0)),
                'value_of_acts_or_activities_paid_on_import_of_goods_and_services_for_which_VAT_is_not_pay_(exempt)' : sum_dic['value_of_acts_or_activities_paid_on_import_of_goods_and_services_for_which_VAT_is_not_pay_(exempt)'] + int(round(p_columns[16], 0)),
                #'vat_for_returns_discounts_and_rebates_on_purchases'  : int(round((values_diot[13] if values_diot[13] else 0.0), 0)) if values_diot[13] else "",                            
                })
            fcsv_csv.writerow(
                {'type_of_third'    : p_columns[0],
                'type_of_operation' : p_columns[1],
                'vat'               : p_columns[2],
                'number_id_fiscal'  : p_columns[3],
                'foreign_name'      : p_columns[4],
                'country_of_residence': p_columns[5],
                'nationality'       : p_columns[6],
                'value_of_acts_or_activities_paid_at_the_rate_of_16%': int(round(p_columns[7])) if p_columns[7] else "",
                'amount_of_non-creditable_VAT_paid_at_the_rate_of_16%' :  int(round(p_columns[8])) if p_columns[8] else "",
                'value_of_acts_or_activities_paid_estimulo_fiscal_frontera_norte_IVA_8%' :  int(round(p_columns[9])) if p_columns[9] else "",
                'amount_of_non-creditable_VAT_paid_estimulo_fiscal_frontera_norte_IVA_8%':  int(round(p_columns[10])) if p_columns[10] else "",
                'value_of_acts_or_activities_paid_on_import_of_goods_and_services_at_the_rate_of_16%_VAT' :  int(round(p_columns[11])) if p_columns[11] else "",
                'amount_of_non-creditable_VAT_paid_by_imports_at_the_rate_of_16%' :  int(round(p_columns[12])) if p_columns[12] else "",
                'value_of_the_other_acts_or_activities_paid_at_the_rate_of_0%_VAT' :  int(round(p_columns[13])) if p_columns[14] else "",
                'value_of_acts_or_activities_paid_by_those_who_do_not_pay_the_VAT_(Exempt)' :  int(round(p_columns[14])) if p_columns[14] else "",
                'tax Withheld by the taxpayer' :  int(round(p_columns[15])) if p_columns[15] else "",
                'value_of_acts_or_activities_paid_on_import_of_goods_and_services_for_which_VAT_is_not_pay_(exempt)' :  int(round(p_columns[16])) if p_columns[16] else "",
               })
        
        fcsv_csv.writerow(sum_dic)
        f_write.close()
        f_write_csv.close()
        f_read = open(fname, "rb")
        fdata = f_read.read()
        out = base64.encodebytes(fdata)
        name = "%s-%s-%s.txt" % ("ODOO-DIOT", self.company_id.name, strftime('%Y-%m-%d'))
        f_read.close()
        f_read_csv = open(fname_csv, "rb")
        fdata_csv = f_read_csv.read()
        out_csv = base64.encodebytes(fdata_csv)
        name_csv = "%s-%s-%s.csv" % ("ODOO-DIOT", self.company_id.name, strftime('%Y-%m-%d'))
        f_read.close()
        if out:
            state = 'get'
        else:
            state = 'not_file'
        self.write({'state'         : state,
                    'file'          : out,
                    'file_csv'      : out_csv,
                    'filename'      : name,
                    'filename_csv'  : name_csv,
                    })
        return {'type'      : 'ir.actions.act_window',
                'view_type' : 'form',
                'view_mode' : 'form',
                'res_id'    : self.id,
                'views'     : [(False, 'form')],
                'res_model' : 'account.diot.report',
                'target'    : 'new',
                }