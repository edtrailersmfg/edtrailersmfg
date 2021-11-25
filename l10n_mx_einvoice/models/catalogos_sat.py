# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _, tools
from datetime import datetime
import time
from odoo import SUPERUSER_ID
import time
import dateutil
import dateutil.parser
from dateutil.relativedelta import relativedelta
from datetime import datetime, date, timedelta
from odoo.exceptions import UserError, RedirectWarning, ValidationError
from odoo.osv import osv, expression


import logging
_logger = logging.getLogger(__name__)


msg2 = "Contacta a tu administrador de Sistema o contactanos info@argil.mx"


class pay_method(models.Model):
    _name = 'pay.method'
    _description="Métodos del Pago del SAT"

    code        = fields.Char(string='Clave SAT', required=True, index=True)
    name        = fields.Char(string='Forma de Pago', size=128, required=True, index=True)
    description = fields.Text(string='Descripción', required=True)

    bancarizado = fields.Selection(selection=[('si','Si'),
                                    ('no','No'),
                                    ('opcional','Opcional'),],
                                    string="Bancarizado", required=True, default='no')
    num_operacion = fields.Selection(selection=[('opcional','Opcional'),],
                                    string="No. Operación", required=True, default='opcional')
    
    rfc_del_emisor_cuenta_ordenante = fields.Selection(selection=[('no','No'),
                                       ('opcional','Opcional'),],
                                        string="RFC del Emisor de la Cuenta Ordenante", required=True, default='opcional')
    
    cuenta_ordenante = fields.Selection(selection=[('no','No'),
                                       ('opcional','Opcional'),],
                                        string="Cuenta Ordenante", required=True, default='opcional')
    patron_cuenta_ordenante = fields.Char(string="Patrón para Cuenta Ordenante")
    
    rfc_del_emisor_cuenta_beneficiario = fields.Selection(selection=[('no','No'),
                                                           ('opcional','Opcional'),],
                                        string="RFC del Emisor Cuenta de Beneficiario", required=True, default='opcional')
    
    cuenta_beneficiario = fields.Selection(selection=[('no','No'),
                                       ('opcional','Opcional'),],
                                        string="Cuenta Beneficiario", required=True, default='opcional')
    
    patron_cuenta_beneficiario = fields.Char(string="Patrón para Cuenta Beneficiario")
    
    
    tipo_cadena_pago = fields.Selection(selection=[('no','No'),
                                       ('opcional','Opcional'),],
                                        string="Tipo Cadena Pago", required=True, default='no')
    
    banco_emisor_obligatorio_extranjero = fields.Boolean(string="Requerir Nombre Banco Emisor",
                                                        help="Nombre del Banco emisor de la cuenta ordenante en caso de extranjero")
    
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'El nombre de la Forma de Pago debe ser único !'),
        ('code_uniq', 'unique(code)', 'La clave de la Forma de Pago debe ser único !'),
    ]    
    
    
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
            return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)

        return super(pay_method, self)._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)

        

    @api.depends('name', 'code')
    def name_get(self):
        result = []
        for x in self:
            if x.code and x.name:
                name = '[ '+x.code + ' ] ' + x.name
                result.append((x.id, name))
        return result
    

class AccountRegimenFiscal(models.Model):
    _name = 'regimen.fiscal'
    _description = 'Regimen Fiscal'
    _order = 'name'


    name        = fields.Char(string='Regimen Fiscal', size=128, required=True)
    description = fields.Text('Descripcion')


###### PAISES #########
"""
class ResCountrySatCode(models.Model):
    _name = 'res.country.sat.code'
    _description = 'Codigos de Paises del SAT'

    
    code = fields.Char('Codigo', size=64, required=True)
    name = fields.Char('Pais', required=True)

    formato_cp      = fields.Char(string="Formato Código Postal")
    formato_registro_tributario = fields.Char(string="Formato Registro Tributario")
    validacion_registro_tributario = fields.Char(string="Validación del Registro de Identidad Tributaria")
    agrupaciones    = fields.Selection(selection=[('tlcan','TLCAN'),
                                        ('ue','Unión Europea')],
                                        string="Agrupaciones")
    _sql_constraints = [
        ('code_unique', 'unique(code)',
         'El Código debe ser único')]    

    
    @api.depends('code', 'name')
    def name_get(self):
        result = []
        for rec in self:
            if rec.name and rec.code:
                name = "[ "+rec.code+"] "+rec.name
                result.append((rec.id, name))
        return result

    
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
            return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)

        return super(ResCountrySatCode, self)._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)
"""
    
