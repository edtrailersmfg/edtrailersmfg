# -*- encoding: utf-8 -*-
from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT


import datetime
from pytz import timezone
import pytz
import tempfile
import base64
import os
import tempfile
import hashlib
from xml.dom import minidom
from lxml import etree
from lxml.objectify import fromstring

import time
import codecs
import traceback
import re

import json

from datetime import timedelta

from lxml import etree
from lxml.objectify import fromstring
from xml.dom.minidom import parse, parseString

CFDI_XSLT_CADENA_TFD = 'l10n_mx_einvoice/SAT/cadenaoriginal_3_3/cadenaoriginal_TFD_1_1.xslt'

import logging
_logger = logging.getLogger(__name__)

msg2 = "Contacte a su administrador de sistemas o mande correo a info@fixdoo.mx"

def conv_ascii(text):
    """
    @param text : text that need convert vowels accented & characters to ASCII
    Converts accented vowels, ñ and ç to their ASCII equivalent characters
    """
    old_chars = [
        'á', 'é', 'í', 'ó', 'ú', 'à', 'è', 'ì', 'ò', 'ù', 'ä', 'ë', 'ï', 'ö',
        'ü', 'â', 'ê', 'î', 'ô', 'û', 'Á', 'É', 'Í', 'Ó', 'Ú', 'À', 'È', 'Ì',
        'Ò', 'Ù', 'Ä', 'Ë', 'Ï', 'Ö', 'Ü', 'Â', 'Ê', 'Î', 'Ô', 'Û',
        'ç', 'Ç', 'ª', 'º', '°', ' ', 'Ã', 'Ø'
    ]
    new_chars = [
        'a', 'e', 'i', 'o', 'u', 'a', 'e', 'i', 'o', 'u', 'a', 'e', 'i', 'o',
        'u', 'a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U', 'A', 'E', 'I',
        'O', 'U', 'A', 'E', 'I', 'O', 'U', 'A', 'E', 'I', 'O', 'U',
        'c', 'C', 'a', 'o', 'o', ' ', 'A', '0'
    ]
    for old, new in zip(old_chars, new_chars):
        try:
            text = text.replace(unicode(old, 'UTF-8'), new)
        except:
            try:
                text = text.replace(old, new)
            except:
                raise UserError(_("Warning !\nCan't recode the string [%s] in the letter [%s]") % (text, old))
    return text



