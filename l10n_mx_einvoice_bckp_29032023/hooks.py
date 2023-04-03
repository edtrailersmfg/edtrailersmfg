# coding: utf-8
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from os.path import join, dirname, realpath
import csv
from odoo import api, tools, SUPERUSER_ID

_logger = logging.getLogger(__name__)


def post_init_hook(cr, registry):
    _replace_report_in_mail_template(cr, registry)
    _load_sat_account_code(cr, registry) # Codigos del SAT
    _load_eaccount_currency(cr, registry) # Monedas (Contabilidad Electronica - SAT)
    _load_sat_producto(cr, registry) # Productos y Servicios (SAT)
    _load_sat_arancel(cr, registry) # Fracciones Arancelarias
    _load_res_country_zip_sat_code(cr, registry) # Codigos Postales
    _load_res_colonia_zip_sat_code(cr, registry) # Colonias
    # _load_sat_patente(cr, registry) # Patentes ¿Es necesario? ¿Se usa?
    # _load_sat_patente_aduanal(cr, registry) # Patentes Aduanales ¿Es necesario? ¿Se usa?
    
def _replace_report_in_mail_template(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    template = env.ref('account.email_template_edi_invoice', False)
    if template:
        report_cfdi = env.ref('account.account_invoices_cfdi', False)
        template.report_template = report_cfdi.id if report_cfdi else False
    config_settings = env['res.config.settings']
    ir_ui_view_obj = env['ir.ui.view']
    ir_ui_view_header = ir_ui_view_obj.search([('name','=','external_layout_background')])
    if ir_ui_view_header:
    	config_settings.external_report_layout_id =  ir_ui_view_header[0].id

    
def _load_sat_account_code(cr, registry):
    """Codigos agrupadores de Cuentas contables del SAT (catalogo de cuentas)"""
    _logger.info("\nCargando: Codigos agrupadores de Cuentas contables del SAT (catalogo de cuentas)")
    csv_path = join(dirname(realpath(__file__)), 'data', 'sat.account.code.csv')
    csv_file = open(csv_path, 'rb')
    csv_file.readline() # Read the header, so we avoid copying it to the db
    cr.copy_expert(
        """COPY sat_account_code (key, name)
           FROM STDIN WITH DELIMITER '|'""", csv_file)
    # Create xml_id, to allow make reference to this data
    cr.execute(
        """INSERT INTO ir_model_data
           (name, res_id, module, model, noupdate)
           SELECT concat('sat_account_code_', key), id, 'l10n_mx_einvoice', 'sat.account.code', 't'
           FROM sat_account_code""")
    
    _logger.info("\nFin Carga: Codigos agrupadores de Cuentas contables del SAT (Catalogo SAT)")
    
def _load_eaccount_currency(cr, registry):
    """Monedas (Catalogo SAT)"""
    _logger.info("\nCargando: Monedas (Catalogo SAT)")
    csv_path = join(dirname(realpath(__file__)), 'data', 'eaccount.currency.csv')
    csv_file = open(csv_path, 'rb')
    csv_file.readline() # Read the header, so we avoid copying it to the db
    cr.copy_expert(
        """COPY eaccount_currency (code, name, decimales, porcentaje_variacion)
           FROM STDIN WITH DELIMITER '|'""", csv_file)
    # Create xml_id, to allow make reference to this data
    cr.execute(
        """INSERT INTO ir_model_data
           (name, res_id, module, model, noupdate)
           SELECT concat('eaccount_currency_', code), id, 'l10n_mx_einvoice', 'eaccount.currency', 't'
           FROM eaccount_currency""")
    
    _logger.info("\nFin Carga: Monedas (Catalogo SAT)")

def _load_sat_producto(cr, registry):
    """Productos y Servicios (Catalogo SAT)"""
    _logger.info("\nCargando: Productos y Servicios (Catalogo SAT)")
    csv_path = join(dirname(realpath(__file__)), 'data',
                    'sat.producto.csv')
    csv_file = open(csv_path, 'rb')
    csv_file.readline() # Read the header, so we avoid copying it to the db
    cr.copy_expert(
        """COPY sat_producto (code, name, estimulo_franja_fronteriza, incluir_ieps_trasladado, incluir_iva_trasladado, incluye_complemento, palabras_similares, vigencia_inicio, complemento_que_debe_incluir)
           FROM STDIN WITH DELIMITER '|'""", csv_file)
    # Create xml_id, to allow make reference to this data
    cr.execute(
        """INSERT INTO ir_model_data
           (name, res_id, module, model, noupdate)
           SELECT concat('sat_producto_', code), id, 'l10n_mx_einvoice', 'sat.producto', 't'
           FROM sat_producto""")
    _logger.info("\nFin Carga: Productos y Servicios (Catalogo SAT)")
    

def _load_sat_arancel(cr, registry):
    """Fracciones Arancelarias (Catalogo SAT)"""
    _logger.info("\nCargando: Fracciones Arancelarias (Catalogo SAT)")
    csv_path = join(dirname(realpath(__file__)), 'data', 'sat.arancel.csv')
    csv_file = open(csv_path, 'rb')
    #csv_file.readline() # Read the header, so we avoid copying it to the db
    cr.copy_expert(
        """COPY sat_arancel (code, name, vigencia_inicio, unidad_de_medida)
           FROM STDIN WITH DELIMITER '|'""", csv_file)
    # Create xml_id, to allow make reference to this data
    cr.execute(
        """INSERT INTO ir_model_data
           (name, res_id, module, model, noupdate)
           SELECT concat('sat_arancel_', code), id, 'l10n_mx_einvoice', 'sat.arancel', 't'
           FROM sat_arancel""")
    _logger.info("\nFin Carga: Fracciones Arancelarias (Catalogo SAT)")
    
    
def _load_res_country_zip_sat_code(cr, registry):
    """Codigos Postales (Catalogo SAT)"""
    _logger.info("\nCargando: Codigos Postales (Catalogo SAT) - Puede tardar de 2 a 4 minutos (dependiendo los recursos del servidor)")
    env = api.Environment(cr, SUPERUSER_ID, {})
    csv_path = join(dirname(realpath(__file__)), 'data', 'res.country.zip.sat.code.csv')
    zip_vals_list = []
    #_logger.info("\nConstruyendo Dict: Codigos Postales (Catalogo SAT)")
    with open(csv_path, 'r') as csv_file:
        for row in csv.DictReader(csv_file, delimiter='|', 
                                  fieldnames=['xml_id', 'code', 'state_sat_code', 'township_sat_code', 'locality_sat_code']):
            state = env.ref('base.%s' % row['state_sat_code'], raise_if_not_found=False)
            township = env.ref('l10n_mx_einvoice.%s' % row['township_sat_code'], raise_if_not_found=False)
            locality = env.ref('l10n_mx_einvoice.%s' % row['locality_sat_code'], raise_if_not_found=False)
            
            zip_vals_list.append({
                'code': row['code'],
                'state_sat_code'    : state.id if state else False,
                'township_sat_code' : township.id if township else False,
                'locality_sat_code' : locality.id if locality else False,
                'xml_id'            : row['xml_id']
            })
    

    _logger.info("\nAun cargando: Codigos Postales (Catalogo SAT)")
    zip_codes = env['res.country.zip.sat.code'].create(zip_vals_list)
    #_logger.info("\nFin de Carga Base: Codigos Postales (Catalogo SAT)")
    if zip_codes:
        cr.execute('''
           INSERT INTO ir_model_data (name, res_id, module, model, noupdate)
               SELECT 
                    res_country_zip_sat_code.xml_id,
                    res_country_zip_sat_code.id,
                    'l10n_mx_einvoice',
                    'res.country.zip.sat.code',
                    TRUE
               FROM res_country_zip_sat_code
               WHERE res_country_zip_sat_code.id IN %s
        ''', [tuple(zip_codes.ids)])
        
        cr.execute('''
            update res_partner set zip_sat_id=res_country_zip_sat_code.id 
            from res_country_zip_sat_code 
            where res_partner.zip is not null and res_country_zip_sat_code.code = res_partner.zip
                and res_partner.zip_sat_id is null;''')

    _logger.info("\nFin Carga: Codigos Postales (Catalogo SAT)")
    
def _load_res_colonia_zip_sat_code(cr, registry):
    """Colonias (Catalogo SAT)"""
    _logger.info("\nCargando: Colonias (Catalogo SAT) - Puede tardar de 2 a 4 minutos (dependiendo los recursos del servidor)")
    env = api.Environment(cr, SUPERUSER_ID, {})
    csv_path = join(dirname(realpath(__file__)), 'data', 'res.colonia.zip.sat.code.csv')
    colonias_vals_list = []
    _logger.info("\nConstruyendo Dict: Colonias (Catalogo SAT)")

    with open(csv_path, 'r') as csv_file:
        for row in csv.DictReader(csv_file, delimiter='|', 
                                  fieldnames=['xml_id', 'code', 'name', 'zip_sat_code']):
            zip_code = env.ref('l10n_mx_einvoice.%s' % row['zip_sat_code'], raise_if_not_found=False)
            colonias_vals_list.append({
                'code'              : row['code'],
                'name'              : row['name'],
                'zip_sat_code'      : zip_code.id if zip_code else False,
                'xml_id'            : row['xml_id']
            })
    

    _logger.info("\nAun Cargando: Colonias (Catalogo SAT)")
    zip_codes = env['res.colonia.zip.sat.code'].create(colonias_vals_list)
    #_logger.info("\nFin de Carga Base: Colonias (Catalogo SAT)")
    if zip_codes:
        cr.execute('''
           INSERT INTO ir_model_data (name, res_id, module, model, noupdate)
               SELECT 
                    res_colonia_zip_sat_code.xml_id,
                    res_colonia_zip_sat_code.id,
                    'l10n_mx_einvoice',
                    'res.colonia.zip.sat.code',
                    TRUE
               FROM res_colonia_zip_sat_code
               WHERE res_colonia_zip_sat_code.id IN %s
        ''', [tuple(zip_codes.ids)])

    _logger.info("\nFin Carga: Colonias (Catalogo SAT)")
    
    
def _load_sat_patente(cr, registry):
    """Patentes (Catalogo SAT)"""
    _logger.info("\nCargando: Patentes (Catalogo SAT)")
    env = api.Environment(cr, SUPERUSER_ID, {})
    csv_path = join(dirname(realpath(__file__)), 'data', 'sat.patente.csv')
    patentes_vals_list = []
    _logger.info("\nConstruyendo Dict: Patentes (Catalogo SAT) - Puede tardar de 1 a 2 minutos (dependiendo los recursos del servidor)")

    with open(csv_path, 'r') as csv_file:
        for row in csv.DictReader(csv_file, delimiter='|', 
                                  fieldnames=['xml_id', 'aduana_id', 'cantidad', 'ejercicio', 'start_date', 'name']):
            aduana_code = env.ref('l10n_mx_einvoice.%s' % row['aduana_id'], raise_if_not_found=False)
            patentes_vals_list.append({
                'aduana_id' : aduana_code.id if aduana_code else False,
                'name'      : row['name'],
                'ejercicio' : row['ejercicio'],
                'cantidad'  : row['cantidad'],
                'start_date': row['start_date'],
                'xml_id'    : row['xml_id'],
            })
    

    _logger.info("\nAun Cargando: Patentes (Catalogo SAT)")
    aduana_codes = env['sat.patente'].create(patentes_vals_list)
    #_logger.info("\nFin de Carga Base: Patentes (Catalogo SAT)")
    if aduana_codes:
        cr.execute('''
           INSERT INTO ir_model_data (name, res_id, module, model, noupdate)
               SELECT 
                    sat_patente.xml_id,
                    sat_patente.id,
                    'l10n_mx_einvoice',
                    'sat.patente',
                    TRUE
               FROM sat_patente
               WHERE sat_patente.id IN %s
        ''', [tuple(aduana_codes.ids)])

    _logger.info("\nFin Carga: Patentes (Catalogo SAT)")
    
    
def _load_sat_patente_aduanal(cr, registry):
    """Patentes Aduanales(Catalogo SAT)"""
    _logger.info("\nCargando: Patentes Aduanales (Catalogo SAT)")
    env = api.Environment(cr, SUPERUSER_ID, {})
    csv_path = join(dirname(realpath(__file__)), 'data', 'sat.patente.aduanal.csv')
    patentes_vals_list = []
    with open(csv_path, 'r') as csv_file:
        for row in csv.DictReader(csv_file, delimiter='|', 
                                  fieldnames=['xml_id', 'code']):
            
            patentes_vals_list.append({
                'code'      : row['code'],
                'xml_id'    : row['xml_id'],
            })
    
    patente_aduanal_codes = env['sat.patente.aduanal'].create(patentes_vals_list)
    if patente_aduanal_codes:
        cr.execute('''
           INSERT INTO ir_model_data (name, res_id, module, model, noupdate)
               SELECT 
                    sat_patente_aduanal.xml_id,
                    sat_patente_aduanal.id,
                    'l10n_mx_einvoice',
                    'sat.patente.aduanal',
                    TRUE
               FROM sat_patente_aduanal
               WHERE sat_patente_aduanal.id IN %s
        ''', [tuple(patente_aduanal_codes.ids)])

    _logger.info("\nFin Carga: Patentes Aduanales (Catalogo SAT)")