class res_country(models.Model):
    _inherit = 'res.country'

    
    sat_code = fields.Char('Código SAT CE',
                          help="Código SAT para Comercio Exterior")
    #fields.Many2one('res.country.sat.code', 'Codigo SAT CE', help='Codigo del PAIS para Comercio Exterior', )
    
    """
    @api.depends('sat_code', 'name')
    def name_get(self):
        result = []
        for rec in self:
            if rec.name and rec.code:
                code = rec.sat_code.code if rec.sat_code else rec.code
                name = "[ "+code+" ] "+rec.name
                result.append((rec.id, name))
        return result
    """
    
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
            return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)

        return super(res_country, self)._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)

###### ESTADOS #########
"""
class ResCountryStateSatCode(models.Model):
    _name = 'res.country.state.sat.code'
    _description = 'Codigos de Estados de la Rep. Mexicana del SAT'

    code = fields.Char('Codigo', size=64, required=True)
    name = fields.Char('Nombre Estado', required=True)
    country_sat_code = fields.Many2one('res.country.sat.code', 'Codigo Pais SAT', required=True)

    
    @api.depends('code', 'name')
    def name_get(self):
        result = []
        for rec in self:
            if rec.name and rec.code:
                code = rec.code
                name = "[ "+code+" ] "+rec.name
                result.append((rec.id, name))
        return result

    
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
            return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)

        return super(ResCountryStateSatCode, self)._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)


class ResCountryState(models.Model):
    _inherit = 'res.country.state'

    sat_code = fields.Many2one('res.country.state.sat.code', 'Codigo SAT CE', 
                               help='Codigo del Estado para Comercio Exterior', )

    @api.onchange('sat_code','country_id')
    def onchange_domain_sat_list(self):
        domain = {}
        if self.country_id:
            state_sat_obj = self.env['res.country.state.sat.code']
            states_ids = state_sat_obj.search([('country_sat_code.code','=',self.country_id.sat_code.code)])
            if states_ids:
                domain.update(
                    {
                        'sat_code':[('id','in',[x.id for x in states_ids])]
                    })

        if self.sat_code:
            country_sat_obj = self.env['res.country']
            country_ids = country_sat_obj.search([('sat_code.code','=',self.sat_code.country_sat_code.code)])
            if country_ids:
                domain.update(
                    {
                        'country_id':[('id','in',[x.id for x in country_ids])]
                    })

        if not self.country_id and not self.sat_code:
            state_sat_obj = self.env['res.country.state.sat.code']
            states_ids = state_sat_obj.search([])
            country_sat_obj = self.env['res.country']
            country_ids = country_sat_obj.search([])
            domain.update(
                    {
                        'sat_code':[('id','in',[x.id for x in states_ids])],
                        'country_id':[('id','in',[x.id for x in country_ids])]
                    })

        return {'domain': domain}
"""
###### MUNICIPIOS #########

class ResCountryTownshipSatCode(models.Model):
    _name = 'res.country.township.sat.code'
    _description = 'Codigos de Municipios del SAT'

    code = fields.Char('Codigo', size=64, index=True)
    name = fields.Char('Nombre Municipio', index=True)
    state_sat_code = fields.Many2one('res.country.state', 'Estado/Provincia', index=True)

    
    @api.depends('code', 'name')
    def name_get(self):
        result = []
        for rec in self:
            if rec.name and rec.code:
                code = rec.code
                name = "[%s] %s" % (rec.code, rec.name)
                result.append((rec.id, name))
        return result

    
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
            return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)

        return super(ResCountryTownshipSatCode, self)._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)

###### Localidades #########

