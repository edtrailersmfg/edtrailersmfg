# -*- coding: utf-8 -*-
from odoo import api, models, fields, tools, _
from odoo.tools.xml_utils import _check_with_xsd
from odoo.exceptions import UserError, RedirectWarning, ValidationError
import logging
import re
import base64
import json
import requests
import random
import string
import tempfile
from lxml import etree
from lxml.objectify import fromstring
from datetime import datetime
from io import BytesIO
#from zeep import Client
#from zeep.transports import Transport
from json.decoder import JSONDecodeError
from suds.client import Client, WebFault
from suds.plugin import MessagePlugin
import os
import io
import zipfile
import subprocess
import xmltodict

_logger = logging.getLogger(__name__)


codigo_cancelacion = {
    '201': 'La solicitud de cancelación se registró exitosamente.',
    '202': 'Comprobante cancelado previamente.',
    '211': 'Comprobante enviado a cancelar exitosamente.',
    '205': 'El comprobante aún no se encuentra reportado en el SAT.',
    '402': 'El UUID enviado no tiene un formato correcto.',
    '300': 'Token no es válido',
    '301': 'Token no registrado para esta empresa',
    '302': 'Token ha caducado',
}



class LogPlugin(MessagePlugin):
    def sending(self, context):
        _logger.info(str(context.envelope))
        #print(str(context.envelope))
        return
    def received(self, context):
        _logger.info(str(context.reply))
        #print(str(context.reply))
        return


