# -*- encoding: utf-8 -*-
from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError, RedirectWarning, ValidationError
import datetime
from pytz import timezone
import pytz
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
import zipfile
import base64
from xml.dom.minidom import parse, parseString
import time
import csv
import tempfile
import os
import io
import sys
import codecs
from xml.dom import minidom
from datetime import datetime, timedelta
import time
from suds.client import Client, WebFault
import suds
import qrcode
from suds.plugin import MessagePlugin
import logging
_logger = logging.getLogger(__name__)

class LogPlugin(MessagePlugin):
    def sending(self, context):
        _logger.info(str(context.envelope))
        #print(str(context.envelope))
        return
    def received(self, context):
        _logger.info(str(context.reply))
        #print(str(context.reply))
        return

production_url  = 'https://sat.sifei.com.mx:8443/SIFEI/SIFEI?wsdl'
testing_url     = 'http://devcfdi.sifei.com.mx:8080/SIFEI33/SIFEI?wsdl'

cancel_production_url  = 'https://sat.sifei.com.mx:9000/CancelacionSIFEI/Cancelacion?wsdl'
cancel_testing_url     = 'http://devcfdi.sifei.com.mx:8888/CancelacionSIFEI/Cancelacion?wsdl'   
    
class AccountInvoice(models.Model):
    _inherit = 'account.move'

    

    def add_node(self, node_name=None, attrs=None, parent_node=None,
                 minidom_xml_obj=None, attrs_types=None, order=False):
        """
            @params node_name : Name node to added
            @params attrs : Attributes to add in node
            @params parent_node : Node parent where was add new node children
            @params minidom_xml_obj : File XML where add nodes
            @params attrs_types : Type of attributes added in the node
            @params order : If need add the params in order in the XML, add a
                    list with order to params
        """
        if not order:
            order = attrs
        new_node = minidom_xml_obj.createElement(node_name)
        for key in order:
            if attrs_types[key] == 'attribute':
                new_node.setAttribute(key, attrs[key])
            elif attrs_types[key] == 'textNode':
                key_node = minidom_xml_obj.createElement(key)
                text_node = minidom_xml_obj.createTextNode(attrs[key])

                key_node.appendChild(text_node)
                new_node.appendChild(key_node)
        parent_node.appendChild(new_node)
        return new_node

    
    def add_addenda_xml(self, xml_res_str=None, comprobante=None):
        return xml_res_str
        
    
    def _get_type_sequence(self):
        return 'cfdi:Comprobante'

    
    
    def get_driver_cfdi_sign(self):
        factura_mx_type__fc = super(AccountInvoice, self).get_driver_cfdi_sign()
        if factura_mx_type__fc == None:
            factura_mx_type__fc = {}
        factura_mx_type__fc.update({'pac_sifei': self.action_get_stamp_sifei})
        return factura_mx_type__fc
    
    
    def get_driver_cfdi_cancel(self):
        factura_mx_type__fc = super(AccountInvoice, self).get_driver_cfdi_cancel()
        if factura_mx_type__fc == None:
            factura_mx_type__fc = {}
        factura_mx_type__fc.update({'pac_sifei': self.action_cancel_stamp_sifei})
        return factura_mx_type__fc
        
    
    def action_cancel_stamp_sifei(self):
        msg = ''
        if (self.company_id.pac_testing and self.company_id.pac_user_4_testing and \
            self.company_id.pac_password_4_testing and  self.company_id.pac_equipo_id_4_testing) or \
            (not self.company_id.pac_testing and self.company_id.pac_user and \
             self.company_id.pac_password and self.company_id.pac_equipo_id):
            file_globals = self._get_file_globals()
            user        = self.company_id.pac_testing and self.company_id.pac_user_4_testing or self.company_id.pac_user
            password    = self.company_id.pac_testing and self.company_id.pac_password_4_testing or self.company_id.pac_password
            equipo_id   = self.company_id.pac_testing and self.company_id.pac_equipo_id_4_testing or self.company_id.pac_equipo_id
            wsdl_url    = self.company_id.pac_testing and testing_url or production_url
            #fname_pfx = open(file_globals['fname_pfx'], "rb")
            #certificate_pfx = fname_pfx.read()
            #fname_pfx.close()
            #certificate_pfx = self.journal_id.certificate_pfx_file.decode("utf-8")
            certificate_pfx = self.journal_id.certificate_pfx_file
            client = Client(wsdl_url, plugins=[LogPlugin()])
            try:
                resultado = client.service.cancelaCFDI(user, password, self.company_id.partner_id.vat_split,
                                                       certificate_pfx, file_globals['password'], self.cfdi_folio_fiscal)
            except WebFault as f:
                raise UserError(_('Advertencia !!!\nOcurrió un error al intentar Cancelar el Timbre. \n\nCódigo: %s\nError: %s\nMensaje: %s') % 
                                (f.fault.detail.SifeiException.codigo,f.fault.detail.SifeiException.error, f.fault.detail.SifeiException.message))
            
            msg += _('Resultado: %s') % (resultado)
        else:
            msg = _('No se configuró correctamente los datos del Webservice del PAC, revise los parámetros del PAC')
        return {'message': msg, 'status_uuid': self.cfdi_folio_fiscal, 'status': True}
    
    
    
    def action_get_stamp_sifei(self, fdata=None):
        """
        @params fdata : File.xml codification in base64
        """
        context = self._context.copy() or {}
        invoice = self
        comprobante = self._get_type_sequence()
        cfd_data = base64.decodebytes(fdata or self.xml_file_no_sign_index)
        xml_res_str = parseString(cfd_data)
        xml_res_addenda = self.add_addenda_xml(xml_res_str, comprobante)
        
        xml_res_str_addenda = xml_res_addenda.toxml('UTF-8')
        xcodecs = codecs.BOM_UTF8
        xcodecs = xcodecs.decode("UTF-8")
        xml_res_str_addenda = xml_res_str_addenda.decode("UTF-8").replace(xcodecs, '')
        
        file = False
        msg = ''
        cfdi_xml = False
        
        if (self.company_id.pac_testing and self.company_id.pac_user_4_testing and \
            self.company_id.pac_password_4_testing and  self.company_id.pac_equipo_id_4_testing) or \
            (not self.company_id.pac_testing and self.company_id.pac_user and \
             self.company_id.pac_password and self.company_id.pac_equipo_id):
            file_globals = self._get_file_globals()
            user        = self.company_id.pac_testing and self.company_id.pac_user_4_testing or self.company_id.pac_user
            password    = self.company_id.pac_testing and self.company_id.pac_password_4_testing or self.company_id.pac_password
            equipo_id   = self.company_id.pac_testing and self.company_id.pac_equipo_id_4_testing or self.company_id.pac_equipo_id
            wsdl_url    = self.company_id.pac_testing and testing_url or production_url
                        
            if 'devcfdi' in wsdl_url:
                msg += _('ADVERTENCIA, TIMBRADO EN PRUEBAS!!!!\n\n')

            # -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-    
            ## Archivo a Timbrar ###
            (fileno, fname_xml) = tempfile.mkstemp(".xml", "odoo_xml_to_sifei__")
            f_argil = open(fname_xml, 'w')
            f_argil.write(xml_res_str_addenda)
            f_argil.close()
            os.close(fileno)

            xres = os.system("zip -j " + fname_xml.split('.')[0] + ".zip " + fname_xml + " > /dev/null")
            
            zipped_xml_file = open(fname_xml.split('.')[0] + ".zip", 'rb')
            cfdi_zipped = base64.b64encode(zipped_xml_file.read())
            zipped_xml_file.close()

            client = Client(wsdl_url, plugins=[LogPlugin()])
            w,f = False, False
            try:
                resultado = client.service.getCFDI(user, password, cfdi_zipped.decode("utf-8"), ' ', equipo_id)
            except WebFault as w:
                f = w

            if f:
                raise UserError(_('Advertencia !!!\nOcurrió un error al intentar obtener el Timbre. \n\nCódigo: %s\nError: %s\nMensaje: %s') % 
                                (f.fault.detail.SifeiException.codigo,f.fault.detail.SifeiException.error, f.fault.detail.SifeiException.message))
            
            #fname_stamped_zip = self.binary2file(b'', b'odoo_' + str.encode(self.fname_invoice) + b'_stamped', b'.zip')
            
            fstamped = io.BytesIO(base64.b64decode(str.encode(resultado)))
            
            zipf = zipfile.ZipFile(fstamped, 'r')
            zipf1 = zipf.open(zipf.namelist()[0])
            xml_timbrado_str = zipf1.read().replace(b'\r',b'').replace(b'\n',b'')
            xml_timbrado = parseString(xml_timbrado_str)
            timbre = xml_timbrado.getElementsByTagName('tfd:TimbreFiscalDigital')[0]
                
            # -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-
            htz=abs(int(self._get_time_zone()))
            mensaje = 'Proceso de timbrado exitoso...'
            folio_fiscal = timbre.attributes['UUID'].value            
            fecha_timbrado = timbre.attributes['FechaTimbrado'].value or False
            fecha_timbrado = fecha_timbrado and time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(fecha_timbrado[:19], '%Y-%m-%dT%H:%M:%S')) or False
            fecha_timbrado = fecha_timbrado and datetime.strptime(fecha_timbrado, '%Y-%m-%d %H:%M:%S') + timedelta(hours=htz) or False
            cfdi_no_certificado = timbre.attributes['NoCertificadoSAT'].value
            cfdi_cbb = self.create_qr_image(cfd_data, self.amount_total, timbre.attributes['UUID'].value)
            cfdi_sello =  timbre.attributes['SelloSAT'].value
            cfdi_data = {
                'cfdi_cbb': cfdi_cbb or False,
                'cfdi_sello': cfdi_sello or False,
                'cfdi_no_certificado': cfdi_no_certificado or False,
                'cfdi_fecha_timbrado': fecha_timbrado,
                'cfdi_xml': xml_timbrado_str, 
                'cfdi_folio_fiscal': folio_fiscal,
            }
            msg += mensaje + ". Folio Fiscal: " + folio_fiscal + "."
            msg += _(u"\nPor favor asegúrese que la estructura del XML de la factura ha sido generada correctamente en el SAT\nhttps://www.consulta.sat.gob.mx/sicofi_web/moduloECFD_plus/ValidadorCFDI/Validador%20cfdi.html")
            if cfdi_data.get('cfdi_xml', False):
                file = base64.encodebytes(cfdi_data['cfdi_xml'] or '')
                cfdi_xml = cfdi_data.pop('cfdi_xml')
            if cfdi_xml:
                self.write(cfdi_data)
                cfdi_data['cfdi_xml'] = cfdi_xml
            else:
                raise UserError(_('Advertencia !!!\nOcurrió un error al intentar timbrar, por favor revise el LOG'))
        else:
            msg += 'No se encontró información del PAC, revise la configuración'
            raise UserError(_('Advertencia !!!\nNo se encontró información del Webservice del PAC, revise la configuración'))
        return {'file': file, 'msg': msg, 'cfdi_xml': cfdi_xml.decode("utf-8")}

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

    def create_qr_image(self, cfdi_xml, amount_total, timbre_uuid):
        #Get info for QRC
        cfdi_minidom = minidom.parseString(cfdi_xml)
        
        node = cfdi_minidom.getElementsByTagName('cfdi:Comprobante')[0]
        subnode = node.getElementsByTagName('cfdi:Emisor')[0]
        # Para CFDI: https://verificacfdi.facturaelectronica.sat.gob.mx/default.aspx
        # Para retenciones: https://prodretencionverificacion.clouda.sat.gob.mx/
        url = "https://verificacfdi.facturaelectronica.sat.gob.mx/default.aspx"
        UUID = timbre_uuid

        qr_emisor = subnode.getAttribute('Rfc')        
        subnode = node.getElementsByTagName('cfdi:Receptor')[0]        
        qr_receptor = subnode.getAttribute('Rfc')
        total = "%.6f" % ( amount_total or 0.0)
        total_qr = ""
        qr_total_split = total.split('.')
        decimales = qr_total_split[1]
        index_zero = self.return_index_floats(decimales)
        decimales_res = decimales[0:index_zero+1]
        if decimales_res == '0':
            total_qr = qr_total_split[0]
        else:
            total_qr = qr_total_split[0]+"."+decimales_res

        last_8_digits_sello = ""

        timbre = cfdi_minidom.getElementsByTagName('cfdi:Comprobante')[0]
        cfdi_sello =  timbre.attributes['Sello'].value

        last_8_digits_sello = cfdi_sello[len(cfdi_sello)-8:]

        qr_string = '%s?id=%s&re=%s&rr=%s&tt=%s&fe=%s'% (url, UUID, qr_emisor, qr_receptor, total_qr, last_8_digits_sello)

        try:
            img = qrcode.make(qr_string.encode('utf-8'))
            output = io.BytesIO()
            img.save(output, format='JPEG')
            qr_bytes = base64.encodebytes(output.getvalue())
        except:
            raise UserError(_('Advertencia !!!\nNo se pudo crear el Código Bidimensional. Error %s') % e)
        return qr_bytes or False
    