class ResCountryLocalitySatCode(models.Model):
    _name = 'res.country.locality.sat.code'
    _description = 'Codigos de Localidades del SAT'

    code = fields.Char('Codigo', size=64, index=True)
    name = fields.Char('Nombre Localidad', index=True)
    state_sat_code = fields.Many2one('res.country.state', 'Estado/Provincia', index=True)

    
    @api.depends('code', 'name')
    def name_get(self):
        result = []
        for rec in self:
            if rec.name and rec.code:
                code = rec.code
                name = "[ "+code+" ] "+rec.name
                result.append((rec.id, name))
        return result

    
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
            return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)

        return super(ResCountryLocalitySatCode, self)._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)

###### Codigos Postales #########

class ResCountryZipSatCode(models.Model):
    _name = 'res.country.zip.sat.code'
    _description = 'Codigos de Codigos Postales del SAT'
    _rec_name = 'code'
    _order = 'code'


    code = fields.Char(string='Codigo', size=64, index=True)
    state_sat_code = fields.Many2one('res.country.state', string='Estado/Provincia', index=True)
    township_sat_code = fields.Many2one('res.country.township.sat.code', string='Codigo Municipio SAT', index=True)
    locality_sat_code = fields.Many2one('res.country.locality.sat.code', string='Codigo Localidad SAT', index=True)

    state_sat_code_char = fields.Char(string='Codigo Estado SAT (CADENA)', size=128)
    township_sat_code_char = fields.Char(string='Codigo Municipio SAT (CADENA)', size=128)
    locality_sat_code_char = fields.Char(string='Codigo Localidad SAT (CADENA)', size=128)
    
    xml_id = fields.Char('XML ID', help="Dummy, se usa para cargar los datos mas rapido a la BD")

    
    
    @api.depends('code', 'locality_sat_code', 'state_sat_code', 'township_sat_code')
    def name_get(self):
        result = []
        for rec in self:
            if rec.code:
                """
                code = rec.code
                complete_name = ""
                if rec.locality_sat_code:
                    state_sat_code = rec.state_sat_code.name if rec.state_sat_code else ""
                    township_sat_code = rec.township_sat_code.name if rec.township_sat_code else ""
                    locality_sat_code = rec.locality_sat_code.name if rec.locality_sat_code else ""
                    complete_name = "[ "+str(rec.code)+" ] "+str(locality_sat_code or "")+", "+str(township_sat_code or "")+", "+str(state_sat_code or "")
                else:
                    state_sat_code = rec.state_sat_code.name if rec.state_sat_code else ""
                    township_sat_code = rec.township_sat_code.name if rec.township_sat_code else ""
                    complete_name = "[ "+str(rec.code)+" ] "+str(township_sat_code or "")+", "+str(state_sat_code or "")
                """
                complete_name = "%s%s%s" % ((rec.township_sat_code and (rec.township_sat_code.name + ', ') or ''),
                                            (rec.state_sat_code and (rec.state_sat_code.name + ' ') or ''),
                                            rec.code)
                result.append((rec.id, complete_name))
        return result

   
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = [('code', '=ilike', name.split(' ')[0] + '%')]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
            return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)

        return super(ResCountryZipSatCode, self)._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)

###### Codigos Postales #########

class ResColoniaZipSatCode(models.Model):
    _name = 'res.colonia.zip.sat.code'
    _description = 'Codigos de Codigos colonias del SAT'
    _order = 'zip_sat_code, name'
    
    name = fields.Char('Nombre Colonia', size=256, index=True)    
    code = fields.Char('Codigo', size=64, index=True)
    zip_sat_code = fields.Many2one('res.country.zip.sat.code', 'Codigo Postal SAT', index=True)
    
    zip_sat_code_char = fields.Char('Codigo Colonia SAT (CHAR)', size=64, index=True)
    xml_id = fields.Char('XML ID', help="Dummy, se usa para cargar los datos mas rapido a la BD")
    
    @api.depends('code', 'name', 'zip_sat_code')
    def name_get_bkp(self):
        result = []
        for rec in self:
            if rec.name:# and rec.code and rec.zip_sat_code:
                name = str(rec.name or "") #+ "[ CP: "+str(rec.zip_sat_code.code if rec.zip_sat_code else "") + " Cod: " +str(rec.code)+" ]"
                result.append((rec.id, name))
            """    
            else:
                
                if not rec.zip_sat_code:
                    name = str(rec.name or "") + "[ Cod: "+str(rec.code)+" ]"
                    result.append((rec.id, name))
                else:
                    name = rec.name
                    result.append((rec.id, name))
            """

        return result

    
    @api.model
    def _name_search_bkp(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
            return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)

        return super(ResColoniaZipSatCode, self)._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)


