# -*- encoding: utf-8 -*-
#

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError, ValidationError
from base64 import b64decode as b64dec, b64encode as b64enc

from lxml import etree as et
from zipfile import ZipFile
import time
import os
import zipfile
import tempfile
import re
import logging
_logger = logging.getLogger(__name__)

from M2Crypto import RSA, X509
from M2Crypto.EVP import MessageDigest
_RFC_PATTERN = re.compile('[A-Z\xc3\x91&]{3,4}[0-9]{2}[0-1][0-9][0-3][0-9][A-Z0-9]?[A-Z0-9]?[0-9A-Z]?')
_SERIES_PATTERN = re.compile('[A-Z]+')
_UUID_PATTERN = re.compile('[a-f0-9A-F]{8}-[a-f0-9A-F]{4}-[a-f0-9A-F]{4}-[a-f0-9A-F]{4}-[a-f0-9A-F]{12}')

class files_generator_wizard(models.TransientModel):
    _name = 'files.generator.wizard'
    _description ="Wizard para generar los archivos XML de Contab. Electr."
    
    filename    = fields.Char(string='Archivo', size=128)
    primary_file= fields.Binary(string='Archivo Plano')
    stamped_file= fields.Binary(string='Archivo Sellado')
    zipped_file = fields.Binary(string='Archivo Zipped')
    format      = fields.Selection([('xml', 'XML'), ('pdf', 'PDF')], string='Formato del archivo', 
                                    required=True, default='xml')
    xml_target  = fields.Selection([
                                    ('accounts_catalog', 'Catálogo de cuentas'),
                                    ('trial_balance', 'Balanza de comprobación'),
                                    ('vouchers', 'Información de pólizas'),
                                    ('helpers', 'Auxiliar de folios')], 
                                    string='Archivo a generar', required=True, default='accounts_catalog')
    state  = fields.Selection([('init', 'Init'),
                               ('val_xcpt', 'Val Except'),
                               ('val_done', 'Val Done'),
                               ('stamp_xcpt', 'Stamp Except'),
                               ('stamp_done', 'Stamp Done'),
                               ('zip_done', 'Zip done')], string='State', default='init')
    month  = fields.Selection([('01', 'Enero'),
                               ('02', 'Febrero'),
                               ('03', 'Marzo'),
                               ('04', 'Abril'),
                               ('05', 'Mayo'),
                               ('06', 'Junio'),
                               ('07', 'Julio'),
                               ('08', 'Agosto'),
                               ('09', 'Septiembre'),
                               ('10', 'Octubre'),
                               ('11', 'Noviembre'),
                               ('12', 'Diciembre'),
                               ('13', '-- Cierre --')], string='Periodo', required=True)
    trial_delivery  = fields.Selection([('N', 'Normal'), ('C', 'Complementaria')], 
                                       string='Tipo de envío', required=True, default='N')
    trial_lastchange_date = fields.Date('Última modificación contable')
    request_type  = fields.Selection([('AF', 'Acto de fiscalización'),
                                      ('FC', 'Fiscalización compulsa'),
                                      ('DE', 'Devolución'),
                                      ('CO', 'Compensación')], string='Tipo de solicitud',  default=lambda *a: 'DE')
                                     #,attrs={'required': [('xml_target', '=', 'vouchers')]})
    order_number    = fields.Char(string='N\xc3\xbamero de orden', size=13)
    procedure_number= fields.Char(string='N\xc3\xbamero de trámite', size=14) # Cambio Contabilidad 1.3
    year            = fields.Integer(string='Ejercicio', required=True, default=lambda *a: int(time.strftime('%Y')))
    accounts_chart  = fields.Many2one('account.account', string='Plan contable', domain=[('parent_id', '=', False)])
    

    _XSI_DECLARATION = 'http://www.w3.org/2001/XMLSchema-instance'
    _SAT_NS = {'xsi': _XSI_DECLARATION}

    # Contabilidad 1.3

    _ACCOUNTS_CATALOG_URI = 'http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/CatalogoCuentas'
    _TRIAL_BALANCE_URI = 'http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/BalanzaComprobacion'
    _VOUCHERS_URI = 'http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/PolizasPeriodo'
    _HELPERS_URI = 'http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/AuxiliarFolios'
   
    # FIN #

    _LETTER_PERIODS = {'01': 'Enero / ',
     '02': 'Febrero / ',
     '03': 'Marzo / ',
     '04': 'Abril / ',
     '05': 'Mayo / ',
     '06': 'Junio / ',
     '07': 'Julio / ',
     '08': 'Agosto / ',
     '09': 'Septiembre / ',
     '10': 'Octubre / ',
     '11': 'Noviembre / ',
     '12': 'Diciembre / '}


    def _outputXml(self, output):
        return et.tostring(output, pretty_print=True, xml_declaration=True, encoding='UTF-8')


    def _reopen_wizard(self, res_id):
        return {'type'      : 'ir.actions.act_window',
                'res_id'    : res_id,
                'view_mode' : 'form',
                'view_type' : 'form',
                'res_model' : 'files.generator.wizard',
                'target'    : 'new',
                'name'      : 'Contabilidad electrónica'}



    def _xml_from_dict(self, node, namespaces, nsuri, parent = None):
        """
         Recursively builds an XML tree from a two elements tuple passed in the 'content' parameter.
        Consider that this method is prepared only to generate nodes, attributes and content in the
        form of child nodes; moreover, all the elements will be qualified using the specified nsuri
        and prefix. 
         Each element of that list represents a node or set of nodes that will be created. Each tuple
        contains two positions: 
        Position 0: tag of a new element to be created or the key word 'unroot' to indicate that no
                    new element is needed.
        Position 1: value for the element. This can either be a list of tuples or any other object. When
                    a list is found, content for the element will be created from it using recursive
                    calls to this method. When any other type is found, an attribute for the element 
                    will be created; if a string value is passed then the attribute is appended as-is,
                    otherwise a new string is created from the value and then used to append a new
                    attribute.
              
        Consider the following lines of code
        
        data = [
                ('root', [('at', 'val'), ('at1', 12),
                          ('el', [('at0', True), 
                                  ('subel0', [('at0', 'val0'), ('at01', 34.987)]),
                                  ('subel1', [('at1', -123), ('unroot', [
                                                                         ('child', [('at', 'val')])
                                                                        ]
                                                            )
                                            ]
                                )
                                ]
                          ),
                          ('el1', [('subel11', [('at0', False)])
                                   ('subel12', [
                                                ('child', [('at', 'val')])
                                               ])]
                          )
                        ]
                 )
            ]
                
        Applying the rules outlined above, the resulting XML generated by this method is
        
        <?xml version="1.0" coding="UTF-8"?>
            <root at="val" at1="12">
                <el at0="True">
                    <subel0 at0="val0" at01="34.987"/>
                    <subel1 at1="-123">
                        <child at="val"/>
                    </subel1>
                </el>
                <el1>
                    <subel11 at0="False"/>
                    <subel12>
                        <child1 at1="val1"/>
                    </subel12>
                </el1>
            </root>
        
        """
        attrs = {}
        for elm in node[1]:
            if isinstance(elm[1], list):
                continue
            if type(elm[1]) == str:
                attrs.update({elm[0]:elm[1]})
            else:
                attrs.update({elm[0]:str(elm[1])})
            
        #attrs.update({elm[0]:elm[1] if type(elm and elm[1]) in (str) else str(elm[1]) for elm in node[1] if not isinstance(elm[1], list)})
        children = [ elm for elm in node[1] if isinstance(elm[1], list) ]
        currNode = et.Element('{' + nsuri + '}' + node[0], attrib=attrs, nsmap=namespaces) if node[0] != 'unroot' else parent
        for chl in children:
            child = self._xml_from_dict(chl, namespaces, nsuri, currNode)
            if child is not currNode:
                currNode.append(child)

        return currNode



    def _validate_xml(self, schema, xmlTree, filename):
        validationResult = 'val_done'
        schema_path = self._find_file_in_addons('asti_eaccounting_mx_base/sat_xsd', schema)
        try:
            schema_file = open(schema_path, 'r')
        except IOError:
            raise UserError(_('Esquema XSD no encontrado\n\nEl esquema de validación del SAT no fue encontrado en la ruta "%s"') % schema_path[0:schema_path.find(schema)])
        schemaXml = et.parse(schema_file)
        try:
            schema = et.XMLSchema(schemaXml)
        except et.XMLSchemaParseError:
            if 'accounts_catalog' in schema_path:
                newLocation = schema_path.replace('accounts_catalog', 'complex_types')
            elif 'vouchers' in schema_path:
                newLocation = schema_path.replace('vouchers', 'complex_types')
            else:
                newLocation = schema_path.replace('helpers', 'complex_types')
            schemaXml.find('{http://www.w3.org/2001/XMLSchema}import').attrib['schemaLocation'] = newLocation
            try:
                schema = et.XMLSchema(schemaXml)
                validationResult = 'val_xcpt'
            except:
                schema = None
        if schema is None:
            raise UserError(_('Error al cargar esquema de validación\n\nPor favor realize nuevamente el procesamiento del archivo.'))
        try:
            schema.assertValid(xmlTree)
            return validationResult
        except et.DocumentInvalid as ex:
            error_haul = u'Los siguientes errores fueron encontrados:\n\n'
            error_haul += u'\n'.join([ u'Línea: %s\nTipo: %s\nMensaje: %s\n**********' % (err.line, err.type_name, err.message) for err in ex.error_log ])
            xsdhandler_id = self.env['xsdvalidation.handler.wizard'].create({
                                'error_file': b64enc(error_haul.encode('UTF-8')),
                                'error_filename': 'errores.txt',
                                'sample_xml': b64enc(self._outputXml(xmlTree)),
                                'sample_xmlname': filename})
            return {'type'      : 'ir.actions.act_window',
                    'res_model' : 'xsdvalidation.handler.wizard',
                    'res_id'    : xsdhandler_id.id,
                    'view_mode' : 'form',
                    'view_type' : 'form',
                    'target'    : 'new',
                    'name'      : 'La validación del archivo generado falló.'
                   }



    def _find_file_in_addons(self, directory, filename):
        """To use this method, specify a filename and the directory where it resides.
        Said directory must be at the first level for the modules folders."""
        addons_paths = tools.config['addons_path'].split(',')
        actual_module = directory.split('/')[0]
        if len(addons_paths) == 1:
            return os.path.join(addons_paths[0], directory, filename)
        for pth in addons_paths:
            for subdir in os.listdir(pth):
                if subdir == actual_module:
                    return os.path.join(pth, directory, filename)


        return False


    def process_file(self, account_ids = None, balance_ids = None, moveIds = None):
        self.ensure_one()
        form = self
        user = self.env.user
        if len(user.company_id.partner_id.vat) < 12 or len(user.company_id.partner_id.vat) > 13 or not _RFC_PATTERN.match(user.company_id.partner_id.vat):
            raise UserError(_('Datos de compañia erróneos\n\nEl RFC "%s" no es válido con respecto a los lineamientos del SAT.') % (user.company_id.partner_id.vat))
        if form.year < 2015:
            raise UserError(_('Fecha fuera de rango\n\nLa contabilidad electrónica comienza a reportarse a partir del 2015.'))
        if not user.company_id.partner_id.vat:
            raise UserError(_('Información faltante\n\nNo se ha configurado un R.F.C. para la empresa'))
        periodObj = self.env['account.period']
        period_id = periodObj.search([('name', '=', form.month + '/' + str(form.year)), ('company_id', '=', user.company_id.id)], limit=1)
        if not period_id:
            raise UserError(_('Información faltante\n\nEl periodo especificado no fue encontrado. Compruebe que los códigos de sus periodos fiscales tienen el formato "mm/aaaa"'))        
        if form.xml_target == 'accounts_catalog':
            catCtas_wizard_obj = self.env['catalogo.cuentas.wizard']
            catCtas_wizard = catCtas_wizard_obj.create({'chart_account_id': form.accounts_chart.id})
            account_ids = catCtas_wizard.get_info()
            if form.format == 'pdf':
                #raise UserError(_('Pendiente\n\nAun no esta disponible')
                return self.env.ref('asti_eaccounting_mx_base.action_report_catalogo_cuentas_sat').report_action(account_ids)
                return self.env['report'].get_action(account_ids, 'asti_eaccounting_mx_base.action_report_catalogo_cuentas_sat')
            ctas = []
            for acc in account_ids:
                if acc.sat_account_code and acc.account_id.first_period_id.date_start <= period_id.date_start:
                    ctaAttrs = [ ('CodAgrup', acc.sat_account_code),
                                 ('NumCta', acc.account_code[0:100]),
                                 ('Desc', acc.account_name[0:400]),
                                 ('Nivel', acc.account_level),
                                 ('Natur', acc.account_nature)]
                    if acc.parent_id:
                        ctaAttrs.append(('SubCtaDe', acc.parent_code[0:100]))
                    ctas.append(('Ctas', ctaAttrs))
            if not len(ctas):
                raise UserError(_('Archivo vacío\n\nNo se encontraron cuentas para XML cuyo primer periodo reportado sea mayor o igual al periodo procesado.'))
            xml_content = ('Catalogo', [('Version', '1.3'),
                                        ('RFC', user.company_id.partner_id.vat),
                                        ('Mes', ('0'+ str(period_id.date_start.month))[-2:]),
                                        ('Anio', str(period_id.date_start.year)),
                                        ('unroot', ctas)
                                     ])
            catalog_ns = self._SAT_NS.copy()
            catalog_ns['catalogocuentas'] = self._ACCOUNTS_CATALOG_URI
            xmlTree = self._xml_from_dict(xml_content, catalog_ns, self._ACCOUNTS_CATALOG_URI)
            xmlTree.attrib['{{{pre}}}schemaLocation'.format(pre=self._XSI_DECLARATION)] = '%s http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/CatalogoCuentas/CatalogoCuentas_1_3.xsd' % self._ACCOUNTS_CATALOG_URI
        elif form.xml_target == 'trial_balance':
            if balance_ids is None:
                trialWizardObj = self.env['account.monthly_balance_wizard']
                trial_balance_id = trialWizardObj.create({'chart_account_id': form.accounts_chart.id,
                                                         'company_id'       : user.company_id.id,
                                                         'period_id'        : period_id.id,
                                                         'partner_breakdown': False,
                                                         'output'           : 'list_view',})
                balance_ids = eval(trial_balance_id.get_info()['domain'][1:-1])[2]
            balanceRecords = self.env['account.monthly_balance'].browse(balance_ids)
            if form.format == 'pdf':
                allowed_ids = self.env['account.monthly_balance'].browse()
                for rc in balanceRecords:
                    if rc.account_id.take_for_xml and rc.account_id.first_period_id.date_start <= period_id.date_start:
                        allowed_ids += rc
                if not allowed_ids:
                    raise UserError("Ninguna cuenta de la balanza en este periodo está marcada para considerarse en el XML.")
                return self.env.ref('asti_eaccounting_mx_base.action_report_balanza_mensual_sat').report_action(allowed_ids)
                return self.env['report'].get_action(allowed_ids, 'asti_eaccounting_mx_base.report_balanza_mensual_sat')
            ctas = []
            for record in balanceRecords:
                if record.account_id.take_for_xml and record.account_id.first_period_id.date_start <= period_id.date_start: # and record.account_id.company_id.id == user.company_id.id:
                    ctasAttrs = [('NumCta', record.account_code[0:100]),
                                 ('SaldoIni', round(record.initial_balance, 2)),
                                 ('Debe', round(record.debit, 2)),
                                 ('Haber', round(record.credit, 2)),
                                 ('SaldoFin', round(record.ending_balance, 2))]
                    ctas.append(('Ctas', ctasAttrs))

            if not len(ctas):
                raise UserError(_('Archivo vacío\n\nNinguna cuenta de la balanza en este periodo está marcada para considerarse en el XML.'))
            content = [ ('Version', '1.3'),
                        ('RFC', user.company_id.partner_id.vat),
                        ('Mes', '{:02}'.format(period_id.date_start.month)),
                        ('Anio', str(period_id.date_start.year)),
                        ('TipoEnvio', form.trial_delivery),
                        ('unroot', ctas)]
            if form.trial_delivery == 'C':
                content.append(('FechaModBal', form.trial_lastchange_date))
            trialBalance_ns = self._SAT_NS.copy()
            trialBalance_ns['BCE'] = self._TRIAL_BALANCE_URI
            xmlTree = self._xml_from_dict(('Balanza', content), trialBalance_ns, self._TRIAL_BALANCE_URI)
            xmlTree.attrib['{{{pre}}}schemaLocation'.format(pre=self._XSI_DECLARATION)] = '%s http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/BalanzaComprobacion/BalanzaComprobacion_1_3.xsd' % self._TRIAL_BALANCE_URI
        elif form.xml_target in ('vouchers', 'helpers'):
            if form.format == 'pdf':
                raise UserError(_('Informe no disponible\n\nLa representación impresa no está disponible para las pólizas.'))
            if form.request_type in ('AF', 'FC'):
                if len(form.order_number) != 13:
                    raise UserError(_('Número de orden erróneo\n\nVerifique que su número de orden contenga 13 caracteres (incluida la diagonal)'))
                if not re.compile('[A-Z]{3}[0-6][0-9][0-9]{5}(/)[0-9]{2}').match(form.order_number.upper()):
                    raise UserError(_('Número de orden erróneo\n\nVerifique que su número de orden tenga la siguiente estructura:\n  * Tres letras mayúsculas de la A al Z sin incluir la "Ñ"\n  * Un dígito entre 0 y 6\n  * Un dígito entre 0 y 9\n  * Cinco dígitos entre 0 y 9\n  * Una diagonal "/"\n  * Dos dígitos del entre 0 y 9'))
            if form.request_type in ('DE', 'CO'):
                # Contabilidad 1.3
                if len(form.procedure_number) != 14: # Contabilidad 1.3
                    raise UserError(_('Número de trámite erróneo\n\nVerifique que su número de trámite contenga 14 caracteres.')) # Contabilidad 1.3
            accountMoveObj = self.env['account.move']
            if moveIds is None:
                #### FIX NEEDED #####
                # SE REQUIERE QUE TOME TODAS LAS POLIZAS SIN IMPORTAR LA COMPANIA
                periods = periodObj.search([('name','=',period_id.name)]) # Esto es util para cuando se tienen Companys hijos
                period_ids = [w.id for w in periods]
                moves = accountMoveObj.search([('period_id', 'in', period_ids), ('state', '=', 'posted')]) #, ('company_id', '=', user.company_id.id)])
            else:
                moves = accountMoveObj.browse(moveIds)
            if form.format == 'pdf':
                return {}
            if not moves:
                raise UserError(_('Información faltante\n\nNo se han encontrado pólizas para el periodo seleccionado.'))
            entries = []
            if form.xml_target == 'vouchers':
                for mv in moves:
                    voucher = (mv.ref if mv.ref else '') + '(' + mv.name + ')'
                    if not mv.line_ids:
                        raise UserError(_('Póliza incompleta\n\nLa póliza %s no tiene asientos definidos.') % (voucher))
                    #if not mv.item_concept and not mv.ref:
                    #    raise UserError(_('Información faltante\n\nLa póliza %s no tiene definido un concepto') % (voucher))

                    if not mv.item_concept:
                        mvAttrs = [('NumUnIdenPol', mv.name[0:50]), ('Fecha', mv.date), ('Concepto', mv.ref or (mv.journal_id.name + ' - ' + mv.name))]
                    else:
                        mvAttrs = [('NumUnIdenPol', mv.name[0:50]), ('Fecha', mv.date), ('Concepto', mv.item_concept[0:300])]
                    lines = []

                    for ln in mv.line_ids:
                        _logger.info("\nPartida: ID: %s - Cuenta: %s - %s - Name: %s - Ref: %s - Debit: %s - Credit: %s" % (ln.id, ln.account_id.code, ln.account_id.name, ln.name, ln.ref, ln.debit, ln.credit))
                        if not ln.name and not ln.ref:
                            raise UserError(_('Información faltante\n\nCompruebe que todos los asientos de la póliza %s tengan un concepto definido.') % (voucher))
                        lnAttrs = [  ('NumCta', ln.account_id.code[0:100]),
                                     ('DesCta', ln.account_id.name[0:100]),
                                     ('Concepto', (ln.name and ln.name[0:200]) or (ln.ref and ln.ref[0:200]) or ' '),
                                     ('Debe', round(ln.debit, 2)),
                                     ('Haber', round(ln.credit, 2))]
                        (cfdis, others, foreigns, checks, transfers, payments,) = ([],
                         [],
                         [],
                         [],
                         [],
                         [])
                        for cmpl in ln.complement_line_ids:
                            if cmpl.rfc and not _RFC_PATTERN.match(cmpl.rfc):
                                raise UserError(_('Información incorrecta\n\nEl RFC "%s" no es válido con respecto a los lineamientos del SAT. Póliza %s') % (cmpl.rfc, voucher))
                            if cmpl.rfc2 and not _RFC_PATTERN.match(cmpl.rfc2):
                                raise UserError(_('Información incorrecta\n\nEl RFC "%s" no es válido con respecto a los lineamientos del SAT. Póliza %s') % (cmpl.rfc2, voucher))
                            cmpl_attrs = []
                            commons = ['cfdi', 'foreign', 'other']
                            cmpl_attrs.append(('MontoTotal' if cmpl.type_key in commons else 'Monto', round(cmpl.amount, 2)))
                            if cmpl.compl_currency_id:
                                if not cmpl.compl_currency_id.sat_currency_id:
                                    raise UserError(_('Información faltante\n\nLa moneda "%s" no tiene asignado un código del SAT.') % (cmpl.compl_currency_id.name))
                                cmpl_attrs.append(('Moneda', cmpl.compl_currency_id.sat_currency_id.code))
                            if cmpl.exchange_rate:
                                cmpl_attrs.append(('TipCamb', round(cmpl.exchange_rate, 5)))
                            commons.pop(1)
                            commons.append('check')
                            commons.append('transfer')
                            if cmpl.type_key in commons:
                                if cmpl.rfc and cmpl.rfc2 and cmpl.rfc != user.company_id.partner_id.vat and cmpl.rfc2 != user.company_id.partner_id.vat:
                                    cmpl_attrs.append(('RFC', cmpl.rfc2.upper()))
                                else:
                                    cmpl_attrs.append(('RFC', cmpl.rfc.upper() if cmpl.rfc != user.company_id.partner_id.vat else cmpl.rfc2.upper()))
                            commons.pop(0)
                            commons.pop(0)
                            if cmpl.type_key in commons:                                
                                if cmpl.origin_account_id:
                                    cmpl_attrs.append(('CtaOri', cmpl.origin_account_id.acc_number[0:50]))
                            commons.append('payment')
                            if cmpl.type_key in commons:
                                cmpl_attrs.append(('Fecha', cmpl.compl_date))
                                cmpl_attrs.append(('Benef', cmpl.payee_id.name[0:300]))
                            if cmpl.type_key == 'cfdi':
                                if cmpl.uuid:
                                    if len(cmpl.uuid) != 36 or not _UUID_PATTERN.match(cmpl.uuid.upper()):
                                        raise UserError(_('Información incorrecta\n\nEl UUID "%s" en la póliza %s no se apega a los lineamientos del SAT.') % (cmpl.uuid, voucher))
                                    cmpl_attrs.append(('UUID_CFDI', cmpl.uuid.upper()))
                                cfdis.append(('CompNal', cmpl_attrs))
                            elif cmpl.type_key == 'other':
                                if cmpl.cbb_series and not _SERIES_PATTERN.match(cmpl.cbb_series):
                                    raise UserError(_('Información incorrecta\n\nLa "Serie" en el comprobante de la póliza %s solo debe contener letras.') % (voucher))
                                if cmpl.cbb_series:
                                    cmpl_attrs.append(('CFD_CBB_Serie', cmpl.cbb_series))
                                cmpl_attrs.append(('CFD_CBB_NumFol', cmpl.cbb_number))
                                others.append(('CompNalOtr', cmpl_attrs))
                            elif cmpl.type_key == 'foreign':
                                cmpl_attrs.append(('NumFactExt', cmpl.foreign_invoice))
                                cmpl_attrs.append(('TaxID', cmpl.foreign_tax_id))
                                foreigns.append(('CompExt', cmpl_attrs))
                            elif cmpl.type_key == 'check':
                                if not cmpl.origin_bank_id:
                                    raise UserError(_('Información faltante\n\nEl Complemento en la Poliza %s no cuenta con la informacion del Banco Nacional Origen.') % (voucher)) # Contabilidad 1.3
                                if not cmpl.origin_bank_id.sat_bank_id.bic: # Contabilidad 1.3
                                    raise UserError(_('Información faltante\n\nNo se ha encontrado un número de identificacion Bancaria para el Banco % s') % (cmpl.origin_bank_id.name)) # Contabilidad 1.3
                                if not cmpl.check_number:
                                    raise UserError(_('Información faltante\n\nNo se ha encontrado un número de cheque en la póliza % s') % (voucher))
                                cmpl_attrs.append(('Num', cmpl.check_number))
                                cmpl_attrs.append(('BanEmisNal', cmpl.origin_bank_id.sat_bank_id.bic))
                                if cmpl.origin_bank_id.sat_bank_id.bic == '999':
                                    cmpl_attrs.append(('BanEmisExt', cmpl.origin_frgn_bank))
                                checks.append(('Cheque', cmpl_attrs))
                            elif cmpl.type_key == 'transfer':
                                if not cmpl.origin_bank_id:
                                    raise UserError(_('Información faltante\n\nEl Complemento en la Poliza %s no cuenta con la informacion del Banco Nacional Origen.') % (voucher)) # Contabilidad 1.3
                                if not cmpl.origin_bank_id.sat_bank_id.bic: # Contabilidad 1.3
                                    raise UserError(_('Información faltante\n\nNo se ha encontrado un número de identificacion Bancaria para el Banco %s') % (cmpl.origin_bank_id.name)) # Contabilidad 1.3
                                cmpl_attrs.append(('BancoOriNal', cmpl.origin_bank_id.sat_bank_id.bic))
                                if cmpl.origin_bank_id.sat_bank_id.bic == '999':
                                    cmpl_attrs.append(('BancoOriExt', cmpl.origin_bank_id.name[0:150]))
                                if  not cmpl.destiny_account_id.acc_number:
                                    raise UserError(_('Información faltante\n\nLa Poliza %s no tiene una cuenta destino.') % (voucher))
                                cmpl_attrs.append(('CtaDest', cmpl.destiny_account_id.acc_number[0:50]))
                                if not cmpl.destiny_bank_id.sat_bank_id.bic:
                                    raise UserError(_('Información faltante\n\nEl Banco %s no tiene un número BIC.') % (cmpl.destiny_bank_id.name))
                                cmpl_attrs.append(('BancoDestNal', cmpl.destiny_bank_id.sat_bank_id.bic))
                                if cmpl.destiny_bank_id.sat_bank_id.bic == '999':
                                    cmpl_attrs.append(('BancoDestExt', cmpl.destiny_frgn_bank))
                                transfers.append(('Transferencia', cmpl_attrs))
                            elif cmpl.type_key == 'payment':
                                cmpl_attrs.append(('MetPagoPol', cmpl.pay_method_id.code))
                                cmpl_attrs.append(('RFC', cmpl.rfc2.upper()))
                                payments.append(('OtrMetodoPago', cmpl_attrs))

                        if len(cfdis):
                            lnAttrs.append(('unroot', cfdis))
                        if len(others):
                            lnAttrs.append(('unroot', others))
                        if len(foreigns):
                            lnAttrs.append(('unroot', foreigns))
                        if len(checks):
                            lnAttrs.append(('unroot', checks))
                        if len(transfers):
                            lnAttrs.append(('unroot', transfers))
                        if len(payments):
                            lnAttrs.append(('unroot', payments))
                        lines.append(('Transaccion', lnAttrs))
                    mvAttrs.append(('unroot', lines))
                    # transfer_details = [
                    #                 ('CtaOri','cuenta_origen'), #Opcional
                    #                 ('BancoOriNal','Santander'), #Required Catalogo de Banco SAT
                    #                 ('BancoOriExt','Nombre Banco Extranjero'), #Opcional, pero requerido si se tiene la informacion
                    #                 ('CtaDest','Cuenta Destino Transferencia'), # Required 
                    #                 ('BancoDestNal','Santander'), #Banco Destino Nacional, Catalogo del SAT
                    #                 ('BancoDestExt','Nombre Banco Extranjero Destino'), #Opcional, pero requerido si te tiene la informacion
                    #                 ('Fecha','2017-05-10'), #Required, Fecha de la transaccion
                    #                 ('Benef','Beneficiario Transf'), # Required
                    #                 ('RFC','RFC al que se le hace la transf'), # Required
                    #                 ('Monto','200.00'), #Required,Monto transferido, Hasta 2 decimales
                    #                 ('Moneda','MXN'), # Optional, Catalogo SAT, Obligatoria en caso de que no sea peso
                    #                 ('TipCamb','1.0'), # Optional, en caso de que la moneda no sea Peso sera obligatoria
                    #                 ]
                    # lines.append(('Transferencia',transfer_details))
                    entries.append(('Poliza', mvAttrs))

            else: # Auxiliar de Folios
                for mv in moves:
                    if not len(mv.complement_line_ids):
                        continue
                    voucher = (mv.ref if mv.ref else '') + '(' + mv.name + ')'
                    if not mv.name or mv.name == '/':
                        raise UserError(_('Información faltante\n\nLa póliza %s no tiene un número definido.') % (voucher))
                    if not mv.date:
                        raise UserError(_('Información faltante\n\nLa póliza %s no tiene una fecha definida.') % (voucher))
                    mvAttrs = [('NumUnIdenPol', mv.name), ('Fecha', mv.date)]
                    (cfdis, others, foreigns,) = ([], [], [])
                    for cmpl in mv.complement_line_ids:
                        cmpl_attrs = [('MontoTotal', round(cmpl.amount, 2))]
                        if cmpl.rfc:
                            if not _RFC_PATTERN.match(cmpl.rfc):
                                raise UserError(_('Información incorrecta\n\nEl RFC "%s" no es válido con respecto a los lineamientos del SAT. Póliza %s') % (cmpl.rfc, voucher))
                            cmpl_attrs.append(('RFC', cmpl.rfc))
                        if cmpl.compl_currency_id:
                            if not cmpl.compl_currency_id.sat_currency_id:
                                raise UserError(_('Información faltante\n\nLa moneda "%s" no tiene asignado un código del SAT.') % (cmpl.compl_currency_id.name))
                            cmpl_attrs.append(('Moneda', cmpl.compl_currency_id.sat_currency_id.code))
                        if cmpl.exchange_rate:
                            cmpl_attrs.append(('TipCamb', round(1 / cmpl.exchange_rate, 5)))
                        if cmpl.pay_method_id:
                            cmpl_attrs.append(('MetPagoAux', cmpl.pay_method_id.code))
                        if cmpl.type_key == 'cfdi':
                            if cmpl.uuid:
                                if len(cmpl.uuid) != 36 or not _UUID_PATTERN.match(cmpl.uuid.upper()):
                                    raise UserError(_('Información incorrecta\n\nEl UUID "%s" en la póliza %s no se apega a los lineamientos del SAT.') % (cmpl.uuid, voucher))
                            cmpl_attrs.append(('UUID_CFDI', cmpl.uuid.upper()))
                            cfdis.append(('ComprNal', cmpl_attrs))
                        elif cmpl.type_key == 'other':
                            if cmpl.cbb_series:
                                cmpl_attrs.append(('CFD_CBB_Serie', cmpl.cbb_series))
                            cmpl_attrs.append(('CFD_CBB_NumFol', cmpl.cbb_number))
                            others.append(('ComprNalOtr', cmpl_attrs))
                        else:
                            if cmpl.foreign_tax_id:
                                cmpl_attrs.append(('TaxID', cmpl.foreign_tax_id))
                                cmpl_attrs.append(('NumFactExt', cmpl.foreign_invoice))
                                foreigns.append(('ComprExt', cmpl_attrs))

                    if len(cfdis):
                        mvAttrs.append(('unroot', cfdis))
                    if len(others):
                        mvAttrs.append(('unroot', others))
                    if len(foreigns):
                        mvAttrs.append(('unroot', foreigns))
                    entries.append(('DetAuxFol', mvAttrs))

                if not len(entries):
                    raise UserError(_('Auxiliar vacío\n\nNo se encontraron pólizas que tengan complementos auxiliares relacionados.'))
            content = [('Version', '1.3' if form.xml_target == 'vouchers' else '1.3'),
                       ('RFC', user.company_id.partner_id.vat),
                       ('Mes', '{:02}'.format(period_id.date_start.month)),
                       ('Anio', str(period_id.date_start.year)),
                       ('TipoSolicitud', form.request_type),
                       ('unroot', entries)]
            if form.request_type in ('AF', 'FC'):
                content.append(('NumOrden', form.order_number.upper()))
            if form.request_type in ('DE', 'CO'):
                content.append(('NumTramite', form.procedure_number))
            target_ns = self._SAT_NS.copy()
            
            if form.xml_target == 'vouchers':
                target_ns['PLZ'] = self._VOUCHERS_URI
                xmlTree = self._xml_from_dict(('Polizas', content), target_ns, self._VOUCHERS_URI)
                xmlTree.attrib['{{{pre}}}schemaLocation'.format(pre=self._XSI_DECLARATION)] = '%s http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/PolizasPeriodo/PolizasPeriodo_1_3.xsd' % self._VOUCHERS_URI
            else:
                target_ns['RepAux'] = self._HELPERS_URI
                xmlTree = self._xml_from_dict(('RepAuxFol', content), target_ns, self._HELPERS_URI)
                xmlTree.attrib['{{{pre}}}schemaLocation'.format(pre=self._XSI_DECLARATION)] = '%s http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/AuxiliarFolios/AuxiliarFolios_1_3.xsd' % self._HELPERS_URI
        filename = self.env.user.company_id.partner_id.vat + str(form.year) + form.month
        if form.xml_target == 'accounts_catalog':
            filename += 'CT'
        elif form.xml_target == 'trial_balance':
            filename += 'B' + form.trial_delivery
        elif form.xml_target == 'vouchers':
            filename += 'PL'
        elif form.xml_target == 'helpers':
            filename += 'XF'
        filename += '.xml'
        validationResult = self._validate_xml(form.xml_target + '.xsd', xmlTree, filename)
        if isinstance(validationResult, dict):
            return validationResult
        self.write({'state'         : validationResult,
                    'filename'      : filename,
                    'primary_file'  : b64enc(self._outputXml(xmlTree))})
        return self._reopen_wizard(self.id)


    def do_stamp(self):
        self.ensure_one()                           
        form = self
        stamp_res = 'stamp_done'
        xslt_path = self._find_file_in_addons('asti_eaccounting_mx_base/sat_xslt', form.xml_target + '.xslt')
        try:
            xslt_file = open(xslt_path, 'r')
        except:
            raise UserError(_('Hoja XSLT no encontrada\n\nLa hoja de transformación no fue encontrada en la ruta "%s"') % (xslt_path))
        xsltTree = et.parse(xslt_file)
        xsltTree.find('{http://www.w3.org/1999/XSL/Transform}output').attrib['omit-xml-declaration'] = 'yes'
        try:
            xslt = et.XSLT(xsltTree)
        except et.XSLTParseError:
            xsltTree.find('{http://www.w3.org/1999/XSL/Transform}include').attrib['href'] = xslt_path.replace(form.xml_target, 'utils')
            try:
                xslt = et.XSLT(xsltTree)
                stamp_res = 'stamp_xcpt'
            except:
                xslt = None
        if xslt is None:
            raise UserError(_('Error al cargar la hoja XSLT\n\nPor favor intente sellar de nuevo el documento.'))
        xmlTree = et.ElementTree(et.fromstring(b64dec(form.primary_file)))
        transformedDocument = str(xslt(xmlTree)).encode('UTF-8')
        user = self.env.user
        ##########
        journal_id = self.env['account.journal'].search(
                                                 [('company_id', '=', user.company_id.id),
                                                  ('use_for_cfdi', '=', True),
                                                  ('date_start', '<=', time.strftime('%Y-%m-%d')),
                                                  ('date_end', '>=', time.strftime('%Y-%m-%d')),
                                                  #('active', '=', True),
                                                 ], limit=1)
        if not journal_id:
            raise UserError(_('Información faltante\n\nNo se ha encontrado una configuración de certificados disponible para la compañía %s') % (user.company_id.name))
        ##########
        eCert = journal_id
        ##########
        if not eCert.certificate_key_file_pem:
            raise UserError(_('Información faltante\n\nSe necesita una clave en formato PEM para poder sellar el documento'))
        crypter = RSA.load_key_string(b64dec(eCert.certificate_key_file_pem))
        algrthm = MessageDigest('sha256') # Contabilidad 1.3
        algrthm.update(transformedDocument)
        rawStamp = crypter.sign(algrthm.digest(), 'sha256') # Contabilidad 1.3
        certHexNum = X509.load_cert_string(b64dec(eCert.certificate_file_pem), X509.FORMAT_PEM).get_serial_number()
        #certNum = ('%x' % certHexNum).replace('33', 'B').replace('3', '')
        certNum = eCert.serial_number
        cert = ''.join([ ln for ln in b64dec(eCert.certificate_file_pem).decode("utf-8").split('\n') if 'CERTIFICATE' not in ln ])
        target = '{'
        if form.xml_target == 'accounts_catalog':
            target += self._ACCOUNTS_CATALOG_URI + '}Catalogo'
        elif form.xml_target == 'trial_balance':
            target += self._TRIAL_BALANCE_URI + '}Balanza'
        xmlTree.getroot().attrib['Sello'] = b64enc(rawStamp)
        xmlTree.getroot().attrib['noCertificado'] = certNum
        xmlTree.getroot().attrib['Certificado'] = cert
        validationResult = self._validate_xml(form.xml_target + '.xsd', xmlTree, form.filename)
        if isinstance(validationResult, dict):
            return validationResult
        self.write({'state': stamp_res,
                    'stamped_file': b64enc(self._outputXml(xmlTree))
                   })
        return self._reopen_wizard(self.id)


    def do_zip(self):
        self.ensure_one()
        form = self
        (descriptor, zipname,) = tempfile.mkstemp('eaccount_', '__asti_')
        zipDoc = ZipFile(zipname, 'w')
        xmlContent = b64dec(form.stamped_file) if form.stamped_file else b64dec(form.primary_file)
        zipDoc.writestr(form.filename, xmlContent, zipfile.ZIP_DEFLATED)
        zipDoc.close()
        os.close(descriptor)
        filename = self.env.user.company_id.partner_id.vat + str(form.year) + form.month
        if form.xml_target == 'accounts_catalog':
            filename += 'CT'
        elif form.xml_target == 'trial_balance':
            filename += 'B' + form.trial_delivery
        elif form.xml_target == 'vouchers':
            filename += 'PL'
        elif form.xml_target == 'helpers':
            filename += 'XF'
        filename += '.zip'
        self.write({ 'state': 'zip_done',
                     'zipped_file': b64enc(open(zipname, 'rb').read()),
                     'filename': filename})
        return self._reopen_wizard(self.id)



files_generator_wizard()

