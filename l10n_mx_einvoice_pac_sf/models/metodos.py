# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError
import datetime
from pytz import timezone
import pytz
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

import base64
import xml.dom.minidom
import time
import csv
import tempfile
import os
import sys
import codecs
from xml.dom import minidom
from zeep import Client
import zeep
from datetime import datetime, timedelta
import time
import logging
_logger = logging.getLogger(__name__)

from zeep.plugins import HistoryPlugin

from lxml import etree

history = HistoryPlugin()

class AccountMove(models.Model):
    _inherit = 'account.move'

    production_url  = 'https://solucionfactible.com/ws/services/Timbrado?wsdl'
    testing_url     = 'https://testing.solucionfactible.com/ws/services/Timbrado?wsdl'

    
    def get_driver_cfdi_sign(self):
        factura_mx_type__fc = super(AccountMove, self).get_driver_cfdi_sign()
        if factura_mx_type__fc == None:
            factura_mx_type__fc = {}
        factura_mx_type__fc.update({'pac_sf': self.action_get_stamp_sf})
        return factura_mx_type__fc
    
    
    def get_driver_cfdi_cancel(self):
        factura_mx_type__fc = super(AccountMove, self).get_driver_cfdi_cancel()
        if factura_mx_type__fc == None:
            factura_mx_type__fc = {}
        factura_mx_type__fc.update({'pac_sf': self.action_cancel_stamp_sf})
        return factura_mx_type__fc
        
    
    def action_cancel_stamp_sf(self):
        msg = ''
        status = False
        if self.company_id.pac_testing or (self.company_id.pac_user and self.company_id.pac_password):
            file_globals = self._get_file_globals()
            user        = self.company_id.pac_testing and 'testing@solucionfactible.com' or self.company_id.pac_user
            password    = self.company_id.pac_testing and 'timbrado.SF.16672' or self.company_id.pac_password
            wsdl_url    = self.company_id.pac_testing and self.testing_url or self.production_url
            
            fcer = open(file_globals['fname_cer_no_pem'], "rb")
            fkey = open(file_globals['fname_key_no_pem'], "rb")
            cerCSD = fcer.read()
            keyCSD = fkey.read()
            fcer.close()
            fkey.close()
            contrasenaCSD = self.journal_id.certificate_password
            client = Client(wsdl_url, plugins=[history])
            isZipFile = 0
            if self.company_id.partner_id.vat == 'TBE740319AP4':
                contrasenaCSD += ' '
            try:
                uuid_cancelacion_motivo = '%s|%s|%s' % (self.cfdi_folio_fiscal, self.motivo_cancelacion, 
                                                 self.uuid_relacionado_cancelacion or '')
                resultado = client.service.cancelar(user, password, uuid_cancelacion_motivo, cerCSD, keyCSD, contrasenaCSD)
                
                envelope_pretty_xml = etree.tostring(history.last_sent["envelope"], encoding="unicode", pretty_print=True)
                response_pretty_xml = etree.tostring(history.last_received["envelope"], encoding="unicode", pretty_print=True)

                _logger.info("\nEnvelope: %s " % envelope_pretty_xml)
                _logger.info("\nResponse: %s " % response_pretty_xml)

            except WebFault as f:
                raise UserError(_('Advertencia !!!\nOcurrió un error al intentar Cancelar el CFDI.'))
            
            if resultado.status == 200:
                msg +=  '\n- Cancelación Exitosa.\n- UUID Cancelado es: %s\nMensaje: %s' % (self.cfdi_folio_fiscal, resultado.resultados[0].mensaje)
                status_uuid = resultado.resultados[0].statusUUID
                status = True
            else:
                raise UserError(_('Advertencia!\nCódigo de Cancelación: %s. - Mensaje: %s') % (resultado.status, resultado.mensaje))
        else:
            msg = _('No se configuró correctamente los datos del PAC, revise los parámetros del PAC')
        return {'message': msg, 'status_uuid': status_uuid, 'status': status}
    
    
    
    def action_get_stamp_sf(self, fdata=None):
        context = self._context.copy() or {}
        invoice = self
        comprobante = 'cfdi:Comprobante'
        cfd_data = base64.decodebytes(fdata or self.xml_file_no_sign_index)
        #cfd_data = (fdata or self.xml_file_no_sign_index)
        #_logger.info("\ncfd_data: %s" % cfd_data)
        xml_res_str = xml.dom.minidom.parseString(cfd_data)
        xml_res_addenda = xml_res_str # self.add_addenda_xml(xml_res_str, comprobante)
        xml_res_str_addenda = xml_res_addenda.toxml('UTF-8')
        xml_res_str_addenda = xml_res_str_addenda.replace(codecs.BOM_UTF8, b'')

        compr = xml_res_addenda.getElementsByTagName(comprobante)[0]
        date = compr.attributes['Fecha'].value
        date_format = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d')
        context['date'] = date_format
        invoice_ids = [invoice.id]
        file = False
        msg = ''
        cfdi_xml = False
        if self.company_id.pac_testing or (self.company_id.pac_user and self.company_id.pac_password):
            user        = self.company_id.pac_testing and 'testing@solucionfactible.com' or self.company_id.pac_user
            password    = self.company_id.pac_testing and 'timbrado.SF.16672' or self.company_id.pac_password
            wsdl_url    = self.company_id.pac_testing and self.testing_url or self.production_url
            
            if 'testing' in wsdl_url:
                msg += _('ADVERTENCIA, TIMBRADO EN PRUEBAS!!!!\n\n')            
            cfdi = xml_res_str_addenda            
            client = Client(wsdl_url, plugins=[history])
            isZipFile = 0
            try:
                resultado = client.service.timbrar(user, password, cfdi, isZipFile)
                
                envelope_pretty_xml = etree.tostring(history.last_sent["envelope"], encoding="unicode", pretty_print=True)
                response_pretty_xml = etree.tostring(history.last_received["envelope"], encoding="unicode", pretty_print=True)

                _logger.info("\nEnvelope: %s " % envelope_pretty_xml)
                _logger.info("\nResponse: %s " % response_pretty_xml)

            except WebFault as f:
                raise UserError(_('Advertencia !!!\nOcurrió un error al intentar obtener el Timbre. \n\nCódigo: %s\nError: %s\nMensaje: %s') % 
                                (f.fault.detail.SifeiException.codigo,f.fault.detail.SifeiException.error, f.fault.detail.SifeiException.message))
            _logger.info("resultado: %s" % resultado)
            htz = int(self._get_time_zone())
            resultados_mensaje = resultado.resultados[0].mensaje or ''
            folio_fiscal = resultado.resultados[0].uuid or ''
            codigo_timbrado = resultado.resultados[0].status or ''
            mensaje = resultado.resultados[0].mensaje
            if codigo_timbrado == 200 and folio_fiscal:
                fecha_timbrado = resultado.resultados[0].fechaTimbrado and resultado.resultados[0].fechaTimbrado.replace(tzinfo=None) or False
                cfdi_data = {
                    'cfdi_cbb': base64.encodebytes(resultado.resultados[0].qrCode) or False,  # ya lo regresa en base64
                    'cfdi_sello': resultado.resultados[0].selloSAT or False,
                    'cfdi_no_certificado': resultado.resultados[0].certificadoSAT or False,
                    'cfdi_fecha_timbrado': fecha_timbrado,
                    'cfdi_xml': resultado.resultados[0].cfdiTimbrado.decode("utf-8")  or b'',  #base64.decodebytes(resultado.resultados[0].cfdiTimbrado or b''), 
                    'cfdi_folio_fiscal': resultado.resultados[0].uuid or '',
                    #'pac_id': pac_params.id,
                }
                msg += mensaje + "." + resultados_mensaje + " Folio Fiscal: " + folio_fiscal + "."
                msg += _(u"\nPor favor asegúrese que la estructura del XML de la factura ha sido generada correctamente en el SAT\nhttps://www.consulta.sat.gob.mx/sicofi_web/moduloECFD_plus/ValidadorCFDI/Validador%20cfdi.html")
                if cfdi_data.get('cfdi_xml', False):
                    #url_pac = '</"%s"><!--Para validar el XML CFDI puede descargar el certificado del PAC desde la siguiente liga: https://solucionfactible.com/cfdi/00001000000102699425.zip-->' % (comprobante)
                    #cfdi_data['cfdi_xml'] = cfdi_data['cfdi_xml'].replace(b'</"%s">' % (comprobante), url_pac)
                    file = base64.encodebytes(str.encode(cfdi_data['cfdi_xml'])) or ''
                    # self.cfdi_data_write(cr, uid, [invoice.id], cfdi_data, context=context)
                    cfdi_xml = cfdi_data.pop('cfdi_xml')
                if cfdi_xml:
                    self.write(cfdi_data)
                    cfdi_data['cfdi_xml'] = cfdi_xml
                else:
                    msg += _("No puedo extraer el archivo XML del PAC")
            else:
                msg += _('Advertencia !!!\nCódigo Sellado: %s. - Código Validación: %s. - Folio Fiscal: %s. - Mensaje: %s. - Mensaje de Validación: %s.') % (
                    codigo_timbrado, resultado.resultados[0].status, folio_fiscal, mensaje, resultados_mensaje)

        else:
            msg += 'No se encontró información del Webservice del PAC, revise la configuración'
            raise UserError(_('Advertencia !!!\nNo se encontró información del Webservice del PAC, revise la configuración'))
        #raise osv.except_osv('Pausa','Pausa')
        return {'file': file, 'msg': msg, 'cfdi_xml': cfdi_xml}
    