######## Aduanas ################

###### Aduanas - c_Aduana ######
class SATAduana(models.Model):
    _name = "sat.aduana"
    _description = "Catálogo de Aduanas del SAT"
    
    
    code = fields.Char(string="Clave Aduana", size=64, required=True, index=True)
    name = fields.Char(string="Descripción", required=True, index=True)
    
    _sql_constraints = [
        ('code_unique', 'unique(code)',
         'El Código debe ser único')]
    
    
    @api.depends('name', 'code')
    def name_get(self):
        result = []
        for rec in self:
            if rec.code and rec.name:
                name = '[ '+rec.code+' ]' + ' ' + rec.name
                result.append((rec.id, name))
        return result

    
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
            return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)

        return super(SATAduana, self)._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)

###### Codigos Productos y Servicios ######

class SATProducto(models.Model):
    _name = "sat.producto"
    _description = "Catálogo de Productos del SAT"
    
    code = fields.Char(string="Código", size=8, required=True, index=True)
    name = fields.Char(string="Descripción", required=True, index=True)
    vigencia_inicio = fields.Date(string="Vigencia Inicio", required=True, default='2016-10-01')
    vigencia_fin    = fields.Date(string="Vigencia Fin")
    incluir_iva_trasladado = fields.Selection(selection=[('si', 'Si'),
                                               ('opcional', 'Opcional')],
                                              string="Incluir IVA Trasladado", required=True, default='opcional')
    incluir_ieps_trasladado = fields.Selection(selection=[('no', 'No'),
                                               ('opcional', 'Opcional')],
                                              string="Incluir IEPS Trasladado", required=True, default='opcional')
    
    incluye_complemento = fields.Boolean('Incluye Complemento')
    complemento_que_debe_incluir = fields.Char(string="Complemento")
    vigencia_inicio = fields.Date(string="Vigencia Inicio", required=False, default='2019-01-07')
    vigencia_fin    = fields.Date(string="Vigencia Fin", required=False)
    estimulo_franja_fronteriza = fields.Selection(selection=[('1', 'Si'),
                                                   ('0', 'No'),],
                                              string="Estimulo Franja Fonteriza", required=True, default='0')
    palabras_similares = fields.Char(string="Palabras similares", required=False, index=True)
    
    
    _sql_constraints = [
        ('code_unique', 'unique(code)',
         'El Código debe ser único')]
    
    
    @api.depends('name', 'code')
    def name_get(self):
        result = []
        for rec in self:
            if rec.name and rec.code:
                name = '[ '+rec.code+' ]' + ' ' + rec.name
                result.append((rec.id, name))
        return result

    
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
            return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)

        return super(SATProducto, self)._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)

    
###### Unidades de Medida ######
class SATUdM(models.Model):
    _name = "sat.udm"
    _description = "Unidades de Medida del SAT"
    
    code            = fields.Char(string="Código", size=4, required=True, index=True)
    name            = fields.Char(string="Unidad de Medida", required=True, index=True)
    description     = fields.Text(string="Descripción")
    vigencia_inicio = fields.Date(string="Vigencia Inicio", required=False, default='2016-10-01')
    vigencia_fin    = fields.Date(string="Vigencia Fin", required=False)
    symbol          = fields.Char(string="Símbolo")
    notes           = fields.Text('Notas')
    
    _sql_constraints = [
        ('code_unique', 'unique(code)',
         'El Código debe ser único')]
    
    
    @api.depends('name', 'code')
    def name_get(self):
        result = []
        for rec in self:
            if rec.code and rec.name:
                name = '[ '+rec.code+' ]' + ' ' + rec.name
                result.append((rec.id, name))
        return result

    
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
            return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)

        return super(SATUdM, self)._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)