class AccountMove(models.Model):
    _inherit = 'account.move'
        

    # def get_invoice_taxes_to_print(self):
    #     tax_lines_data = self._prepare_tax_lines_data_for_totals_from_invoice()
    #     json_taxes = self._get_tax_totals(self.partner_id, tax_lines_data, self.amount_total, 
    #                                       self.amount_untaxed, self.currency_id)
    #     subtotals = json_taxes['subtotals']
    #     subtotal_name = ""
    #     if subtotals:
    #         subtotal_name = subtotals[0]['name']
    #     return json_taxes

    def invoice_with_taxes_report(self):
        invoice_w_txs = False
        tax_lines_data = self._prepare_tax_lines_data_for_totals_from_invoice()
        if tax_lines_data:
            invoice_w_txs = True
        return invoice_w_txs

    @api.depends('invoice_date','invoice_datetime')
    def _get_date_invoice_tz(self):
        tz = self.env.user.partner_id.tz or 'Mexico/General'
        if self.invoice_datetime:
            self.date_invoice_tz = self.invoice_datetime and self.server_to_local_timestamp(
                    self.invoice_datetime, tz) or False
        else:
            vals_date = self.assigned_datetime({'invoice_datetime': False,
                                                'invoice_date': self.invoice_date})
            self.invoice_datetime = vals_date['invoice_datetime']
            self.date_invoice_tz = self.invoice_datetime and self.server_to_local_timestamp(
                    self.invoice_datetime, tz) or False
            
        
    
    def _get_fname_invoice(self):
        for rec in self:
            if rec.move_type in ('in_invoice','in_refund'):
                rec.fname_invoice = '.'
                continue

            fname = ""
            if rec.company_id.partner_id.country_id.code=='MX':
                if not rec.company_emitter_id.partner_id.vat :
                    raise UserError(_("Error!\nLa Compañía Emisora no tiene definido el RFC."))

                fname += (rec.company_emitter_id.partner_id.vat[:2]=='MX' and \
                           rec.company_emitter_id.partner_id.vat[:4] != 'MXMX' and \
                           rec.company_emitter_id.partner_id.vat[2:] or \
                           rec.company_emitter_id.partner_id.vat) + '_' + (rec.name.replace('/','_').replace(' ','_').replace('-','_') or '')
            else:
                fname += (rec.company_id.partner_id.vat or '') + '_' + (rec.name.replace('/','_').replace(' ','_').replace('-','_') or '')
            rec.fname_invoice = fname
        
    """
    @api.model
    def tax_line_move_line_get(self):
        res = []
        for tax_line in self.tax_line_ids:
            res.append({
                'tax_line_id': tax_line.tax_id.id,
                'type': 'tax',
                'name': tax_line.name,
                'price_unit': tax_line.amount,
                'quantity': 1,
                'price': tax_line.amount,
                'account_id': tax_line.account_id.id,
                'account_analytic_id': tax_line.account_analytic_id.id,
                'invoice_id': self.id,
                'amount_base': tax_line.amount_base_company_curr or (not tax_line.tax_id.amount and tax_line.invoice_id.amount_untaxed or 0.0),
                'tax_id_secondary': tax_line.tax_id.id or False,
                })
        return res    
    """
    
    
    """    
    #### ON_CHANGE 
    @api.onchange('journal_id')
    def _onchange_journal_id(self):
        res = super(AccountMove, self)._onchange_journal_id()
        self.address_invoice_company_id = self.journal_id.address_invoice_company_id
        self.company2_id = self.journal_id.company2_id

    
    @api.onchange('partner_id', 'company_id')
    def _onchange_partner_id(self):
        res = super(AccountMove, self)._onchange_partner_id()
        self.pay_method_id  = self.partner_id and ((self.partner_id.parent_id and [self.partner_id.parent_id.pay_method_id.id]) or
                              (self.partner_id.pay_method_id and self.partner_id.pay_method_id.id)) or False
        self.pay_method_ids = self.partner_id and ((self.partner_id.parent_id and [self.partner_id.parent_id.pay_method_id.id]) or
                              (self.partner_id.pay_method_id and [self.partner_id.pay_method_id.id])) or False
        self.uso_cfdi_id = self.partner_id and ((self.partner_id.parent_id and self.partner_id.parent_id.uso_cfdi_id.id) or
                              (self.partner_id.uso_cfdi_id and self.partner_id.uso_cfdi_id.id)) or False

    """
    
    @api.onchange('invoice_date')
    def _onchange_invoice_date(self):
        super(AccountMove, self)._onchange_invoice_date()
        if self.move_type in ('out_invoice', 'out_refund'):
            vals_date = self.assigned_datetime({'invoice_datetime': False,
                                                'invoice_date': self.invoice_date})
            self.invoice_datetime = vals_date['invoice_datetime']
            
            
                
            
            
    
    
    # def button_draft(self):
    #     for invoice in self:
    #         if invoice.type in ('out_invoice','out_refund') and invoice.cfdi_folio_fiscal and invoice.state=='posted':
    #             raise UserError(_('No puede regresar la Factura o Nota de Crédito a borrador porque ya se encuentra timbrada. Si desea Cancelar la Factura de clic sobre el Botón "SOLICITUD CANCELACION"'))
    #     self.write({'xml_file_no_sign_index': False,
    #                 'cfdi_last_message': False, 
    #                 'cfdi_cadena_original' : False, 
    #                 'cfdi_state':'draft'})
    #     return super(AccountMove, self).button_draft()
    ####################################
    

    def server_to_local_timestamp(self, fecha, dst_tz_name, tz_offset=True, ignore_unparsable_time=True):

        if not fecha:
            return False

        res = fecha
        server_tz = "UTC"
        try:
            # dt_value needs to be a datetime object (so no time.struct_time or mx.DateTime.DateTime here!)
            dt_value = fecha
            if tz_offset and dst_tz_name:
                try:                        
                    src_tz = pytz.timezone(server_tz)
                    dst_tz = pytz.timezone(dst_tz_name)
                    src_dt = src_tz.localize(dt_value, is_dst=True)
                    dt_value = src_dt.astimezone(dst_tz)
                except Exception:
                    pass
            res = dt_value.replace(tzinfo=None)
        except Exception:
            if not ignore_unparsable_time:
                return False
        return res

        
    def _get_time_zone(self):
        userstz = self.env.user.partner_id.tz
        a = 0
        if userstz:
            hours = timezone(userstz)
            fmt = '%Y-%m-%d %H:%M:%S %Z%z'
            today_now = datetime.datetime.now()
            loc_dt = hours.localize(datetime.datetime(today_now.year, today_now.month, today_now.day,
                                                      today_now.hour, today_now.minute, today_now.second))
            timezone_loc = (loc_dt.strftime(fmt))
            diff_timezone_original = timezone_loc[-5:-2]
            timezone_original = int(diff_timezone_original)
            s = str(datetime.datetime.now(pytz.timezone(userstz)))
            s = s[-6:-3]
            timezone_present = int(s)*-1
            a = timezone_original + ((
                timezone_present + timezone_original)*-1)
        return a
    
    def assigned_datetime(self, values={}):
        res = {}
        if values.get('invoice_date', False) and not values.get('invoice_datetime', False):
            _logger.info("1111111111111111")
            user_hour = abs(self._get_time_zone())
            _logger.info("user_hour: %s" % user_hour)
            time_invoice = datetime.datetime.now().strptime('0%s:00:00' % user_hour, '%H:%M:%S').time()#datetime.datetime.time(user_hour, 0, 0)
            invoice_date = values['invoice_date'] #datetime.datetime.strptime(values['invoice_date'], '%Y-%m-%d').date()
            dt_invoice = datetime.datetime.combine(invoice_date, time_invoice).strftime('%Y-%m-%d %H:%M:%S')            
            xdt_invoice = datetime.datetime.now(pytz.timezone(self.env.user.partner_id.tz or 'Mexico/General'))
            if xdt_invoice.date() == values['invoice_date']:
                dt_invoice = datetime.datetime.now()
            ################################
            res.update({'invoice_datetime' : dt_invoice,
                        'invoice_date' :  values['invoice_date']})
        if values.get('invoice_datetime', False) and not values.get('invoice_date', False):
            _logger.info("2222222222222222")
            _logger.info("values['invoice_datetime']: %s" % values['invoice_datetime'])
            invoice_date = fields.Datetime.context_timestamp(self, values['invoice_datetime'])
            res.update({'invoice_date'    : values['invoice_datetime'].date(),#invoice_date, 
                       'invoice_datetime' : values['invoice_datetime']})            
        if False and 'invoice_datetime' in values  and 'invoice_date' in values:
            _logger.info("33333333333333333")
            if values['invoice_datetime'] and values['invoice_date']:
                invoice_date = values['invoice_datetime'].date() 
                if invoice_date != values['invoice_date']:
                    raise UserError(_('Invoice dates should be equal'))
                            
        if  not values.get('invoice_datetime', False) and not values.get('invoice_date', False):
            _logger.info("4444444444444444444444444")
            res['invoice_date'] = fields.Date.context_today
            res['invoice_datetime'] = fields.Datetime.now()
        return res
            
    """
    def action_move_create(self):
        res = super(AccountMove, self).action_move_create()
        for inv in self:
            if inv.type in ('out_invoice', 'out_refund'):
                vals_date = self.assigned_datetime({'invoice_datetime': inv.invoice_datetime,
                                                    'invoice_date': inv.invoice_date,
                                                            })
                inv.write(vals_date)
        return res
    """
    
    def check_partner_data(self, xpartner, is_company_address=False):
        partner = xpartner.commercial_partner_id
        if not is_company_address and partner.company_type == 'person':
            raise UserError(_("La Empresa - (ID: %s) %s - no está definida como Compañía o Persona Fisica, para usarlo en Facturas, es necesario que la defina como Compañía...") % (partner.id,partner.name))
        if not partner.vat:
            raise UserError(_("La Empresa - (ID: %s) %s - no tiene el RFC definido, por favor revise...") % (partner.id,partner.name))
        if partner.country_id.code == 'MX' and not is_company_address and not partner.zip_sat_id:
            _logger.info("is_company_address: %s - partner: %s" % (is_company_address, partner.name))
            raise UserError(_("La Empresa - (ID: %s) %s - no tiene Codigo Postal en su direccion %s, por favor revise...") % (partner.id, partner.name, partner.zip_sat_id.code))
        return
    
    
    ##################################
    
    def binary2file(self, binary_data, file_prefix="", file_suffix=""):
        """
        @param binary_data : Field binary with the information of certificate
                of the company
        @param file_prefix : Name to be used for create the file with the
                information of certificate
        @file_suffix : Sufix to be used for the file that create in this function
        """
        (fileno, fname) = tempfile.mkstemp(file_suffix, file_prefix)
        f = open(fname, 'wb')
        f.write(base64.b64decode(binary_data))
        f.close()
        os.close(fileno)
        return fname
    
    
    def _xml2cad_orig(self):
        context = self._context.copy()
        xslt_root = etree.parse(tools.file_open(context['fname_xslt']))
        cfdi_as_tree = fromstring(context['xml_prev'])
        cadena_original = str(etree.XSLT(xslt_root)(cfdi_as_tree))
        return cadena_original

    
    def _get_certificate_str(self, fname_cer_pem=""):
        """
        @param fname_cer_pem : Path and name the file .pem
        """
        fcer = open(fname_cer_pem, "r")
        lines = fcer.readlines()
        fcer.close()
        cer_str = ""
        loading = False
        for line in lines:
            if 'END CERTIFICATE' in line:
                loading = False
            if loading:
                cer_str += line
            if 'BEGIN CERTIFICATE' in line:
                loading = True
        return cer_str


    def dict2xml(self, data_dict, node=False, doc=False):
        """
        @param data_dict : Dictionary of attributes for add in the XML 
                    that will be generated
        @param node : Node from XML where will be added data from the dictionary
        @param doc : Document XML generated, where will be working
        """
        parent = False
        if node:
            parent = True
        for element, attribute in self._dict_iteritems_sort(data_dict):
            if not parent:
                doc = minidom.Document()
            # Para lineas que no esten agrupadas podemos usar un diccionario = []
            # donde cada item del list es un diccionario.
            if element == '_value_not_grouped':
                for attr in attribute:
                    self.dict2xml(attr, node, doc)
            elif isinstance(attribute, dict):
                if not parent:
                    node = doc.createElement(element)
                    self.dict2xml(attribute, node, doc)
                else:
                    child = doc.createElement(element)
                    # Creamos el texto dentro de "element", Por ejemplo: <tag>valor</tag>
                    # Recuerde usar un diccionario con un elemento: '_value' : valor
                    if isinstance(attribute, dict) and '_value' in attribute:
                        if len(attribute)==1:
                            xres = doc.createTextNode(attribute['_value'])
                            child.appendChild(xres)
                        else:
                            attribute2 = attribute.copy()
                            attribute2.pop('_value')
                            self.dict2xml(attribute2, child, doc)
                            xres = doc.createTextNode(attribute['_value'])
                            child.appendChild(xres)
                    else:
                        self.dict2xml(attribute, child, doc)
                    node.appendChild(child)
            elif isinstance(attribute, list):
                child = doc.createElement(element)
                for attr in attribute:
                    if isinstance(attr, dict):
                        if element=='cfdi:InformacionAduanera': #AC
                            child = doc.createElement(element) #AC
                        self.dict2xml(attr, child, doc)
                        if element == 'cfdi:InformacionAduanera': #AC
                            node.appendChild(child) #AC
                node.appendChild(child)
            else:
                if isinstance(attribute, str): # or isinstance(attribute, bytes):
                    attribute = conv_ascii(attribute)
                else:
                    attribute = str(attribute)
                node.setAttribute(element, attribute)
        if not parent:
            doc.appendChild(node)
        return doc    
    
    
    # TODO: agregar esta funcionalidad con openssl
    def _get_md5_cad_orig(self, cadorig_str, fname_cadorig_digest):
        """
        @param cadorig_str :
        @fname cadorig_digest :
        """
        cadorig_digest = hashlib.md5(cadorig_str).hexdigest()
        open(fname_cadorig_digest, "w").write(cadorig_digest)
        return cadorig_digest, fname_cadorig_digest
    
    
    # def _get_noCertificado(self, fname_cer, pem=True):
    #     """
    #     @param fname_cer : Path more name of file created whit information 
    #                 of certificate with suffix .pem
    #     @param pem : Boolean that indicate if file is .pem
    #     """
    #     certificate_lib = self.env['facturae.certificate.library']
    #     fname_serial = certificate_lib.b64str_to_tempfile(base64.encodebytes(b''), 
    #                                                       file_suffix='.txt', 
    #                                                       file_prefix='odoo__serial__')
    #     result = certificate_lib._get_param_serial(fname_cer, fname_out=fname_serial, type='PEM')
    #     return result

        
    def _get_sello(self):
        # TODO: Put encrypt date dynamic
        context = self._context.copy() or {}
        fecha = self._context['fecha']
        year = float(time.strftime('%Y', time.strptime(fecha, '%Y-%m-%dT%H:%M:%S')))
        encrypt = "sha256"
        result_sello_256 = self.env['facturae.certificate.library'].with_context(context)._sign_sello()
        return result_sello_256.decode("utf-8") 

    
    def _dict_iteritems_sort(self, data_dict):
        """
        @param data_dict : Dictionary with data from invoice
        """
        key_order = [
            'cfdi:CfdiRelacionados',
            'cfdi:Emisor',
            'cfdi:Receptor',
            'cfdi:Conceptos',
            'cfdi:Impuestos',
            'cfdi:Complemento',
            'cfdi:Addenda',
        ]
        keys = list(data_dict.keys())
        key_item_sort = []
        for ko in key_order:
            if ko in keys:
                key_item_sort.append([ko, data_dict[ko]])
                keys.pop(keys.index(ko))
        
        if keys ==['Rfc', 'RegimenFiscal', 'Nombre' ]:
            keys = ['Rfc', 'Nombre', 'RegimenFiscal']
        if keys ==['RegimenFiscal', 'Rfc', 'Nombre' ]:
            keys = ['Rfc', 'Nombre', 'RegimenFiscal']
        if keys ==['Nombre', 'RegimenFiscal', 'Rfc']:
            keys = ['Rfc', 'Nombre', 'RegimenFiscal']
        if keys == ['cfdi:Retenciones', 'cfdi:Traslados']:
            keys = ['cfdi:Traslados','cfdi:Retenciones']
        if keys == ['cfdi:Traslados', 'TotalImpuestosTrasladados', 'cfdi:Retenciones', 'TotalImpuestosRetenidos']:
            keys = ['cfdi:Retenciones', 'TotalImpuestosRetenidos','cfdi:Traslados', 'TotalImpuestosTrasladados']
        if keys == ['TotalImpuestosTrasladados', 'cfdi:Traslados', 'TotalImpuestosRetenidos', 'cfdi:Retenciones']:
            keys = ['cfdi:Retenciones', 'TotalImpuestosRetenidos','cfdi:Traslados', 'TotalImpuestosTrasladados']
        
        #TAGS de Complemento de Comercio Exterior
        #print("keys: %s" % keys)
        if 'cce11:Emisor' in keys:
            keys2 = ['Version', 'TipoOperacion', 'ClaveDePedimento', 'CertificadoOrigen', 'NumCertificadoOrigen', 'Incoterm', 'Subdivision', 'Observaciones', 'TipoCambioUSD', 'TotalUSD',  'xmlns:cce11',  'xsi:schemaLocation', 'xmlns:xsi', 'cce11:Emisor', 'cce11:Receptor', 'cce11:Destinatario', 'cce11:Mercancias']
            if not 'NumCertificadoOrigen' in keys:
                keys2.remove('NumCertificadoOrigen')
            if not 'cce11:Destinatario' in keys:
                keys2.remove('cce11:Destinatario')
            keys = keys2
            
        #TAGS de Complemento Detallista -- 1 --
        elif 'xmlns:detallista' in keys:
            # print "keys: %s" % keys
            keys2 = ['xmlns:detallista','xsi:schemaLocation','contentVersion','type','documentStructureVersion','documentStatus',
                     'detallista:requestForPaymentIdentification',
                     'detallista:specialInstruction',
                     'detallista:orderIdentification',
                     'detallista:AdditionalInformation',
                     'detallista:DeliveryNote',
                     'detallista:buyer',
                     'detallista:seller',
                     #'detallista:allowanceCharge',
                     '_value_not_grouped', #'detallista:lineItem',
                     'detallista:totalAmount',
                     'detallista:TotalAllowanceCharge'
                    ]
            for xkey in keys2:
                if not xkey in keys:
                    keys2.remove(xkey)
            keys = keys2
        #TAGS de Complemento Detallista  - Lineas de productos -- 2 --
        elif 'detallista:tradeItemIdentification' in keys:
            #print "keys: %s" % keys
            keys2 = ['detallista:tradeItemIdentification',
                     'detallista:alternateTradeItemIdentification',
                     'detallista:tradeItemDescriptionInformation',
                     'detallista:invoicedQuantity',
                     'detallista:grossPrice',
                     'detallista:netPrice',
                     'detallista:totalLineAmount'
                    ]
            for xkey in keys2:
                if not xkey in keys:
                    keys2.remove(xkey)
            keys = keys2
        #TAGS de Complemento Detallista  - Total en Lineas de productos -- 3 --
        elif 'detallista:grossAmount' in keys:
            #print "keys: %s" % keys
            keys2 = ['detallista:grossAmount', 'detallista:netAmount']
            for xkey in keys2:
                if not xkey in keys:
                    keys2.remove(xkey)
            keys = keys2
            
            
        for key_too in keys:
            key_item_sort.append([key_too, data_dict[key_too]])
        return key_item_sort    
    
    
    def _get_file_globals(self):
        ctx = self._context.copy()
        file_globals = {}
        invoice = self
        ctx.update({'date_work': invoice.date_invoice_tz})

        if not (invoice.journal_id.date_start <= invoice.date_invoice_tz.date() and invoice.journal_id.date_end >= invoice.date_invoice_tz.date()):
            raise UserError(_("Error !!!\nLa fecha de la factura está fuera del rango de Vigencia del Certificado, por favor revise."))
        
        
        certificate_file_pem     = invoice.journal_id.certificate_file_pem
        certificate_key_file_pem = invoice.journal_id.certificate_key_file_pem
        certificate_file         = invoice.journal_id.certificate_file
        certificate_key_file     = invoice.journal_id.certificate_key_file
        certificate_pfx_file     = invoice.journal_id.certificate_pfx_file
        
        fname_cer_pem = False
        #try:
        fname_cer_pem = self.binary2file(
                certificate_file_pem, 'odoo_' + (
                invoice.journal_id.serial_number or '') + '__certificate__',
                '.cer.pem')
        #except:
        #    raise UserError(_("Error !!! \nEl archivo del Certificado no existe en formato PEM"))
        
        file_globals['fname_cer'] = fname_cer_pem
        # - - - - - - - - - - - - - - - - - - - - - - -
        fname_key_pem = False
        #try:
        fname_key_pem = self.binary2file(certificate_key_file_pem, 'odoo_' + (invoice.journal_id.serial_number or '') + '__certificate__','.key.pem')
        #except:
        #    raise UserError(_("Error !!! \nEl archivo de la llave (KEY) del Certificado no existe en formato PEM"))

        file_globals['fname_key'] = fname_key_pem
        # - - - - - - - - - - - - - - - - - - - - - - -
        fname_cer_no_pem = False
        #try:
        fname_cer_no_pem = self.binary2file(certificate_file, 'odoo_' + (invoice.journal_id.serial_number or '') + '__certificate__','.cer')
        #except:
        #    pass
        file_globals['fname_cer_no_pem'] = fname_cer_no_pem
        # - - - - - - - - - - - - - - - - - - - - - - -
        fname_key_no_pem = False
        #try:
        fname_key_no_pem = self.binary2file(certificate_key_file, 'odoo_' + (invoice.journal_id.serial_number or '') + '__certificate__','.key')
        #except:
        #    pass
        file_globals['fname_key_no_pem'] = fname_key_no_pem
        # - - - - - - - - - - - - - - - - - - - - - - -
        fname_pfx = False
        #try:
        fname_pfx = self.binary2file(certificate_pfx_file, 'odoo_' + (invoice.journal_id.serial_number or '') + '__certificate__','.pfx')
        #except:
        #    raise UserError(_("Error !!! \nEl archivo del Certificado no existe en formato PFX"))

        file_globals['fname_pfx'] = fname_pfx
        # - - - - - - - - - - - - - - - - - - - - - - -
        file_globals['password'] = invoice.journal_id.certificate_password
        # - - - - - - - - - - - - - - - - - - - - - - -
        if invoice.journal_id.fname_xslt:
            if (invoice.journal_id.fname_xslt[0] == os.sep or \
                invoice.journal_id.fname_xslt[1] == ':'):
                file_globals['fname_xslt'] = invoice.journal_id.fname_xslt
            else:
                file_globals['fname_xslt'] = os.path.join(
                    tools.config["root_path"], invoice.journal_id.fname_xslt)
        else:
            # Search char "," for addons_path, now is multi-path
            all_paths = tools.config["addons_path"].split(",")
            for my_path in all_paths:
                if os.path.isdir(os.path.join(my_path,
                    'l10n_mx_einvoice', 'SAT')):
                    # If dir is in path, save it on real_path
                    file_globals['fname_xslt'] = my_path and os.path.join(
                        my_path, 'l10n_mx_einvoice', 'SAT', 'cadenaoriginal_3_3',
                        'cadenaoriginal_3_3.xslt') or ''
                    ### TFD CADENA ORIGINAL XSLT ###
                    file_globals['fname_xslt_tfd'] = my_path and os.path.join(
                        my_path, 'l10n_mx_einvoice', 'SAT', 'cadenaoriginal_3_3',
                        'cadenaoriginal_TFD_1_1.xslt') or ''
                    break
        if not file_globals.get('fname_xslt', False):
            raise UserError(_("Advertencia !!! \nNo se tiene definido fname_xslt"))

        if not os.path.isfile(file_globals.get('fname_xslt', ' ')):
            raise UserError(_("Advertencia !!! \nNo existe el archivo [%s]. !") % (file_globals.get('fname_xslt', ' ')))

        file_globals['serial_number'] = invoice.journal_id.serial_number
        # - - - - - - - - - - - - - - - - - - - - - - -

        # Search char "," for addons_path, now is multi-path
        all_paths = tools.config["addons_path"].split(",")
        for my_path in all_paths:
            if os.path.isdir(os.path.join(my_path, 'l10n_mx_einvoice', 'SAT')):
                # If dir is in path, save it on real_path
                file_globals['fname_xslt'] = my_path and os.path.join(
                    my_path, 'l10n_mx_einvoice', 'SAT','cadenaoriginal_3_3',
                    'cadenaoriginal_3_3.xslt') or ''
                ### TFD CADENA ORIGINAL XSLT ###
                file_globals['fname_xslt_tfd'] = my_path and os.path.join(
                    my_path, 'l10n_mx_einvoice', 'SAT', 'cadenaoriginal_3_3',
                    'cadenaoriginal_TFD_1_1.xslt') or ''
        return file_globals
             
    def return_index_floats(self,decimales):
        i = len(decimales) - 1
        indice = 0
        while(i > 0):
            if  decimales[i] != '0':
                indice = i
                i = -1
            else:
                i-=1
        return  indice
    
    
    def write_cfd_data(self, cfd_datas):
        """
        @param cfd_datas : Dictionary with data that is used in facturae CFD and CFDI
        """
        if not cfd_datas:
            cfd_datas = {}
        comprobante = 'cfdi:Comprobante'
        cfd_data = cfd_datas
        NoCertificado = cfd_data.get(comprobante, {}).get('NoCertificado', '')
        certificado = cfd_data.get(comprobante, {}).get('Certificado', '')
        sello = cfd_data.get(comprobante, {}).get('Sello', '')
        cadena_original = cfd_data.get('cadena_original', '')
        data = {
            'no_certificado': NoCertificado,
            'certificado': certificado,
            'sello': sello,
            'cadena_original': cadena_original,
        }
        self.write(data)
        return True

    def _get_einvoice_complement_dict(self, comprobante):
        return comprobante
    
    
    def _get_global_taxes(self):
        self.ensure_one()
        values = {
            'total_retenciones': 0,
            'total_impuestos': 0,
            'retenciones': [],
            'impuestos': [],
        }
        taxes = {}
        for line in self.invoice_line_ids.filtered('price_subtotal'):
            price = line.price_unit * (1.0 - (line.discount or 0.0) / 100.0)
            tax_line = {tax['id']: tax for tax in line.tax_ids.compute_all(
                price, line.currency_id, line.quantity, line.product_id, line.partner_id, self.move_type in ('in_refund', 'out_refund'))['taxes']}
            for tax in line.tax_ids.filtered(lambda r: r.sat_tasa_cuota != 'Exento'):
                tax_dict = tax_line.get(tax.id, {})
                amount = round(abs(tax_dict.get(
                    'amount', tax.amount / 100 * float("%.2f" % line.price_subtotal))), 2)
                rate = round(abs(tax.amount), 2)
                amount_base = round(abs(tax_dict.get(
                    'base',line.price_subtotal)), )
                if tax.id not in taxes:
                    taxes.update({tax.id: {
                        'name': (tax.invoice_repartition_line_ids.tag_ids[0].name
                                 if tax.mapped('invoice_repartition_line_ids.tag_ids') else tax.name).upper(),
                        'amount': amount,
                        'rate': rate if tax.amount_type == 'fixed' else rate / 100.0,
                        'type': tax.sat_tasa_cuota,
                        'tax_amount': tax_dict.get('amount', tax.amount),
                        'sat_code_tax' : tax.sat_code_tax,
                        'amount_base': amount_base,
                    }})
                else:
                    taxes[tax.id].update({
                        'amount': taxes[tax.id]['amount'] + amount,
                        'tax_amount': taxes[tax.id]['tax_amount'] + amount,
                        'amount_base': taxes[tax.id]['amount_base'] + amount_base,
                    })
                if tax.amount >= 0:
                    values['total_impuestos'] += amount
                else:
                    values['total_retenciones'] += amount
        values['impuestos'] = [tax for tax in taxes.values() if tax['tax_amount'] >= 0]
        values['retenciones'] = [tax for tax in taxes.values() if tax['tax_amount'] < 0]
        #values['retenciones'] = self._l10n_mx_edi_group_withholding(
        #    [tax for tax in taxes.values() if tax['tax_amount'] < 0])
        return values
    
    def _get_facturae_invoice_dict_data(self):
        self.ensure_one()
        invoice_datas = []
        invoice_data_parents = []
        invoice = self
        invoice_data_parent = {}
        ## Tipo de Documento ####
        tipoComprobante = invoice.type_document_id.code
        # else:
        #     raise UserError(_("Solo puede Timbrar facturas de Clientes"))
        if invoice.move_type not in ('out_invoice','out_refund'):
            raise UserError(_("Solo puede Timbrar facturas de Clientes"))
        _logger.info("invoice_date: %s" % invoice.invoice_date)
        date_ctx = {'date': invoice.date_invoice_tz and invoice.date_invoice_tz.date() or invoice.invoice_date or fields.Date.context_today}
                #and time.strftime('%Y-%m-%d', time.strptime(invoice.date_invoice_tz,
                #'%Y-%m-%d %H:%M:%S')) or False}

        # Inicia seccion: Comprobante
        invoice_data_parent['cfdi:Comprobante'] = {}
        # default data
        invoice_data_parent['cfdi:Comprobante'].update(
                    {'xmlns:cfdi'   : "http://www.sat.gob.mx/cfd/3",
                     'xmlns:xs'     : "http://www.w3.org/2001/XMLSchema",
                     'xmlns:xsi'    : "http://www.w3.org/2001/XMLSchema-instance",
                     'xsi:schemaLocation': "http://www.sat.gob.mx/cfd/3 http://www.sat.gob.mx/sitio_internet/cfd/3/cfdv33.xsd",
                     'Version': "3.3", })
        
        #xnumber_work = re.findall('\d+', invoice.number)  or False
        #number_work = xnumber_work and xnumber_work[0] or xnumber_work
        
        currency = invoice.currency_id
        rate = invoice.currency_id.with_context(date_ctx).rate
        rate = rate != 0 and 1.0/rate or 0.0
        if rate >= 0.99999 and rate <= 1.00001:#rate==1.0:
            rate = 1
        else:
            rate = '%.4f' % rate or 1
        ## Guardando el Tipo de Cambio ##
        self.write({'tipo_cambio': rate})
        # Serie y Folio
        serie_from_type = invoice.journal_id.code
        try:
            car= '/' if '/' in self.name else '-' if '-' in self.name else '.' if '.' in self.name else '*'
            if car=='*':
                number_work = self.name
            name_splitted = self.name.split(car)
            try:
                serie_from_type = car.join(x for x in name_splitted[:-1]) + car
                number_work = name_splitted[-1:][0]
            except:
                number_work = self.name
        except:
            try:
                xnumber_work = re.findall('\d+', self.name)  or False
                number_work = xnumber_work and xnumber_work[0] or xnumber_work
            except:
                number_work = self.name
            
        #xnumber_work = re.findall('\d+', self.name)  or False
        #number_work = xnumber_work and xnumber_work[0] or xnumber_work
        #serie_from_type = invoice.journal_id.sequence_id.prefix and invoice.journal_id.sequence_id.prefix.replace('/','').replace(' ','').replace('-','') or ''
        # serie_from_type = (self.journal_id.code or '').replace('-', '').replace('/','').replace(' ','').replace('.','')
        #if invoice.move_type == 'out_refund':
        #    if invoice.journal_id.refund_sequence_id:
        #        serie_from_type = serie_from_type = invoice.journal_id.refund_sequence_id.prefix and invoice.journal_id.refund_sequence_id.prefix.replace('/','').replace(' ','').replace('-','') or ''
        invoice_data_parent['cfdi:Comprobante'].update({
            'Folio': number_work,
            'Fecha': invoice.date_invoice_tz.strftime('%Y-%m-%dT%H:%M:%S') or '', #and time.strftime('%Y-%m-%dT%H:%M:%S', time.strptime(invoice.date_invoice_tz, '%Y-%m-%d %H:%M:%S')) or '',
            'TipoDeComprobante': tipoComprobante,
            'NoCertificado': '@',
            'Sello': '',
            'Certificado': '@',
            'SubTotal': "%.2f" % (invoice.amount_untaxed or 0.0),
            'Total' : "%.2f" % ((self.amount_total if self.amount_discount == 0.0 else  \
                                 (self.amount_subtotal - self.amount_discount + self.amount_tax)) or 0.0),
            'Serie' : serie_from_type,
            'LugarExpedicion': invoice.address_issued_id.zip_sat_id.code,
            'Moneda': invoice.currency_id.name.upper(),
            'TipoCambio': rate,
            # 'FormaPago': invoice.pay_method_ids and ','.join([x.code for x in invoice.pay_method_ids]) or '99',
            'CondicionesDePago': invoice.invoice_payment_term_id.name if invoice.invoice_payment_term_id else '',
        })
        if invoice.pay_method_id:
            invoice_data_parent['cfdi:Comprobante'].update({
                'FormaPago': invoice.pay_method_id.code,
            })
        if invoice.metodo_pago_id:
            invoice_data_parent['cfdi:Comprobante'].update({
                'MetodoPago': invoice.metodo_pago_id.code if invoice.metodo_pago_id else ""
            })
        ### CondicionesDePago ###
        if invoice_data_parent['cfdi:Comprobante']['CondicionesDePago']  in (False, '', ' '):
            invoice_data_parent['cfdi:Comprobante'].pop('CondicionesDePago')

        if invoice_data_parent['cfdi:Comprobante']['Serie']  in (False, '', ' '):
            invoice_data_parent['cfdi:Comprobante'].pop('Serie')
        
        if self.amount_discount:
            invoice_data_parent['cfdi:Comprobante'].update({
                                                    'Descuento': "%.2f" % (self.amount_discount or 0.0),
                                                    'SubTotal': "%.2f" % self.amount_subtotal,
                                                    })
                
        
        # Termina seccion: Comprobante
        # Inicia seccion: Emisor
        partner_obj = self.partner_id
        address_invoice = invoice.address_issued_id or False
        address_invoice_parent = invoice.company_emitter_id and invoice.company_emitter_id.partner_id or False
        if not address_invoice:
            raise UserError(_('Advertencia !!\nNo ha definido dirección de emisión...'))
        if not address_invoice_parent:
            raise UserError(_('Advertencia !!\nNo ha definido la dirección de la Compañía...'))
        if not address_invoice_parent.vat:
            raise UserError(_('Advertencia !!\nNo ha definido el RFC de la Compañía...'))
        
        self.check_partner_data(invoice.partner_id, True)
        self.check_partner_data(invoice.address_issued_id, True)
        self.check_partner_data(address_invoice_parent, False)
    
        invoice_data = invoice_data_parent['cfdi:Comprobante']

        ### Agregando los CFDI Relacionados ####
        if self.type_rel_cfdi_ids:
            if not self.type_rel_id:
                raise UserError("Error !\nDebes identificar el Tipo de Relacion para los CFDI.")
            cfdi_relacionado_list = []
            for cfdi_rel in self.type_rel_cfdi_ids:
                cfdi_relacionado_list.append({'cfdi:CfdiRelacionado': [{'UUID': cfdi_rel.invoice_id.cfdi_folio_fiscal}]})
                cfdi_rel.invoice_id.write({'deposit_invoice_used': True, 'deposit_invoice_rel_id': self.id})
            cfdi_relacionado_list.append({'TipoRelacion': self.type_rel_id.code})
            invoice_data['cfdi:CfdiRelacionados'] =  cfdi_relacionado_list
                                                    
        invoice_data['cfdi:Emisor'] = {}

        if not self.env.company.regimen_fiscal_id:
            raise UserError("Error!\nLa Compañía %s no tiene definido un Regimen Fiscal, por lo cual no puede emitir el Recibo CFDI." % address_invoice_parent.name)

        parent_name = address_invoice_parent.name if address_invoice_parent.name else ''
        parent_name = parent_name.replace('&','&amp;')
        parent_name = parent_name.replace('<','&lt;')
        parent_name = parent_name.replace('>','&gt;')
        invoice_data['cfdi:Emisor'].update({

            'Rfc': address_invoice_parent.vat[:2]=='MX' and \
                   address_invoice_parent.vat[:4] != 'MXMX' and \
                   address_invoice_parent.vat[2:] or address_invoice_parent.vat,
            'Nombre': address_invoice_parent.name,
            'RegimenFiscal': self.env.company.regimen_fiscal_id.code or '',
            
        })

        # Termina seccion: Emisor
        # Inicia seccion: Receptor
        parent_obj = self.partner_id.commercial_partner_id
        #parent_obj = partner_obj.browse(cr, uid, parent_id, context=context)
        if not parent_obj.vat:
            raise UserError(_('Advertencia !!\nNo ha definido el RFC para la Empresa [%s] !') % (parent_obj.name))
        if parent_obj.country_id.code != 'MX':
            rfc = 'XEXX010101000'
        else:
            rfc = parent_obj.vat[:2]=='MX' and parent_obj.vat[:4] != 'MXMX' and parent_obj.vat[2:] or parent_obj.vat
        address_invoice = self.partner_id
        invoice_data['cfdi:Receptor'] = {}
        invoice_data['cfdi:Receptor'].update({
            'Rfc': rfc.upper(),
            'Nombre': (parent_obj.name or ''),
            'UsoCFDI': invoice.uso_cfdi_id.code,

        })
        # Termina seccion: Receptor
        
        # Inicia seccion: Conceptos
        total_impuestos_trasladados = 0.0
        total_impuestos_retenidos = 0.0

        invoice_data['cfdi:Conceptos'] = []
        account_tax_obj = self.env['account.tax']
        for line in self.invoice_line_ids.filtered(lambda inv: not inv.display_type):
            sat_product_id = line.product_id.sat_product_id
            if not sat_product_id:
                sat_product_id = line.product_id.categ_id.sat_product_id
            if not sat_product_id:
                raise UserError(_("Error!\nEl producto:\n %s \nNo cuenta con la Clave de Producto/Servicio del SAT." % line.product_id.name))
            sat_uom_id = line.product_uom_id.sat_uom_id
            if not sat_uom_id:
                raise UserError(_("Error!\nLa Unidad de Medida < %s > para el producto < %s > \nno tiene la Clave SAT asignada, por favor revise." % (line.product_uom_id.name, line.product_id.name)))
            ## METODO PARA AÑADIR COMPLEMENTOS ##
            # self.add_complements_with_concept_cfdi(line, line.product_id )
            
            price_unit = line.quantity != 0 and line.price_subtotal / line.quantity or 0.0

            cantidad = "%.2f" % line.quantity or 0.0
            cantidad_qr = ""
            qr_cantidad_split = cantidad.split('.')
            decimales = qr_cantidad_split[1]
            index_zero = self.return_index_floats(decimales)
            decimales_res = decimales[0:index_zero+1]
            if decimales_res == '0':
                cantidad_qr = qr_cantidad_split[0]
            else:
                cantidad_qr = qr_cantidad_split[0]+"."+decimales_res


            concepto = {
                'ClaveProdServ': sat_product_id.code,
                'Cantidad': cantidad_qr,
                'ClaveUnidad': sat_uom_id.code,
                'Unidad': sat_uom_id.name,
                'Descripcion': line.name or '',
                'ValorUnitario': "%.2f" % (price_unit or 0.0),
                'Importe': "%.2f" % (line.price_subtotal or 0.0),
            # Falta el Descuento #
            }

            if line.discount:
                concepto.update({
                    'ValorUnitario': "%.2f" % ((line.amount_subtotal / line.quantity) or 0.0),
                    'Importe': "%.2f" % (line.amount_subtotal or 0.0),
                    'Descuento': "%.2f" % (line.amount_discount),
                    })

            ### Extension que permitira extender los modulos ###
            concepto = line.update_properties_concept(concepto)

            ### Añadiendo el No de Indentificacion
            product_code = ""
            try:
                _logger.info("line.product_id: %s" % line.product_id[line.product_id.no_identity_type])
                product_code = line.product_id[line.product_id.no_identity_type]
            except:
                if line.product_id.no_identity_type != 'none':
                    product_code = line.product_id.no_identity_other
            
            if line.product_id.no_identity_type:
                if line.product_id.no_identity_type != 'none':
                    if line.product_id.no_identity_type == 'default_code':
                        product_code = line.product_id.default_code 
                    elif line.product_id.no_identity_type == 'barcode':
                        product_code = line.product_id.barcode
                    else:
                        product_code = line.product_id.no_identity_other

            if product_code:
                concepto.update({'NoIdentificacion': product_code})            

            price_unit = line.price_unit * (1 - (line.discount or 0.0) / 100.0)

            ##################
            taxes_line = line.filtered('price_subtotal').tax_ids.flatten_taxes_hierarchy()
            ##################

            ### Si hay impuestos en el Concepto agregamos el nodo, si no se omite
            if taxes_line:
                concepto.update({'cfdi:Impuestos':{}})
                impuestos_traslados = concepto['cfdi:Impuestos'].setdefault(
                            'cfdi:Traslados', [])
                impuestos_retenciones = concepto['cfdi:Impuestos'].setdefault(
                        'cfdi:Retenciones', [])
            
            for tax in taxes_line:
                if not tax.sat_tasa_cuota:
                    raise UserError(_("Error no cuentas con el valor Tasa/Cuota del Impuesto:\n%s" % tax.name))
                if not tax.sat_code_tax:
                    raise UserError(_("Error no cuentas con el valor Clave de Impuesto SAT del Impuesto:\n%s" % tax.name))

                ## Definiendo el Tipo de Impuesto #
                ## Montos Positivos Traslados ###
                if tax.amount >= 0:
                    if tax.sat_tasa_cuota == 'Tasa':
                        tax_importe = tax.amount / 100.0 * line.price_subtotal
                    elif tax.sat_tasa_cuota =='Cuota':
                        tax_importe = tax.amount
                    else:
                        continue
                    ## Comienza por Detalle #
                    impuesto_dict = {
                        'cfdi:Traslado':
                        {
                            'Base': "%.2f" % (line.price_subtotal or 0.0),
                            'Impuesto': tax.sat_code_tax,
                            'TipoFactor': tax.sat_tasa_cuota,
                            'TasaOCuota': "%.6f" % (tax.amount/100.0),
                            'Importe': "%.2f" % tax_importe,
                        }
                    }
                    
                    impuestos_traslados.append(impuesto_dict)
                else:
                    ## Comienza por Detalle ##
                    
                    if tax.sat_tasa_cuota == 'Tasa':
                        tax_importe = abs(tax.amount) / 100.0 * line.price_subtotal
                    elif tax.sat_tasa_cuota =='Cuota':
                        tax_importe = abs(tax.amount)
                    else:
                        continue
                        
                    impuesto_dict = {
                        'cfdi:Retencion':
                        {
                            'Base': "%.2f" % (line.price_subtotal or 0.0),
                            'Impuesto': tax.sat_code_tax,
                            'TipoFactor': tax.sat_tasa_cuota,
                            'TasaOCuota': "%.6f" % (abs(tax.amount) / 100.0),
                            'Importe': "%.2f" % tax_importe,
                        }
                    }

                    impuestos_retenciones.append(impuesto_dict)
            if 'cfdi:Impuestos' in concepto:
                if not concepto['cfdi:Impuestos']['cfdi:Traslados']:
                    concepto['cfdi:Impuestos'].pop('cfdi:Traslados')
                if not concepto['cfdi:Impuestos']['cfdi:Retenciones']:
                    concepto['cfdi:Impuestos'].pop('cfdi:Retenciones')

                
            if 'import_ids' in line._fields and line.import_ids:
                info_aduanera = []
                if self.cfdi_complemento != 'comercio_exterior':
                    for pedimento in line.import_ids:
                        informacion_aduanera = {
                            'NumeroPedimento': pedimento.name or '',
                        }
                        info_aduanera.append(informacion_aduanera)
                    if info_aduanera:
                        concepto.update({'cfdi:InformacionAduanera': info_aduanera})

                        
            if sat_product_id.complemento_que_debe_incluir:
                concepto = line.add_complements_with_concept_cfdi(concepto)
                #invoice_data['cfdi:Conceptos'].append({'cfdi:Concepto': node_with_complement})
                #if not node_with_complement:
                #    raise UserError(_("Error!\nLa clave:\n %s\nDel Producto:\n %s\nDispara un complemento, el cual no esta establecido, desactive esta opción o genere un complemento." % ("[ "+sat_product_id.code+" ] "+sat_product_id.name,line.product_id.name)))

            ### Agregando  el Concepto al listado de Conceptos ####
            invoice_data['cfdi:Conceptos'].append({'cfdi:Concepto': concepto})

            # Termina seccion: Conceptos
        
        # Inicia seccion: impuestos
        # Si hay impuestos en la Fatura se agrega el nodo de Impuestos
        taxes = self._get_global_taxes()
        if taxes:
            invoice_data['cfdi:Impuestos'] = {}
            
            if 'total_impuestos' in taxes:
                invoice_data['cfdi:Impuestos'].update({
                    'TotalImpuestosTrasladados': "%.2f"%( taxes['total_impuestos'] or 0.0),
                })
                
                invoice_data['cfdi:Impuestos'].update({'cfdi:Traslados' : []})
                #impuesto_list = invoice_data_impuestos.setdefault('cfdi:Traslados', [])
                for tax_line in taxes['impuestos']:
                    invoice_data['cfdi:Impuestos']['cfdi:Traslados'].append(
                        {'cfdi:Traslado' : {
                            'Impuesto': tax_line['sat_code_tax'],
                            'TipoFactor': tax_line['type'],
                            'TasaOCuota': "%.6f" % abs(tax_line['rate']),
                            'Importe': "%.2f" % abs(tax_line['tax_amount'])}
                        })
            if 'total_retenciones' in taxes:
                if 'total_retenciones' in taxes and taxes['total_retenciones'] > 0.0:
                    invoice_data['cfdi:Impuestos'].update({
                        'TotalImpuestosRetenidos': "%.2f"%( taxes['total_retenciones'] or 0.0 )
                    })
                    invoice_data['cfdi:Impuestos'].update({'cfdi:Retenciones' : []})
                    for tax_line in taxes['retenciones']:
                        invoice_data['cfdi:Impuestos']['cfdi:Retenciones'].append(
                            {'cfdi:Retencion' : {
                                'Impuesto': tax_line['sat_code_tax'],
                                #'TipoFactor': tax_line['type'],
                                #'TasaOCuota': "%.6f" % abs(tax_line['rate']),
                                'Importe': "%.2f" % abs(tax_line['tax_amount'])}
                            })

        
        # Termina seccion: impuestos
        if 'cfdi_complemento' in self._fields and self.cfdi_complemento:
            invoice_data_parent = invoice._get_einvoice_complement_dict(invoice_data_parent)
        invoice_data_parents.append(invoice_data_parent)
        invoice_data_parent['state'] = invoice.state
        invoice_data_parent['invoice_id'] = invoice.id
        invoice_data_parent['type'] = invoice.move_type
        invoice_data_parent['invoice_datetime'] = invoice.invoice_datetime
        invoice_data_parent['date_invoice_tz'] = invoice.date_invoice_tz
        invoice_data_parent['currency_id'] = invoice.currency_id.id
        

        date_ctx = {'date': invoice.date_invoice_tz.date() or False}

        currency = self.currency_id
        rate = self.currency_id.with_context(date_ctx).rate
        rate = rate != 0 and 1.0/rate or 0.0

        invoice_data_parent['rate'] = rate

        if not invoice_data_parents[0].get('invoice_datetime', False):
            raise UserError(_("Fecha de Factura vacía!\nNo es posible obtener la información sin la fecha, asegúrese que el Estado de la factura no es Borrador o que la Fecha Factura se encuentre vacía"))

        return invoice_data_parents