class AccountEdiFormat(models.Model):
    _inherit = 'account.edi.format'

    
    def _get_pfx_file_and_password(self, move):
        certificates = move.company_id.l10n_mx_edi_certificate_ids
        certificate = certificates.sudo().get_valid_certificate()
        
        certificate_pfx = certificate.pfx.decode("utf-8")
        password =  certificate.password #password.decode("utf-8") 
        return certificate_pfx, password
    
    
    
    def _l10n_mx_edi_get_sifei_credentials(self, move):
        if move.company_id.l10n_mx_edi_pac_test_env:
            return {
                'username': move.company_id.l10n_mx_edi_pac_username,
                'password': move.company_id.l10n_mx_edi_pac_password,
                'equipo_id' : move.company_id.l10n_mx_edi_pac_equipo_id,
                'url'     : 'http://devcfdi.sifei.com.mx:8080/SIFEI33/SIFEI?wsdl',
                'cancel_url': 'http://devcfdi.sifei.com.mx:8888/CancelacionSIFEI/Cancelacion?wsdl',
            }
        else:
            if not move.company_id.l10n_mx_edi_pac_username or not move.company_id.l10n_mx_edi_pac_password or not move.company_id.l10n_mx_edi_pac_equipo_id:
                return {
                    'errors': [_("The username and/or password are missing.")]
                }

            return {
                'username': move.company_id.l10n_mx_edi_pac_username,
                'password': move.company_id.l10n_mx_edi_pac_password,
                'equipo_id' : move.company_id.l10n_mx_edi_pac_equipo_id,
                'url': 'https://sat.sifei.com.mx:8443/SIFEI/SIFEI?wsdl',
                'cancel_url': 'https://sat.sifei.com.mx:9000/CancelacionSIFEI/Cancelacion?wsdl',
            }

    def _l10n_mx_edi_sifei_sign(self, move, credentials, cfdi):
        #_logger.info("cfdi: %s" % cfdi)
        
        ##########################
        # -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-    
        ## Archivo a Timbrar ###
        (fileno, fname_xml) = tempfile.mkstemp(".xml", "odoo_xml_to_sifei__")
        f_argil = open(fname_xml, 'bw')
        f_argil.write(cfdi)
        f_argil.close()
        os.close(fileno)

        xres = os.system("zip -j " + fname_xml.split('.')[0] + ".zip " + fname_xml + " > /dev/null")

        zipped_xml_file = open(fname_xml.split('.')[0] + ".zip", 'rb')
        cfdi_zipped = base64.b64encode(zipped_xml_file.read())
        zipped_xml_file.close()

        client = Client(credentials['url'], plugins=[LogPlugin()])
        try:
            resultado = client.service.getCFDI(credentials['username'], credentials['password'], cfdi_zipped.decode("utf-8"), ' ', credentials['equipo_id'])
        except WebFault as f:
            return {
                'errors': [_("La llamada al Servicio de Timbrado de SIFEI falló con el siguiente error: <br/>- Código: %s\n<br/>- Error: %s\n<br/>- Mensaje: %s" % (f.fault.detail.SifeiException.codigo, f.fault.detail.SifeiException.error, f.fault.detail.SifeiException.message))],
            }

        fstamped = io.BytesIO(base64.b64decode(str.encode(resultado)))

        zipf = zipfile.ZipFile(fstamped, 'r')
        zipf1 = zipf.open(zipf.namelist()[0])
        cfdi_signed = zipf1.read() #.replace(b'\r',b'').replace(b'\n',b'')
        if cfdi_signed:
            return {
                'cfdi_signed': cfdi_signed,
                'cfdi_encoding': 'str',
            }
        
        code = '000'
        msg = 'Error desconocido'
        res = resultado.resultados
        errors = []
        if code:
            errors.append(_("Code : %s") % code)
        if msg:
            errors.append(_("Message : %s") % msg)
        return {'errors': errors}
        


    def _l10n_mx_edi_sifei_cancel(self, move, credentials, cfdi):
        certificate_pfx, cert_password = self._get_pfx_file_and_password(move)
        #_logger.info("certificate_pfx: %s" % certificate_pfx)
        #_logger.info("cert_password: %s" % cert_password)
        ##################################
        client = Client(credentials['cancel_url'], plugins=[LogPlugin()])
        try:
            resultado = client.service.cancelaCFDI(credentials['username'], 
                                                   credentials['password'], 
                                                   move.company_id.vat,
                                                   certificate_pfx, 
                                                   cert_password, 
                                                   move.l10n_mx_edi_cfdi_uuid)
            
            
            try:
                res = xmltodict.parse(resultado)
                msg = _('Se solicitó la Cancelación del CFDI con Folio: %s<br/>'
                        'Fecha: %s<br/>'
                        'Código de Cancelación: %s - %s<br/>'
                        'Sello SAT: %s'
                       )  % (res['Acuse']['Folios']['UUID'],
                             res['Acuse']['@Fecha'],
                             res['Acuse']['Folios']['EstatusUUID'],
                             res['Acuse']['Folios']['EstatusUUID'] in codigo_cancelacion and codigo_cancelacion[res['Acuse']['Folios']['EstatusUUID']] or 'Sin descripción',
                             res['Acuse']['Signature']['SignedInfo']['Reference']['DigestValue'],
                               )
                move.message_post(body=msg)
                payment = self.env['account.payment'].search([('move_id','=',move.id)])
                if payment:
                    payment.message_post(body=msg)
                    
            except:
                pass
            
        except WebFault as f:
            return {
                'errors': [_("La llamada al Servicio de Cancelación de SIFEI falló con el siguiente error: <br/>- Código: %s\n<br/>- Error: %s\n<br/>- Mensaje: %s" % (f.fault.detail.SifeiException.codigo, f.fault.detail.SifeiException.error, f.fault.detail.SifeiException.message))],
            }

        #_logger.info("resultado: %s" % resultado)
        return {'success': True}
        
        
        ##################################
        
        uuids = [move.l10n_mx_edi_cfdi_uuid]
        certificates = move.company_id.l10n_mx_edi_certificate_ids
        certificate = certificates.sudo().get_valid_certificate()
        cer_pem = certificate.get_pem_cer(certificate.content)
        key_pem = certificate.get_pem_key(certificate.key, certificate.password)
        key_password = certificate.password

        try:
            transport = Transport(timeout=20)
            client = Client(credentials['url'], transport=transport)
            response = client.service.cancelar(
                credentials['username'], credentials['password'], uuids, cer_pem, key_pem, key_password)
        except Exception as e:
            return {
                'errors': [_("The Solucion Factible service failed to cancel with the following error: %s", str(e))],
            }

        if (response.status not in (200, 201)):
            # ws-timbrado-cancelar - status 200 : El proceso de cancelación se ha completado correctamente.
            # ws-timbrado-cancelar - status 201 : El folio se ha cancelado con éxito.
            return {
                'errors': [_("The Solucion Factible service failed to cancel with the following error: %s", response.mensaje)],
            }

        
        res = response.resultados
        code = getattr(res[0], 'statusUUID', None) if res else getattr(response, 'status', None)
        cancelled = code in ('201', '202')  # cancelled or previously cancelled
        # no show code and response message if cancel was success
        msg = '' if cancelled else getattr(res[0] if res else response, 'mensaje', None)
        code = '' if cancelled else code

        errors = []
        if code:
            errors.append(_("Code : %s") % code)
        if msg:
            errors.append(_("Message : %s") % msg)
        if errors:
            return {'errors': errors}

        return {'success': True}

    def _l10n_mx_edi_sifei_sign_invoice(self, invoice, credentials, cfdi):
        return self._l10n_mx_edi_sifei_sign(invoice, credentials, cfdi)

    def _l10n_mx_edi_sifei_cancel_invoice(self, invoice, credentials, cfdi):
        return self._l10n_mx_edi_sifei_cancel(invoice, credentials, cfdi)

    def _l10n_mx_edi_sifei_sign_payment(self, move, credentials, cfdi):
        return self._l10n_mx_edi_sifei_sign(move, credentials, cfdi)

    def _l10n_mx_edi_sifei_cancel_payment(self, move, credentials, cfdi):
        return self._l10n_mx_edi_sifei_cancel(move, credentials, cfdi)