###### Impuestos ######
class SATImpuesto(models.Model):
    _name = "sat.impuesto"
    _description = "Catálogos de Impuestos del SAT"
    
    code            = fields.Char(string="Código", size=10, required=True, index=True)
    name            = fields.Char(string="Impuesto", required=True, index=True)
    retencion       = fields.Boolean(string="Retención", required=True, default=True)
    traslado        = fields.Boolean(string="Traslado", required=True, default=True)
    tipo            = fields.Selection(selection=[('federal','Federal'),
                                        ('local','Local')],
                                        string="Tipo", help="Aplicación de Impuesto, puede ser Federal o Local")
    entidades_donde_aplica = fields.Many2many("res.country.state",string="Entidades donde Aplica")
    
    
    _sql_constraints = [
        ('code_unique', 'unique(code)',
         'El Código debe ser único')]
    
    
    @api.depends('name', 'code')
    def name_get(self):
        result = []
        for rec in self:
            if rec.name and rec.code:
                name = '[ '+rec.code+' ]' + ' ' + rec.name
                result.append((rec.id, name))
        return result

    
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
            return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)

        return super(SATImpuesto, self)._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)


        
###### Metodos de Pago ######
class SATMetodoPago(models.Model):
    _name = "sat.metodo.pago"
    _description = "Métodos de Pago del SAT"
    
    code            = fields.Char(string="Código", size=10, required=True, index=True)
    name            = fields.Char(string="Método de Pago", required=True, index=True)
    
    
    _sql_constraints = [
        ('code_unique', 'unique(code)',
         'El Código debe ser único')]
    
    
    @api.depends('name', 'code')
    def name_get(self):
        result = []
        for rec in self:
            if rec.name and rec.code:
                name = '[ '+rec.code+' ]' + ' ' + rec.name
                result.append((rec.id, name))
        return result

    
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
            return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)

        return super(SATMetodoPago, self)._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)

"""    
###### Pedimentos Aduanales - c_NumPedimentoAduana ######
class SATPatente(models.Model):
    _name = "sat.patente"    
    _description = "Catálogo de Patentes del SAT"
    
    aduana_id       = fields.Many2one('sat.aduana', string="Aduana", required=False, index=True)
    name            = fields.Char(string="Patente", required=True, index=True)
    ejercicio       = fields.Char(string="Ejercicio", required=False, size=4)
    cantidad        = fields.Char(string="Cantidad", required=False, size=6,
                                 help="Solo se pueden usar 6 caracteres numéricos, por ejemplo: 003000")
    
    start_date      = fields.Date('Inicio Vigencia', required=False, default="2017-01-01")
    end_date      = fields.Date('Fin Vigencia', required=False)

    aduana_char            = fields.Char(string="Codigo Aduana", required=False)
    xml_id = fields.Char('XML ID', help="Dummy, se usa para cargar los datos mas rapido a la BD")


###### Pedimentos Aduanales ######
class SATPatenteAduanal(models.Model):
    _name = "sat.patente.aduanal"
    _description = "Catálogo de Patente Aduanal del SAT"
    _rec_name = 'code' 

    code      = fields.Char("Código Patente Aduanal", required=True, size=128 )
    name            = fields.Char('Patente Aduanal', size=128)
    # patente_id      = fields.Many2one('sat.patente', string="Patente Aduanal", required=True )
    vigencia_inicio = fields.Date(string="Vigencia Inicio", required=False, default="2000-01-01")
    vigencia_fin    = fields.Date(string="Vigencia Fin", required=False)
    xml_id    = fields.Char('XML ID', help="Dummy, se usa para cargar los datos mas rapido a la BD")
"""

###### Regimen Fiscal ######