###################################################
###################################################
class AccountPayment(models.Model):
    _inherit = 'account.payment'


    production_url  = 'https://solucionfactible.com/ws/services/Timbrado?wsdl'
    testing_url     = 'https://testing.solucionfactible.com/ws/services/Timbrado?wsdl'

    

    
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
        factura_mx_type__fc.update({'pac_sf': self.action_get_stamp_sf})
        return factura_mx_type__fc
    
    
    def get_driver_cfdi_cancel(self):
        factura_mx_type__fc = super(AccountPayment, self).get_driver_cfdi_cancel()
        if factura_mx_type__fc == None:
            factura_mx_type__fc = {}
        factura_mx_type__fc.update({'pac_sf': self.action_cancel_stamp_sf})
        return factura_mx_type__fc
        

    
    def action_cancel_stamp_sf(self):
        msg = ''
        status = False
        if self.company_id.pac_testing or (self.company_id.pac_user and self.company_id.pac_password):
            file_globals = self._get_file_globals()
            user        = self.company_id.pac_testing and 'testing@solucionfactible.com' or self.company_id.pac_user
            password    = self.company_id.pac_testing and 'timbrado.SF.16672' or self.company_id.pac_password
            wsdl_url    = self.company_id.pac_testing and self.testing_url or self.production_url
            
            fcer = open(file_globals['fname_cer_no_pem'], "rb")
            fkey = open(file_globals['fname_key_no_pem'], "rb")
            cerCSD = fcer.read()
            keyCSD = fkey.read()
            fcer.close()
            fkey.close()
            contrasenaCSD = self.journal_id.certificate_password
            client = Client(wsdl_url, plugins=[history])
            isZipFile = 0
            if self.company_id.partner_id.vat == 'TBE740319AP4':
                contrasenaCSD += ' '
            try:
                uuid_cancelacion_motivo = '%s|%s|%s' % (self.cfdi_folio_fiscal, self.motivo_cancelacion, 
                                                 self.uuid_relacionado_cancelacion or '')
                resultado = client.service.cancelar(user, password, uuid_cancelacion_motivo, cerCSD, keyCSD, contrasenaCSD)
                
                envelope_pretty_xml = etree.tostring(history.last_sent["envelope"], encoding="unicode", pretty_print=True)
                response_pretty_xml = etree.tostring(history.last_received["envelope"], encoding="unicode", pretty_print=True)

                _logger.info("\nEnvelope: %s " % envelope_pretty_xml)
                _logger.info("\nResponse: %s " % response_pretty_xml)
                        
            except WebFault as f:
                raise UserError(_('Advertencia !!!\nOcurrió un error al intentar obtener el Timbre. \n\nCódigo: %s\nError: %s\nMensaje: %s') % 
                                (f.fault.detail.SifeiException.codigo,f.fault.detail.SifeiException.error, f.fault.detail.SifeiException.message))
            _logger.info("resultado: %s" % resultado)
            if resultado.status == 200:
                msg +=  '\n- Cancelación Exitosa.\n- UUID Cancelado es: %s\nMensaje: %s' % (self.cfdi_folio_fiscal, resultado.resultados[0].mensaje)
                status_uuid = resultado.resultados[0].statusUUID or 'OK'
                status = True
            else:
                raise UserError(_('Advertencia!\nCódigo de Cancelación: %s. - Mensaje: %s') % (resultado.status, resultado.mensaje))
        else:
            msg = _('No se configuró correctamente los datos del PAC, revise los parámetros del PAC')
        return {'message': msg, 'status_uuid': status_uuid, 'status': status}
    
    

    
    def action_get_stamp_sf(self, fdata=None):
        context = self._context.copy() or {}
        payment = self
        comprobante = 'cfdi:Comprobante'
        cfd_data = base64.decodebytes(fdata or self.xml_file_no_sign_index)
        xml_res_str = xml.dom.minidom.parseString(cfd_data)
        xml_res_addenda = xml_res_str #self.add_addenda_xml(xml_res_str, comprobante)
        xml_res_str_addenda = xml_res_addenda.toxml('UTF-8')
        xml_res_str_addenda = xml_res_str_addenda.replace(codecs.BOM_UTF8, b'')

        compr = xml_res_addenda.getElementsByTagName(comprobante)[0]
        date = compr.attributes['Fecha'].value
        date_format = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d')
        context['date'] = date_format
        payment_ids = [payment.id]
        file = False
        msg = ''
        cfdi_xml = False
        if self.company_id.pac_testing or (self.company_id.pac_user and self.company_id.pac_password):
            user        = self.company_id.pac_testing and 'testing@solucionfactible.com' or self.company_id.pac_user
            password    = self.company_id.pac_testing and 'timbrado.SF.16672' or self.company_id.pac_password
            wsdl_url    = self.company_id.pac_testing and self.testing_url or self.production_url
            
            if 'testing' in wsdl_url:
                msg += _('ADVERTENCIA, TIMBRADO EN PRUEBAS!!!!\n\n')
                        
            cfdi = xml_res_str_addenda            
            client = Client(wsdl_url, plugins=[history])
            isZipFile = 0
            try:
                resultado = client.service.timbrar(user, password, cfdi, isZipFile)
                
                envelope_pretty_xml = etree.tostring(history.last_sent["envelope"], encoding="unicode", pretty_print=True)
                response_pretty_xml = etree.tostring(history.last_received["envelope"], encoding="unicode", pretty_print=True)

                _logger.info("\nEnvelope: %s " % envelope_pretty_xml)
                _logger.info("\nResponse: %s " % response_pretty_xml)

            except WebFault as f:
                raise UserError(_('Advertencia !!!\nOcurrió un error al intentar obtener el Timbre. \n\nCódigo: %s\nError: %s\nMensaje: %s') % 
                                (f.fault.detail.SifeiException.codigo,f.fault.detail.SifeiException.error, f.fault.detail.SifeiException.message))            
            
            htz = int(self._get_time_zone())
            resultados_mensaje = resultado.resultados[0].mensaje or ''
            folio_fiscal = resultado.resultados[0].uuid or ''
            codigo_timbrado = resultado.status or ''
            mensaje = resultado.mensaje
            _logger.info("\nresultado: %s\nresultados: %s" % (resultado, resultado.resultados))
            if codigo_timbrado == 200 and resultado.resultados[0].status == 200:
                fecha_timbrado = resultado.resultados[0].fechaTimbrado and resultado.resultados[0].fechaTimbrado.replace(tzinfo=None) or False
                cfdi_data = {
                    'cfdi_cbb': base64.encodebytes(resultado.resultados[0].qrCode) or False,  # ya lo regresa en base64
                    'cfdi_sello': resultado.resultados[0].selloSAT or False,
                    'cfdi_no_certificado': resultado.resultados[0].certificadoSAT or False,
                    'cfdi_fecha_timbrado': fecha_timbrado,
                    'cfdi_xml': resultado.resultados[0].cfdiTimbrado.decode("utf-8")  or b'', 
                    'cfdi_folio_fiscal': resultado.resultados[0].uuid or '',
                }
                msg += mensaje + "." + resultados_mensaje + " Folio Fiscal: " + folio_fiscal + "."
                msg += _(u"\nPor favor asegúrese que la estructura del XML de la factura ha sido generada correctamente en el SAT\nhttps://www.consulta.sat.gob.mx/sicofi_web/moduloECFD_plus/ValidadorCFDI/Validador%20cfdi.html")
                if cfdi_data.get('cfdi_xml', False):
                    file = base64.encodebytes(str.encode(cfdi_data['cfdi_xml'])) or ''
                    cfdi_xml = cfdi_data.pop('cfdi_xml')
                if cfdi_xml:
                    self.write(cfdi_data)
                    cfdi_data['cfdi_xml'] = str.encode(cfdi_xml)
                else:
                    msg += _("No puedo extraer el archivo XML del PAC")
            else:
                msg += _('Advertencia !!!\nCódigo Sellado: %s. - Código Validación: %s. - Folio Fiscal: %s. - Mensaje: %s. - Mensaje de Validación: %s.') % (
                    codigo_timbrado, resultado.resultados[0].status, folio_fiscal, mensaje, resultados_mensaje)
        else:
            msg += 'No se encontró información del Webservice del PAC, revise la configuración'
            raise UserError(_('Advertencia !!!\nNo se encontró información del Webservice del PAC, revise la configuración'))
        #raise osv.except_osv('Pausa','Pausa')
        return {'file': file, 'msg': msg, 'cfdi_xml': cfdi_xml}
        
        #################################
        
        context = self._context.copy() or {}
        
        payment = self
        comprobante = 'cfdi:Comprobante'
        cfd_data = base64.decodebytes(fdata or self.xml_file_no_sign_index)
        xml_res_str = xml.dom.minidom.parseString(cfd_data)
        xml_res_addenda = xml_res_str # self.add_addenda_xml(xml_res_str, comprobante)
        xml_res_str_addenda = xml_res_addenda.toxml('UTF-8')
        xml_res_str_addenda = xml_res_str_addenda.replace(codecs.BOM_UTF8, '')


        compr = xml_res_addenda.getElementsByTagName(comprobante)[0]
        date = compr.attributes['Fecha'].value
        date_format = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d')
        context['date'] = date_format
        payment_ids = [payment.id]
        file = False
        msg = ''
        cfdi_xml = False
        #pac_params = self.env['params.pac'].search([('method_type', '=', 'pac_sf_firmar'), 
        #                                            ('company_id', '=', payment.company_emitter_id.id)], limit=1)
        if self.company_id.pac_testing or (self.company_id.pac_user and self.company_id.pac_password):
            user        = self.company_id.pac_testing and 'testing@solucionfactible.com' or self.company_id.pac_user
            password    = self.company_id.pac_testing and 'timbrado.SF.16672' or self.company_id.pac_password
            wsdl_url    = self.company_id.pac_testing and self.testing_url or self.production_url
            
            if 'testing' in wsdl_url:
                msg += _('ADVERTENCIA, TIMBRADO EN PRUEBAS!!!!\n\n')
            wsdl_client = WSDL.SOAPProxy(wsdl_url, namespace)
            if True:  # if wsdl_client:
                file_globals = self._get_file_globals()
                fname_cer_no_pem = file_globals['fname_cer']
                cerCSD = fname_cer_no_pem and base64.encodebytes(open(fname_cer_no_pem, "r").read()) or ''
                fname_key_no_pem = file_globals['fname_key']
                keyCSD = fname_key_no_pem and base64.encodebytes(open(fname_key_no_pem, "r").read()) or ''
                cfdi = base64.encodebytes(xml_res_str_addenda)
                zip = False  # Validar si es un comprimido zip, con la extension del archivo
                contrasenaCSD = file_globals.get('password', '')
                params = [user, password, cfdi, zip]
                wsdl_client.soapproxy.config.dumpSOAPOut = 0
                wsdl_client.soapproxy.config.dumpSOAPIn = 0
                wsdl_client.soapproxy.config.debug = 0
                wsdl_client.soapproxy.config.dict_encoding = 'UTF-8'
                resultado = wsdl_client.timbrar(*params)
                htz = int(self._get_time_zone())
                mensaje = _(tools.ustr(resultado['mensaje']))
                resultados_mensaje = resultado['resultados'] and resultado['resultados']['mensaje'] or ''
                ### obteniendo la cadena original del PAC ###
                cadena_original = resultado['resultados'] and resultado['resultados']['cadenaOriginal'] or self.cfdi_cadena_original
                folio_fiscal = resultado['resultados'] and resultado['resultados']['uuid'] or ''
                codigo_timbrado = resultado['status'] or ''
                codigo_validacion = resultado['resultados'] and resultado['resultados']['status'] or ''
                if codigo_timbrado == '311' or codigo_validacion == '311':
                    raise UserError(_('Advertencia !!!\nNo Autorizado.\nCode 311'))
                elif codigo_timbrado == '312' or codigo_validacion == '312':
                    raise UserError(_('Advertencia !!!\nError al consultar al SAT.\nCódigo 312'))
                elif codigo_timbrado == '200' and codigo_validacion == '200':
                    fecha_timbrado = resultado['resultados']['fechaTimbrado'] or False
                    cfdi_data = {
                        'cfdi_cbb': resultado['resultados']['qrCode'] or False,  # ya lo regresa en base64
                        'cfdi_sello': resultado['resultados']['selloSAT'] or False,
                        'cfdi_no_certificado': resultado['resultados']['certificadoSAT'] or False,
                        'cfdi_fecha_timbrado': fecha_timbrado,
                        'cfdi_xml': base64.decodebytes(resultado['resultados']['cfdiTimbrado'] or ''),  # este se necesita en uno que no es base64
                        'cfdi_folio_fiscal': resultado['resultados']['uuid'] or '',
                        #'pac_id': pac_params.id,
                        'cfdi_cadena_original': cadena_original,
                    }
                    msg += mensaje + "." + resultados_mensaje + " Folio Fiscal: " + folio_fiscal + "."
                    msg += _(u"\nPor favor asegúrese que la estructura del XML de la factura ha sido generada correctamente en el SAT\nhttps://www.consulta.sat.gob.mx/sicofi_web/moduloECFD_plus/ValidadorCFDI/Validador%20cfdi.html")
                    if cfdi_data.get('cfdi_xml', False):
                        url_pac = '</"%s"><!--Para validar el XML CFDI puede descargar el certificado del PAC desde la siguiente liga: https://solucionfactible.com/cfdi/00001000000102699425.zip-->' % (comprobante)
                        cfdi_data['cfdi_xml'] = cfdi_data['cfdi_xml'].replace('</"%s">' % (comprobante), url_pac)
                        file = base64.encodebytes(cfdi_data['cfdi_xml'] or '')
                        # self.cfdi_data_write(cr, uid, [payment.id], cfdi_data, context=context)
                        cfdi_xml = cfdi_data.pop('cfdi_xml')
                    if cfdi_xml:
                        self.write(cfdi_data)
                        cfdi_data['cfdi_xml'] = cfdi_xml
                    else:
                        msg += _("No puedo extraer el archivo XML del PAC")
                else:
                    msg += _('Advertencia !!!\nCódigo Sellado: %s. - Código Validación: %s. - Folio Fiscal: %s. - Mensaje: %s. - Mensaje de Validación: %s.') % (
                        codigo_timbrado, codigo_validacion, folio_fiscal, mensaje, resultados_mensaje)
        else:
            msg += 'No se encontró información del Webservice del PAC, revise la configuración'
            raise UserError(_('Advertencia !!!\nNo se encontró información del Webservice del PAC, revise la configuración'))
        #raise osv.except_osv('Pausa','Pausa')
        return {'file': file, 'msg': msg, 'cfdi_xml': cfdi_xml}
    

    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:    

    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:    