# -*- encoding: utf-8 -*-
#

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import csv
import os.path
import base64

import odoo.tools as tools
from . import update_mx_data ## Clase con Mucha Informacion

import logging
_logger = logging.getLogger(__name__)

"""
class overall_config_wizard_sat_models_cfdi(models.TransientModel):
    _name = 'overall.config.wizard.sat.models.cfdi'
    _description ="Wizard para cargar los catálogos del SAT"

    load_data = fields.Boolean('Informacion Cargada')
    action_status = fields.Text('Notas de Carga de Datos')
    select_catalog = fields.Selection([
                ("all","Todos"),
                #("data/res.country.sat.code.csv" , "Paises"),
                # Eliminado "data/res.country.state.sat.code.csv" , "Estados"),
                # ("data/res.country.township.sat.code.csv" , "Municipios"),
                # ("data/res.country.locality.sat.code.csv", "Localidades"),
                # hooks ("data/res.country.zip.sat.code.csv", "Códigos Postales"),
                # hooks ("data/res.colonia.zip.sat.code.csv","Colonias"),
                # ('data/sat.aduana.csv', "Aduanas"),
                # hooks ("data/sat.producto.csv", "Productos/Servicios"),
                # ("data/sat.udm.csv", "Unidades de Medida"),
                # Se puso en data.xml ("data/sat.uso.cfdi.csv", "Usos de CFDI"),
                # hooks ("data/sat.patente.csv", "Patentes y Patentes Aduanales"),
                # Se puso en data.xml ("data/res.country.csv", "Actualización Paises Claves SAT"),
                ("data/res.country.state.csv", "Actualización Estados Claves SAT"),
                ("data/zip.sat.code", "Actualización Codigos Postales Clientes/Proveedores"),
                #("data/regimen.fiscal","Eliminar los Regimen Fiscales Antiguos"),
                ("data/colonias/01/res.colonia.zip.sat.code.csv","Catalogo de Colonias Parte 01"),
                ("data/colonias/02/res.colonia.zip.sat.code.csv","Catalogo de Colonias Parte 02"),
                ("data/colonias/03/res.colonia.zip.sat.code.csv","Catalogo de Colonias Parte 03"),
                # hooks ("data/sat.arancel.csv", "Fracciones Arancelarias (Comercio Exterior)"),
                # Se puso en data.xml ('eaccount.bank', 'Bancos Oficiales'),
                #('sat.account.code', 'Códigos Agrupadores SAT'),
                #('eaccount.currency', 'Monedas'),
                # Se puso en data.xml ('eaccount.payment.methods', 'Métodos de Pago (Contabilidad Electrónica)')
        
            ],'Selecciona el Catalogo', default="all" )

    
    def _reopen_wizard(self):
        return { 'type'     : 'ir.actions.act_window',
                 'res_id'   : self.id,
                 'view_mode': 'form',
                 'view_type': 'form',
                 'res_model': 'overall.config.wizard.sat.models.cfdi',
                 'target'   : 'new',
                 'name'     : 'Carga de Catalogos para la Facturacion CFDI 3.3'}

    
    def _find_file_in_addons(self, directory, filename):
        addons_paths = tools.config['addons_path'].split(',')
        actual_module = directory.split('/')[0]
        if len(addons_paths) == 1:
            return os.path.join(addons_paths[0], directory, filename)
        for pth in addons_paths:
            for subdir in os.listdir(pth):
                if subdir == actual_module:
                    return os.path.join(pth, directory, filename)

        return False
    
    
    def process_catalogs_eaccount(self):
        self.ensure_one()
        form = self
        user = self.env.user
        expected_col_number = 2
        orm_obj = self.env[form.select_catalog]
        #if form.select_catalog == 'eaccount.bank':
        #    target_file = self._find_file_in_addons('l10n_mx_einvoice/data', 'banks.csv')
        if form.select_catalog == 'sat.account.code':
            target_file = self._find_file_in_addons('l10n_mx_einvoice/data', 'sat_codes.csv')
        elif form.select_catalog == 'eaccount.payment.methods':
            target_file = self._find_file_in_addons('l10n_mx_einvoice/data', 'payment_methods.csv')
        elif form.select_catalog == 'eaccount.currency':
            target_file = self._find_file_in_addons('l10n_mx_einvoice/data', 'currencies.csv')
        iterable_data = open(target_file, 'r', encoding="utf-8").readlines()
        reader = csv.reader(iterable_data)
        context = {}
        #context['allow_management'] = True
        obj_fields = []
        vals = {}
        #if form.select_catalog == 'eaccount.bank':
        #    search_field = 'bic'
        if form.select_catalog == 'sat.account.code':
            search_field = 'key'
        else:
            search_field = 'code'
        for (idx, row,) in enumerate(reader):
            if len(row) < expected_col_number:
                self.write({'action_status': 'Formato inesperado. Se esperaban %s columnas, pero se encontraron %s. Linea %s' % (expected_col_number, len(row), idx + 1)})
                return True
            if idx == 0:
                obj_fields = row
                continue
            for (pos, fld,) in enumerate(obj_fields):
                vals[fld] = row[pos].zfill(3) if fld == search_field and form.select_catalog in ('eaccount.bank', 'eaccount.currency') else row[pos]

            #if form.select_catalog == 'eaccount.currency':
            #    vals['company_id'] = user.company_id.id
            stored_ids = orm_obj.search([(search_field, '=', vals[search_field])])
            if stored_ids:
                stored_ids.with_context(context).write(vals)
            else:
                res = orm_obj.with_context(context).create(vals)

        #if form.select_catalog == 'eaccount.bank':
        #    status = 'Los Bancos han sido correctamente procesados.'
        if form.select_catalog == 'sat.account.code':
            status = 'Los Códigos del SAT han sido correctamente procesados.'
        elif form.select_catalog == 'eaccount.payment.methods':
            status = 'Los métodos de pago han sido correctamente procesados.'
        elif form.select_catalog == 'eaccount.currency':
            status = 'Las monedas han sido correctamente procesadas.'
        self.write({'action_status': status})
        return self._reopen_wizard()
    

    
    def process_catalogs(self):
        # El siguiente Script Elimina los datos Cargados desde CSV o XML
        # cr.execute("delete from ir_model_data where model='sat.udm';")
        
        status = "Los Informacion se Cargo de Forma Correcta."
        if self.select_catalog in ('eaccount.bank','sat.account.code','eaccount.currency','eaccount.payment.methods'): # AQUI VAMOS ISRAEL
            _logger.info('\n***** Actualizando %s ********\n' % self.select_catalog)
            try:
                self.process_catalogs_eaccount()
                _logger.info('\n ***** %s *****\n' % self.select_catalog)
            except:
                status = "Se encontraron Errores en el Procesamiento.\nConsulte al Desarrollador: info@argil.mx"                
        elif self.select_catalog == "data/res.country.csv":
            cr = self.env.cr
            _logger.info('\n***** Actualizando los Paises ********\n')
            try:
                self.update_countrys_sat()
                _logger.info('\n ***** Paises Actualizados *****\n')
            except:
                status = "Se encontraron Errores en el Procesamiento.\nConsulte al Desarrollador: info@argil.mx"
        elif self.select_catalog == "data/res.country.state.csv":
            cr = self.env.cr
            _logger.info('\n***** Actualizando los Estados ********\n')
            try:
                self.update_countrys_states_sat()
                _logger.info('\n ***** Estados Actualizados *****\n')
            except:
                status = "Se encontraron Errores en el Procesamiento.\nConsulte al Desarrollador: info@argil.mx"
        elif self.select_catalog == "data/zip.sat.code":
            _logger.info('\n***** Actualizando los Codigos Postales ********\n')
            try:
                self.env.cr.execute("
                    update res_partner set zip_sat_id=res_country_zip_sat_code.id 
                                                        from res_country_zip_sat_code 
                                                        where res_country_zip_sat_code.code = res_partner.zip
                                                        and res_partner.zip_sat_id is null;
                    ")
                _logger.info('\n ***** Codigos Postales Actualizados *****\n')
            except:
                status = "Se encontraron Errores en el Procesamiento.\nConsulte al Desarrollador: info@argil.mx"

        #elif self.select_catalog == "data/regimen.fiscal":
        #    _logger.info('\n***** Actualizando los Regimen Fiscales ********\n')
        #    try:
        #        self.env.cr.execute("update res_partner set regimen_fiscal_id=null;")
        #        _logger.info('\n ***** Regimen Fiscales Actualizados *****\n')
        #    except:
        #        status = "Se encontraron Errores en la Ejecucion.\nConsulte al Desarrollador: info@argil.mx"
                
        #elif self.select_catalog == "data/sat.arancel.csv":
        #    _logger.info('\n***** Cargando el Fichero: %s\n' % self.select_catalog)
        #    cr = self.env.cr
        #    module_name = "l10n_mx_einvoice"
        #    mode = "update"
        #    kind = "data"
        #    noupdate = True
        #    report = ""
        #    target_file = self._find_file_in_addons('l10n_mx_einvoice', "data/sat.arancel.csv")
        #    tools.convert_file(cr, module_name, "data/sat.arancel.csv", False, mode, noupdate, kind, target_file)
        #    _logger.info('\n ***** Fichero Cargado *****\n')
            
        else:
            if self.select_catalog == "all":
                list_csv_data = [
                        'data/res.country.sat.code.csv', 
                        'data/res.country.state.sat.code.csv', 
                        'data/res.country.township.sat.code.csv', 
                        "data/res.country.locality.sat.code.csv",
                        "data/res.country.zip.sat.code.csv",
                        "data/res.colonia.zip.sat.code.csv",
                        'data/sat.aduana.csv',
                        "data/sat.producto.csv",
                        "data/sat.udm.csv",
                        # Se puso en data.xml "data/sat.uso.cfdi.csv",
                        #"data/sat.patente.csv",
                        #"data/sat.patente.aduanal.csv",
                        #"data/sat.arancel.csv",
                ]
                cr = self.env.cr
                module_name = "l10n_mx_einvoice"
                mode = "update"
                kind = "data"
                noupdate = True
                report = ""
                try:
                    for csv_file in list_csv_data:
                        _logger.info('\n***** Cargando el Fichero: %s\n' % csv_file)

                        target_file = self._find_file_in_addons('l10n_mx_einvoice', csv_file)
                        tools.convert_file(cr, module_name, csv_file, False, mode, noupdate, kind, target_file)
                        
                        _logger.info('\n ***** Fichero Cargado *****\n')
                except:
                    status = "Se encontraron Errores en el Procesamiento.\nConsulte al Desarrollador: info@argil.mx"

                ### Actualizando los Paises ###
                _logger.info('\n***** Actualizando los Paises ********')
                try:
                    self.update_countrys_sat()
                    _logger.info('\n ***** Paises ACtualizados *****\n')
                except:
                    status = "Se encontraron Errores en el Procesamiento.\nConsulte al Desarrollador: info@argil.mx"
                ### Actualizando los Estados ###
                _logger.info('\n***** Actualizando los Estados ********\n')
                try:
                    self.update_countrys_states_sat()
                    _logger.info('\n ***** Estados Actualizados *****\n')
                except:
                    status = "Se encontraron Errores en el Procesamiento.\nConsulte al Desarrollador: info@argil.mx"
                ### Actualizando los Codigos Postales ###
                _logger.info('\n***** Actualizando los Codigos Postales ********\n')
                try:
                    self.env.cr.execute("
                        update res_partner set zip_sat_id=res_country_zip_sat_code.id 
                                                            from res_country_zip_sat_code 
                                                            where res_country_zip_sat_code.code = res_partner.zip
                                                            and res_partner.zip_sat_id is null;
                        ")
                    _logger.info('\n ***** Codigos Postales Actualizados *****\n')
                except:
                    status = "Se encontraron Errores en el Procesamiento.\nConsulte al Desarrollador: info@argil.mx"

                ### Actualizando los Regimen Fiscales ###
                #_logger.info('\n***** Actualizando los Regimen Fiscales ********\n')
                #try:
                #    self.env.cr.execute("update res_partner set regimen_fiscal_id=null;")
                #    _logger.info('\n ***** Regimen Fiscales Actualizados *****\n')
                #except:
                #    status = "Se encontraron Errores en la Ejecucion.\nConsulte al Desarrollador: info@argil.mx"


            else:   
                csv_file = self.select_catalog
                cr = self.env.cr
                module_name = "l10n_mx_einvoice"
                mode = "update"
                kind = "data"
                noupdate = True
                report = ""
                dependent_list = [
                    "data/res.country.sat.code.csv",
                    "data/res.country.state.sat.code.csv",
                    "data/res.country.township.sat.code.csv",
                    "data/res.country.locality.sat.code.csv",
                    "data/res.country.zip.sat.code.csv",
                    "data/res.colonia.zip.sat.code.csv",
                    ]
                if csv_file in dependent_list:
                    index_select = dependent_list.index(csv_file)
                    csv_list_to_read = dependent_list[0:index_select+1]
                    try:
                        for csv_dep in csv_list_to_read:
                            _logger.info('\n***** Cargando el Fichero: %s\n' % csv_dep)
                            target_file = self._find_file_in_addons('l10n_mx_einvoice', csv_dep)
                            tools.convert_file(cr, module_name, csv_dep, False, mode, noupdate, kind, target_file)
                            _logger.info('\n ***** Fichero Cargado *****\n')
                    except:
                        status = "Se encontraron Errores en el Procesamiento.\nConsulte al Desarrollador: info@argil.mx"
                else:
                    if csv_file == "data/sat.patente.csv":
                        dependent_list = [
                                           "data/sat.aduana.csv",
                                           "data/sat.patente.csv",
                                           "data/sat.patente.aduanal.csv" 
                                          ]
                        try:
                            for csv_dep in dependent_list:
                                _logger.info('\n***** Cargando el Fichero: %s\n' % csv_dep)
                                target_file = self._find_file_in_addons('l10n_mx_einvoice', csv_dep)
                                tools.convert_file(cr, module_name, csv_dep, False, mode, noupdate, kind, target_file)
                        
                                _logger.info('\n ***** Fichero Cargado *****\n')
                        except:
                            status = "Se encontraron Errores en el Procesamiento.\nConsulte al Desarrollador: info@argil.mx"

                    else:
                        _logger.info('\n***** Cargando el Fichero: %s\n' % csv_file)
                        try:
                            target_file = self._find_file_in_addons('l10n_mx_einvoice', csv_file)
                            tools.convert_file(cr, module_name, csv_file, False, mode, noupdate, kind, target_file)
                            _logger.info('\n ***** Fichero Cargado *****\n')
                        except:
                            status = "Se encontraron Errores en el Procesamiento.\nConsulte al Desarrollador: info@argil.mx"

        _logger.info('\n ***** Fin de la Carga de Datos *****\n')

        self.write({'action_status': status,'load_data':True})
        return self._reopen_wizard()


    
    def update_countrys_sat(self):
        cr = self.env.cr
        instance_class_data = update_mx_data.ReturnCountryMxData()
        list_codes = instance_class_data.return_country_list()
        for code in list_codes:
            cr.execute("
                update res_country set 
                    sat_code = ( select id 
                    from res_country_sat_code where code= %s limit 1) where code=%s;

                ",(code[1],code[0]))
    
    
    def update_countrys_states_sat(self):
        cr = self.env.cr
        instance_class_data = update_mx_data.ReturnCountryMxData()
        list_codes = instance_class_data.return_states_list()
        for code in list_codes:
            cr.execute("
                update res_country_state set 
                    sat_code = ( select id 
                    from res_country_state_sat_code where code= %s limit 1) where code=%s;

                ",(code[1],code[0]))
"""