class SATRegimenFiscal(models.Model):
    _name = 'sat.regimen.fiscal'
    _description = 'Regimen Fiscal'


    code        = fields.Char(string="Código", size=10, required=True, index=True)
    name        = fields.Char(string='Regimen Fiscal', required=True)
    aplica_persona_fisica = fields.Boolean(string="Aplica Persona Física", default=False, required=True)
    aplica_persona_moral  = fields.Boolean(string="Aplica Persona Moral", default=False, required=True)
    
    _sql_constraints = [
        ('code_unique', 'unique(code)',
         'El Código debe ser único')]
    
    
    @api.depends('name', 'code')
    def name_get(self):
        result = []
        for rec in self:
            if rec.name and rec.code:
                name = '[ '+rec.code+' ]' + ' ' + rec.name
                result.append((rec.id, name))
        return result

    
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
            return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)

        return super(SATRegimenFiscal, self)._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)


###### Uso de CFDI ######
class SATUsoCfdi(models.Model):
    _name = 'sat.uso.cfdi'
    _description = 'Catálogo de Usos de CFDI del SAT'
    _order = 'code'

    code        = fields.Char(string="Código", size=10, required=True, index=True)
    name        = fields.Char(string='Descripción', required=True)
    aplica_persona_fisica = fields.Boolean(string="Aplica Persona Física", default=False, required=True)
    aplica_persona_moral  = fields.Boolean(string="Aplica Persona Moral", default=False, required=True)
    
    _sql_constraints = [
        ('code_unique', 'unique(code)',
         'El Código debe ser único')]
    
    
    @api.depends('name', 'code')
    def name_get(self):
        result = []
        for rec in self:
            if rec.name and rec.code:
                name = '[ '+rec.code+' ]' + ' ' + rec.name
                result.append((rec.id, name))
        return result

    
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
            return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)

        return super(SATUsoCfdi, self)._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)

###### Tipo de Comprobante ######
class SATTipoCombroante(models.Model):
    _name = 'sat.tipo.comprobante'
    _description = 'Tipo de Comprobante'

    code        = fields.Char(string="Código", size=10, required=True, index=True)
    name        = fields.Char(string='Descripción', required=True)
    
    _sql_constraints = [
        ('code_unique', 'unique(code)',
         'El Código debe ser único')]

    
    @api.depends('name', 'code')
    def name_get(self):
        result = []
        for rec in self:
            if rec.name and rec.code:
                name = '[ '+rec.code+' ]' + ' ' + rec.name
                result.append((rec.id, name))
        return result

    
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
            return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)

        return super(SATTipoCombroante, self)._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)


###### Tipo de Comprobante ######
class SATCfdiRelacionado(models.Model):
    _name = 'sat.tipo.relacion.cfdi'
    _description = 'Tipo de Relacion CFDI'
    _order = 'code'

    code        = fields.Char(string="Código", size=10, required=True, index=True)
    name        = fields.Char(string='Descripción', required=True)
    
    _sql_constraints = [
        ('code_unique', 'unique(code)',
         'El Código debe ser único')]
        
    
    @api.depends('name', 'code')
    def name_get(self):
        result = []
        for rec in self:
            if rec.name and rec.code:
                name = '[ '+rec.code+' ]' + ' ' + rec.name
                result.append((rec.id, name))
        return result

    
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
            return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)

        return super(SATCfdiRelacionado, self)._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)


    
    
###### Fracción Arancelaria - c_FraccionArancelaria ######
class SATFraccionArancelaria(models.Model):
    _name = "sat.arancel"
    _description = "Aranceles del SAT"
    
    
    code = fields.Char(string="Clave", size=64, required=True, index=True)
    name = fields.Char(string="Descripción", required=True, index=True)
    vigencia_inicio = fields.Date(string="Vigencia Inicio", required=True, default='2016-10-01')
    vigencia_fin    = fields.Date(string="Vigencia Fin")
    criterio        = fields.Selection(selection=[('na','No Aplica'),
                                       ('porcentual','Porcentual'),
                                       ('especifica','Específica'),
                                       ('azucaroso', 'Contenido Azucaroso')],
                                     string="Criterio", default='na')
    unidad_de_medida= fields.Selection(selection=[('01','KILO'),  
                                        ('02','GRAMO'  ),
                                        ('03','METRO LINEAL'),
                                        ('04','METRO CUADRADO'),
                                        ('05','METRO CUBICO'),
                                        ('06','PIEZA'),
                                        ('07','CABEZA'),
                                        ('08','LITRO'),
                                        ('09','PAR'),
                                        ('10','KILOWATT'),
                                        ('11','MILLAR'),
                                        ('12','JUEGO'),
                                        ('13','KILOWATT/HORA'),
                                        ('14','TONELADA'),
                                        ('15','BARRIL'),
                                        ('16','GRAMO NETO'),
                                        ('17','DECENAS'),
                                        ('18','CIENTOS'),
                                        ('19','DOCENAS'),
                                        ('20','CAJA'),
                                        ('21','BOTELLA'),
                                        ('99','SERVICIO')],
                                      string='Unidad de Medida')
    impuesto_importacion = fields.Char(string="Impuesto Importación")
    impuesto_exportacion = fields.Char(string="Impuesto Exportación")
    
    _sql_constraints = [
        ('code_unique', 'unique(code)',
         'El Código debe ser único')]
    
    
    @api.depends('name', 'code')
    def name_get(self):
        result = []
        for rec in self:
            if rec.code and rec.name:
                name = '[ '+rec.code+' ]' + ' ' + rec.name
                result.append((rec.id, name))
        return result

    
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
            return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)

        return super(SATFraccionArancelaria, self)._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)

    