###################################################
###################################################
class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    def add_addenda_xml(self, xml_res_str=None, comprobante=None):
        return xml_res_str
        

    def _get_type_sequence(self):
        return 'cfdi:Comprobante'

    
    def write_cfd_data(self, cfd_datas):
        cfd_datas = cfd_datas or {}
        comprobante = 'cfdi:Comprobante'
        data = {}

        cfd_data = cfd_datas
        noCertificado = cfd_data.get(comprobante, {}).get('NoCertificado', '')
        certificado = cfd_data.get(comprobante, {}).get('Certificado', '')
        sello = cfd_data.get(comprobante, {}).get('Sello', '')
        cadena_original = cfd_data.get('cadena_original', '')
        data = {
            'no_certificado': noCertificado,
            'certificado': certificado,
            'sello': sello,
            'cadena_original': cadena_original,
        }
        self.write(data)
        return True
    
    
    
    def get_driver_cfdi_sign(self):
        factura_mx_type__fc = super(AccountPayment, self).get_driver_cfdi_sign()
        if factura_mx_type__fc == None:
            factura_mx_type__fc = {}
        factura_mx_type__fc.update({'pac_sifei': self.action_get_stamp_sifei})
        return factura_mx_type__fc
    
    
    def get_driver_cfdi_cancel(self):
        factura_mx_type__fc = super(AccountPayment, self).get_driver_cfdi_cancel()
        if factura_mx_type__fc == None:
            factura_mx_type__fc = {}
        factura_mx_type__fc.update({'pac_sifei': self.action_cancel_stamp_sifei})
        return factura_mx_type__fc
        
    
    def action_cancel_stamp_sifei(self):
        msg = ''
        if (self.company_id.pac_testing and self.company_id.pac_user_4_testing and \
            self.company_id.pac_password_4_testing and  self.company_id.pac_equipo_id_4_testing) or \
            (not self.company_id.pac_testing and self.company_id.pac_user and \
             self.company_id.pac_password and self.company_id.pac_equipo_id):
            file_globals = self._get_file_globals()
            user        = self.company_id.pac_testing and self.company_id.pac_user_4_testing or self.company_id.pac_user
            password    = self.company_id.pac_testing and self.company_id.pac_password_4_testing or self.company_id.pac_password
            equipo_id   = self.company_id.pac_testing and self.company_id.pac_equipo_id_4_testing or self.company_id.pac_equipo_id
            # wsdl_url    = self.company_id.pac_testing and testing_url or production_url
            wsdl_url    = self.company_id.pac_testing and cancel_testing_url or cancel_production_url

            fname_pfx = open(file_globals['fname_pfx'], "rb")
            certificate_pfx = fname_pfx.read()
            fname_pfx.close()
            certificate_pfx = self.journal_id.certificate_pfx_file.decode("utf-8")
            client = Client(wsdl_url, plugins=[LogPlugin()])
            try:
                resultado = client.service.cancelaCFDI(user, password, self.company_id.partner_id.vat_split,
                                                       certificate_pfx, file_globals['password'], self.cfdi_folio_fiscal)
            except WebFault as f:
                raise UserError(_('Advertencia !!!\nOcurrió un error al intentar Cancelar el Timbre. \n\nCódigo: %s\nError: %s\nMensaje: %s') % 
                                (f.fault.detail.SifeiException.codigo,f.fault.detail.SifeiException.error, f.fault.detail.SifeiException.message))
            
            msg += _('Resultado: %s') % (resultado)
        else:
            msg = _('No se configuró correctamente los datos del Webservice del PAC, revise los parámetros del PAC')
        return {'message': msg, 'status_uuid': self.cfdi_folio_fiscal, 'status': True}
    
    
    
    def action_get_stamp_sifei(self, fdata=None):
        context = self._context.copy() or {}
        payment = self
        invoice_obj = self.env['account.move']
        comprobante = self._get_type_sequence()
        cfd_data = base64.decodebytes(fdata or self.xml_file_no_sign_index)
        xml_res_str = parseString(cfd_data)
        xml_res_addenda = self.add_addenda_xml(xml_res_str, comprobante)
        xml_res_str_addenda = xml_res_addenda.toxml('UTF-8')
        xml_res_str_addenda = xml_res_str_addenda.replace(codecs.BOM_UTF8, b'')
        ###############################
        file = False
        msg = ''
        cfdi_xml = False
        
        if (self.company_id.pac_testing and self.company_id.pac_user_4_testing and \
            self.company_id.pac_password_4_testing and  self.company_id.pac_equipo_id_4_testing) or \
            (not self.company_id.pac_testing and self.company_id.pac_user and \
             self.company_id.pac_password and self.company_id.pac_equipo_id):
            file_globals = self._get_file_globals()
            user        = self.company_id.pac_testing and self.company_id.pac_user_4_testing or self.company_id.pac_user
            password    = self.company_id.pac_testing and self.company_id.pac_password_4_testing or self.company_id.pac_password
            equipo_id   = self.company_id.pac_testing and self.company_id.pac_equipo_id_4_testing or self.company_id.pac_equipo_id
            wsdl_url    = self.company_id.pac_testing and testing_url or production_url
            
            if 'devcfdi' in wsdl_url:
                msg += _('ADVERTENCIA, TIMBRADO EN PRUEBAS!!!!\n\n')

            # -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-    
            ## Archivo a Timbrar ###
            (fileno, fname_xml) = tempfile.mkstemp(".xml", "odoo_xml_payment_to_sifei__")
            f_argil = open(fname_xml, 'w')
            f_argil.write(xml_res_str_addenda.decode("utf-8"))
            f_argil.close()
            os.close(fileno)

            xres = os.system("zip -j " + fname_xml.split('.')[0] + ".zip " + fname_xml + " > /dev/null")
            
            zipped_xml_file = open(fname_xml.split('.')[0] + ".zip", 'rb')
            cfdi_zipped = base64.b64encode(zipped_xml_file.read())
            zipped_xml_file.close()

            client = Client(wsdl_url, plugins=[LogPlugin()])
            w,f = False, False
            try:
                resultado = client.service.getCFDI(user, password, cfdi_zipped.decode("utf-8"), ' ', equipo_id)
            except WebFault as w:
                f = w

            if f:
                raise UserError(_('Advertencia !!!\nOcurrió un error al intentar obtener el Timbre. \n\nCódigo: %s\nError: %s\nMensaje: %s') % 
                                (f.fault.detail.SifeiException.codigo,f.fault.detail.SifeiException.error, f.fault.detail.SifeiException.message))
                
            #fname_stamped_zip = invoice_obj.binary2file(b'', b'odoo_' + str.encode(self.fname_payment) + b'_stamped', b'.zip')
            
            fstamped = io.BytesIO(base64.b64decode(str.encode(resultado)))
            
            zipf = zipfile.ZipFile(fstamped, 'r')
            zipf1 = zipf.open(zipf.namelist()[0])
            xml_timbrado_str = zipf1.read().replace(b'\r',b'').replace(b'\n',b'')
            xml_timbrado = parseString(xml_timbrado_str)
            timbre = xml_timbrado.getElementsByTagName('tfd:TimbreFiscalDigital')[0]
                
            # -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-
            htz=abs(int(self._get_time_zone()))
            mensaje = 'Proceso de timbrado exitoso...'
            folio_fiscal = timbre.attributes['UUID'].value            
            fecha_timbrado = timbre.attributes['FechaTimbrado'].value or False
            fecha_timbrado = fecha_timbrado and time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(fecha_timbrado[:19], '%Y-%m-%dT%H:%M:%S')) or False
            fecha_timbrado = fecha_timbrado and datetime.strptime(fecha_timbrado, '%Y-%m-%d %H:%M:%S') + timedelta(hours=htz) or False
            cfdi_no_certificado = timbre.attributes['NoCertificadoSAT'].value
            cfdi_cbb = invoice_obj.create_qr_image(cfd_data, self.amount, timbre.attributes['UUID'].value)
            cfdi_sello =  timbre.attributes['SelloSAT'].value
            cfdi_data = {
                'cfdi_cbb': cfdi_cbb or False,
                'cfdi_sello': cfdi_sello or False,
                'cfdi_no_certificado': cfdi_no_certificado or False,
                'cfdi_fecha_timbrado': fecha_timbrado,
                'cfdi_xml': xml_timbrado_str, 
                'cfdi_folio_fiscal': folio_fiscal,
            }
            msg += mensaje + ". Folio Fiscal: " + folio_fiscal + "."
            msg += _(u"\nPor favor asegúrese que la estructura del XML de la factura ha sido generada correctamente en el SAT\nhttps://www.consulta.sat.gob.mx/sicofi_web/moduloECFD_plus/ValidadorCFDI/Validador%20cfdi.html")
            if cfdi_data.get('cfdi_xml', False):
                #url_pac = '</"%s"><!--Para validar el XML CFDI puede descargar el certificado del PAC desde la siguiente liga: https://solucionfactible.com/cfdi/00001000000102699425.zip-->' % (comprobante)
                #cfdi_data['cfdi_xml'] = cfdi_data['cfdi_xml'].replace('</"%s">' % (comprobante), url_pac)
                file = base64.encodebytes(cfdi_data['cfdi_xml'] or '')
                # self.cfdi_data_write(cr, uid, [payment.id], cfdi_data, context=context)
                cfdi_xml = cfdi_data.pop('cfdi_xml')
            if cfdi_xml:
                self.write(cfdi_data)
                cfdi_data['cfdi_xml'] = cfdi_xml
            else:
                raise UserError(_('Advertencia !!!\nOcurrió un error al intentar timbrar, por favor revise el LOG'))
        else:
            msg += 'No se encontró información del PAC, revise la configuración'
            raise UserError(_('Advertencia !!!\nNo se encontró información del Webservice del PAC, revise la configuración'))
        #raise osv.except_osv('Pausa','Pausa')
        return {'file': file, 'msg': msg, 'cfdi_xml': cfdi_xml}

    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:    