######### Catalogos de Contabilidad Electronica

class account_banks(models.Model):
    _name = 'eaccount.bank'
    _description = "Catalogo de Bancos del SAT"
    
    name = fields.Char(string='Razón social', size=250, required=True, index=True)
    code = fields.Char(string='Nombre corto', size=250, required=True, index=True)
    bic  = fields.Char(string='Clave', size=11, required=True, index=True)

    
    def name_get(self):
        res = []
        for el in self:
            res.append((el.id, '[' + el.bic + '] ' + el.code))
        return res

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
            return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)

        return super(account_banks, self)._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)


class res_bank_sat(models.Model):
    _inherit = 'res.bank'
    
    sat_bank_id = fields.Many2one('eaccount.bank', string='Código del SAT', required=False, ondelete="restrict")

    
class res_currency_fit(models.Model):
    _name = 'eaccount.currency'
    _description = "Catalogo de Monedas del SAT"

    code            = fields.Char(string="Código", size=10, required=True, index=True)
    name            = fields.Char(string="Descripción", required=True)
    decimales       = fields.Integer(string="Decimales", default=2, required=True)
    porcentaje_variacion = fields.Float(string="Porcentaje de Variación", default=35.00, required=True,
                                       help="Usar valores entre 0 y 100 con 2 puntos decimales")
    
    
    _sql_constraints = [
        ('code_unique', 'unique(code)',
         'El Código debe ser único')]
    
    
    @api.depends('name', 'code')
    def name_get(self):
        result = []
        for rec in self:
            if rec.name and rec.code:
                name = '[ '+rec.code+' ]' + ' ' + rec.name
                result.append((rec.id, name))
        return result

    
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
            return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)

        return super(res_currency_fit, self)._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)


class res_currency_sat(models.Model):
    _inherit = 'res.currency'
    
    sat_currency_id = fields.Many2one('eaccount.currency', string='Código del SAT', required=False)
    

class sat_account_code(models.Model):
    _name = 'sat.account.code'
    _description = 'Código agrupador de SAT para las cuentas'

    key  = fields.Char(string='Código Agrupador', size=10, required=True, index=True)
    name = fields.Char(string='Descripción', size=250, required=True, index=True)
    

    
    @api.depends('name', 'key')
    def name_get(self):
        result = []
        for rec in self:
            name = '[' + rec.key + '] ' + rec.name
            result.append((rec.id, name))
        return result

    
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('key', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
            return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)

        return super(sat_account_code, self)._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)

    
class eaccount_payment_methods(models.Model):
    _name = 'eaccount.payment.methods'
    _description = 'Metodos de pago para Contabilidad Eletronica'
    
    code = fields.Char(string='Código', size=2, required=True)
    name = fields.Char(string='Método de Pago', size=150, required=True)


    @api.depends('name', 'code')
    def name_get(self):
        result = []
        for rec in self:
            name = rec.code + ' ' + rec.name
            result.append((rec.id, name))
        return result
    
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
            return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)

        return super(eaccount_payment_methods, self)._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)
