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
        

    
    
    def validate_scheme_facturae_xml(self, datas_xmls=[], facturae_version = None, facturae_type="cfdv", scheme_type='xsd'):
        # if not datas_xmls:
        #     datas_xmls = []
        # certificate_lib = self.env['facturae.certificate.library']
        # for data_xml in datas_xmls:
        #     (fileno_data_xml, fname_data_xml) = tempfile.mkstemp('.xml', 'odoo_' + (False or '') + '__facturae__' )
        #     f = open(fname_data_xml, 'wb')
        #     if not isinstance(data_xml, str):
        #         data_xml = data_xml.decode('utf-8')                
        #     data_xml = data_xml.replace("&amp;", "Y")#Replace temp for process with xmlstartlet
        #     f.write(str.encode(data_xml) )
        #     f.close()
        #     os.close(fileno_data_xml)
        #     all_paths = tools.config["addons_path"].split(",")
        #     for my_path in all_paths:
        #         if os.path.isdir(os.path.join(my_path, 'l10n_mx_einvoice', 'SAT')):
        #             # If dir is in path, save it on real_path
        #             fname_scheme = my_path and os.path.join(my_path, 'l10n_mx_einvoice', 'SAT', facturae_type + facturae_version +  '.' + scheme_type) or ''
        #             #fname_scheme = os.path.join(tools.config["addons_path"], u'l10n_mx_facturae', u'SAT', facturae_type + facturae_version +  '.' + scheme_type )
        #             fname_out = certificate_lib.b64str_to_tempfile(base64.encodebytes(str.encode('')), file_suffix='.txt', file_prefix='odoo__schema_validation_result__' )
        #             result = certificate_lib.check_xml_scheme(fname_data_xml, fname_scheme, fname_out)
        #             if result: #Valida el xml mediante el archivo xsd
        #                 raise UserError(_("Error al validar la estructura del xml !!!\n Validación de XML versión %s:\n%s" % (facturae_version, result)))
        return True                     
    
    
    
    def _get_facturae_invoice_xml_data(self):
        self.ensure_one()
        context = self._context.copy()
        invoice = self
        comprobante = 'cfdi:Comprobante'
        emisor = 'cfdi:Emisor'
        receptor = 'cfdi:Receptor'
        concepto = 'cfdi:Conceptos'
        facturae_version = '3.3'
        data_dict = self._get_facturae_invoice_dict_data()
        # data_dict = data_dict[0]
        while(type(data_dict)!=dict):
            try:
                data_dict = data_dict[0]
            except:
                data_dict = data_dict
        doc_xml = self.dict2xml({comprobante: data_dict.get(comprobante)})
        # ******
        invoice_number = "sn"
        (fileno_xml, fname_xml) = tempfile.mkstemp('.xml', 'odoo_' + (invoice_number or '') + '__facturae__')
        fname_txt = fname_xml + '.txt'
        f = open(fname_xml, 'w')
        doc_xml.writexml(
            f, indent='    ', addindent='    ', newl='\r\n', encoding='UTF-8')
        f.close()
        os.close(fileno_xml)
        (fileno_sign, fname_sign) = tempfile.mkstemp('.txt', 'odoo_' + (
            invoice_number or '') + '__facturae_txt_md5__')
        os.close(fileno_sign)

        context.update({
            'fname_xml': fname_xml,
            'fname_txt': fname_txt,
            'fname_sign': fname_sign,
        })
        
        nodeComprobante = doc_xml.getElementsByTagName(comprobante)[0]
        NoCertificado = self.journal_id.serial_number
        data_dict[comprobante]['NoCertificado'] = NoCertificado
        nodeComprobante.setAttribute("NoCertificado", NoCertificado)

        context.update(self._get_file_globals())
        cert_str = self._get_certificate_str(context['fname_cer'])
        if not cert_str:
            raise UserError(_("Error en Certificado !!!\nNo puedo obtener el Certificado del Comprobante. Revise su configuración.\n%s" % (msg2)))
        cert_str = cert_str.replace(' ', '').replace('\n', '')
        nodeComprobante.setAttribute("Certificado", cert_str)
        data_dict[comprobante]['Certificado'] = cert_str
        
        context.update({'xml_prev':doc_xml.toxml('UTF-8')})
        txt_str = self.with_context(context)._xml2cad_orig()
        data_dict['cadena_original'] = txt_str
        msg2=''

        if not txt_str:
            raise UserError(_("Error en la Cadena Original !!!\nNo puedo obtener la Cadena Original del Comprobante. Revise su configuración.\n%s" % (msg2)))
        context['cadena_original'] = txt_str
        
        if not data_dict[comprobante].get('Folio', ''):
            raise UserError(_("Error en Folio !!!\nNo puedo obtener el Folio del Comprobante. Antes de generar poder generar el XML debe tener la factura Abierta.\n%s" % (msg2)))
        

        context.update({'fecha': data_dict[comprobante]['Fecha']})
        
        
        
        ### SELLO ###                
        sign_str = self.with_context(context)._get_sello()
        ### Guardando la Cadena Original ####
        self.write({'cfdi_cadena_original':txt_str})

        if not sign_str:
            raise UserError(_("Error en Sello !!!\nNo puedo generar el Sello del Comprobante. Revise su configuración.\n%s" % (msg2)))

        nodeComprobante.setAttribute("Sello", sign_str)
        data_dict[comprobante]['Sello'] = sign_str

        #nodeComprobante.removeAttribute('anoAprobacion')
        #nodeComprobante.removeAttribute('noAprobacion')
        x = doc_xml.documentElement
        nodeReceptor = doc_xml.getElementsByTagName(receptor)[0]
        nodeConcepto = doc_xml.getElementsByTagName(concepto)[0]
        x.insertBefore(nodeReceptor, nodeConcepto)

        self.write_cfd_data(data_dict)

        if context.get('type_data') == 'dict':
            return data_dict
        if context.get('type_data') == 'xml_obj':
            return doc_xml
        data_xml = doc_xml.toxml('UTF-8').decode("utf-8")
        cdcs = codecs.BOM_UTF8
        cdcs = cdcs.decode("utf-8")
        data_xml = cdcs + data_xml
        fname_xml = (data_dict[comprobante][emisor]['Rfc'] or '') + '_' + \
            (data_dict[comprobante].get('Serie', '') or '') + '_' + \
            (str(data_dict[comprobante].get('Folio', '')) or '') + '.xml'
        fname_xml = fname_xml.replace('/','_')
        data_xml = data_xml.replace(
            '<?xml version="1.0" encoding="UTF-8"?>', '<?xml version="1.0" encoding="UTF-8"?>\n')

        #if self.company_id.validate_schema:
        #    self.validate_scheme_facturae_xml([data_xml], facturae_version)

        #data_dict.get('Comprobante',{})
        return fname_xml, data_xml
    
    
    def get_driver_cfdi_sign(self):
        """function to inherit from module driver of pac and add particular function"""
        return {}

    
    def get_driver_cfdi_cancel(self):
        """function to inherit from module driver of pac and add particular function"""
        return {}
                                        
                                        
    ####################################
    
    def do_something_with_xml_attachment(self, attach):
        return True
    

    @api.model
    def get_cfdi_cadena(self, xslt_path, cfdi_as_tree):
        xslt_root = etree.parse(tools.file_open(xslt_path))
        return str(etree.XSLT(xslt_root)(cfdi_as_tree))

    @api.model
    def _get_einvoice_cadena_tfd(self, cfdi_signed):
        self.ensure_one()
        #get the xslt path
        file_globals = self._get_file_globals()
        if 'fname_xslt_tfd' in file_globals:
            xslt_path = file_globals['fname_xslt_tfd']
        else:
            raise UserError("Errr!\nNo existe en archivo XSLT TFD en la carpeta SAT.")
        #get the cfdi as eTree
        # cfdi = base64.decodebytes(str.encode(cfdi_signed))
        # print("##############  cfdi >>>>>>",cfdi)
        cfdi = str.encode(cfdi_signed)
        cfdi = fromstring(cfdi)
        cfdi = self.account_invoice_tfd_node(cfdi)
        #return the cadena
        return self.get_cfdi_cadena(xslt_path, cfdi)

    @api.model
    def account_invoice_tfd_node(self, cfdi):
        attribute = 'tfd:TimbreFiscalDigital[1]'
        namespace = {'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital'}
        node = cfdi.Complemento.xpath(attribute, namespaces=namespace)
        return node[0] if node else None

    def action_cfdi_try_new(self):
        mail_compose_message_pool = self.env['mail.compose.message']
        attachment_obj = self.env['ir.attachment']
        for invoice in self.filtered(lambda w: w.journal_id.use_for_cfdi and \
                                     w.move_type in ('out_invoice','out_refund')):
            if invoice.cfdi_folio_fiscal:
                raise UserError(_('No puede validar la Factura o Nota de Crédito porque ya se encuentra timbrada. Genere un nuevo registro.'))

            fname_invoice = invoice.fname_invoice
            _logger.info('Iniciando proceso para Timbrar factura: %s', fname_invoice)
            # Obtenemos el contenido del archivo XML a timbrar
            cfdi_state = invoice.cfdi_state
            if cfdi_state =='draft':
                _logger.info('Generando archivo XML a enviar a PAC. - Factura: %s', fname_invoice)
                fname, xml_data = invoice._get_facturae_invoice_xml_data()
                _logger.info('Archivo XML creado. - Factura: %s', fname_invoice)
                root = etree.fromstring(xml_data)
                _xml_data = etree.tostring(root, pretty_print=True).decode()
                _logger.info("xml_data: %s" % _xml_data)
                
                invoice.write({'cfdi_state' : 'xml_unsigned',
                               'xml_file_no_sign_index': _xml_data,
                               'cfdi_state'            : 'xml_unsigned',
                               'cfdi_last_message'     : fields.Datetime.to_string(fields.Datetime.context_timestamp(
                                   invoice.with_context(tz=(self.env.user.partner_id.tz or 'Mexico/General')),
                                   datetime.datetime.now())) + \
                                                        '=> Archivo XML generado exitosamente'
                    })
                invoice.message_post(body=_('Archivo XML a timbrar generado exitosamente'))
                cfdi_state = 'xml_unsigned'

            # Mandamos a Timbrar
            
            #invoice = self
            type = invoice.cfdi_pac
            if cfdi_state =='xml_unsigned' and not invoice.xml_file_signed_index:
                try:
                    index_xml = ''
                    msj = ''        
                    # Instanciamos la clase para la integración con el PAC
                    type__fc = invoice.get_driver_cfdi_sign()
                    _logger.info(str(type__fc))
                    type__fc = type__fc or False
                    if type in type__fc.keys():
                        fname_invoice = invoice.fname_invoice and invoice.fname_invoice + \
                            '.xml' or ''
                        if not 'fname' in locals() or not 'xml_data' in locals():
                            _logger.info('Re-intentando generar XML para timbrar - Factura: %s', fname_invoice)
                            fname, xml_data = invoice._get_facturae_invoice_xml_data()
                        else:
                            _logger.info('Listo archivo XML a timbrar en el PAC - Factura: %s', fname_invoice)
                        fdata = base64.encodebytes(str.encode(xml_data))
                        _logger.info('Solicitando a PAC el Timbre para Factura: %s', fname_invoice)
                        res = type__fc[type](fdata) #
                        _logger.info("res: %s" % res)
                        _logger.info('Timbre entregado por el PAC - Factura: %s', fname_invoice)
                        msj = tools.ustr(res.get('msg', False))
                        index_xml = res.get('cfdi_xml', False)
                        
                        root = etree.fromstring(str.encode(index_xml))
                        _index_xml = etree.tostring(root, pretty_print=True).decode()
                        _logger.info("index_xml: %s" % _index_xml)
                        
                        invoice.write({'xml_file_signed_index' : _index_xml})

                        ###### Recalculando la Cadena Original ############
                        cfdi_signed = fdata
                        cadena_tfd_signed = ""
                        try:
                            cadena_tfd_signed = invoice._get_einvoice_cadena_tfd(index_xml)
                        except:
                            cadena_tfd_signed = invoice.cfdi_cadena_original
                        invoice.cfdi_cadena_original = cadena_tfd_signed
                        ################ FIN ################

                        data_attach = {
                                'name'        : fname_invoice,
                                'datas'       : base64.encodebytes(str.encode(index_xml)),
                                'store_fname' : fname_invoice,
                                'description' : 'Archivo XML del Comprobante Fiscal Digital - Factura: %s' % (invoice.name),
                                'res_model'   : 'account.move',
                                'res_id'      : invoice.id,
                                'type'        : 'binary',
                            }
                        attach = attachment_obj.with_context({}).create(data_attach)
                        xres = invoice.do_something_with_xml_attachment(attach)
                        cfdi_state = 'xml_signed'
                    else:
                        msj += _("No se encontró el Driver del PAC para %s" % (type))
                        self.env.cr.commit()
                        return bool(invoice.state=='open')
                    
                    invoice.write({'cfdi_state' : 'xml_signed',
                                'cfdi_last_message': invoice.cfdi_last_message + "\n-.-.-.-.-.-.-.-.-.-.-.-.-.\n" + \
                                fields.Datetime.to_string(fields.Datetime.context_timestamp(
                                                                                invoice.with_context(tz=(self.env.user.partner_id.tz or 'Mexico/General')),
                                                                                datetime.datetime.now())
                                                                               ) + \
                                                                ' => ' + msj})
                    invoice.message_post(body=msj)
                    self.env.cr.commit()
                except Exception:
                    error = tools.ustr(traceback.format_exc())
                    invoice.write({'cfdi_last_message': invoice.cfdi_last_message + "\n-.-.-.-.-.-.-.-.-.-.-.-.-.\n" + \
                                fields.Datetime.to_string(fields.Datetime.context_timestamp(
                                                                                invoice.with_context(tz=(self.env.user.partner_id.tz or 'Mexico/General')),
                                                                                datetime.datetime.now())
                                                                               ) + \
                                                                ' => ' + error})
                    invoice.message_post(body=msj)
                    _logger.error(error)
                    self.env.cr.commit()
                    return bool(invoice.state=='open')
            # Generamos formato de Impresión
            if cfdi_state == 'xml_signed' or invoice.xml_file_signed_index:
                _logger.info('Generando PDF - Factura: %s', fname_invoice)
                cfdi_state = 'pdf'
                invoice.cfdi_state = 'pdf'
                
            
            if cfdi_state == 'pdf' and invoice.partner_id.commercial_partner_id.envio_manual_cfdi:
                msj = _('No se enviaron los archivos por correo porque el Partner está marcado para no enviar automáticamente los archivos del CFDI (XML y PDF)')
                cfdi_state = 'sent'
                #invoice.write({'cfdi_last_message': invoice.cfdi_last_message + "\n-.-.-.-.-.-.-.-.-.-.-.-.-.\n" + \
                #                                fields.Datetime.to_string(fields.Datetime.context_timestamp(
                #                                invoice.with_context(tz=(self.env.user.partner_id.tz or 'Mexico/General')),
                #                                datetime.datetime.now())
                #                               ) + \
                #                                ' => ' + msj,
                #                'cfdi_state': 'sent',
                #                })
                invoice.message_post(body=msj)
            # Enviamos al cliente los archivos de la factura
            elif cfdi_state == 'pdf' and not invoice.partner_id.commercial_partner_id.envio_manual_cfdi:
                _logger.info('Intentando enviar XML y PDF por mail al cliente - Factura: %s', fname_invoice)
                msj = ''
                state = ''
                partner_mail = invoice.partner_id.email or False
                user_mail = self.env.user.email or False

                company_id = invoice.company_id.id
                #invoice = self
                address_id = invoice.partner_id.address_get(['invoice'])['invoice']
                partner_invoice_address = address_id
                fname_invoice = invoice.fname_invoice or ''
                adjuntos = attachment_obj.search([('res_model', '=', 'account.move'), 
                                                  ('res_id', '=', invoice.id)])
                q = True
                attachments = []
                for attach in adjuntos:
                    if q and attach.name.endswith('.xml'):
                        attachments.append(attach.id)
                        break

                
                template_id = self.env['mail.template'].search([('model_id.model', '=', 'account.move'),
                                                                #('company_id','=', company_id),
                                                                ('name','not ilike', '%Portal%'),
                                                                # ('report_template.report_name', '=',report_name)
                                                               ], limit=1)                            

                if template_id:
                    mail_server_obj = self.env['ir.mail_server']
                    mail_servers = mail_server_obj.search([])
                    if mail_servers:
                        ctx = dict(
                            default_model='account.move',
                            default_res_id=invoice.id,
                            default_use_template=bool(template_id),
                            default_template_id=template_id.id,
                            default_composition_mode='comment',
                            mark_invoice_as_sent=True,
                        )
                        ## CHERMAN 
                        # if template_id.report_template:
                        #     if 'l10n_mx_edi_is_required' in template_id.report_template.attachment:
                        #         template_id.report_template.attachment = "((object.company_emitter_id.partner_id.vat or object.company_id.partner_id.vat) + '_' + (object.name or '').replace('/','_').replace(' ','_')  +'.pdf')"
                        context2 = dict(self._context)
                        if 'default_journal_id' in context2:
                            del context2['default_journal_id']
                        if 'default_type' in context2:
                            del context2['default_type']
                        if 'search_default_dashboard' in context2:
                            del context2['search_default_dashboard']                        

                        try:
                            xres = mail_compose_message_pool.with_context(context2)._onchange_template_id(template_id=template_id.id, composition_mode=None,
                                                                                 model='account.move', res_id=invoice.id)
                            try:
                                attachments.append(xres['value']['attachment_ids'][0][2][0])
                            except:
                                mail_attachments = (xres['value']['attachment_ids'])
                                for mail_atch in mail_attachments:
                                    if mail_atch[0] == 4:
                                        # attachments.append(mail_atch[1])
                                        attach_br = self.env['ir.attachment'].browse(mail_atch[1])
                                        if attach_br.name != fname_invoice+'.pdf':
                                            attach_br.write({'name': fname_invoice+'.pdf'})
                                        attachments.append(mail_atch[1])
                        except:
                            _logger.error('No se genero el PDF de la Factura, no se enviara al cliente. - Factura: %s', fname_invoice)
                        try:
                            xres['value'].update({'attachment_ids' : [(6, 0, attachments)]})
                            message = mail_compose_message_pool.with_context(ctx).create(xres['value'])
                            _logger.info('Antes de  enviar XML y PDF por mail al cliente - Factura: %s', fname_invoice)
                            xx = message.action_send_mail()
                            _logger.info('Despues de  enviar XML y PDF por mail al cliente - Factura: %s', fname_invoice)
                            invoice.write({'cfdi_state': 'sent'})
                            msj = _("La factura fue enviada exitosamente por correo electrónico...")
                            cfdi_state == 'sent'
                        except:
                            msj = _("Advertencia !!!\nRevise que su plantilla de correo este correcta ya que no pudo generarse el correo automático para el cliente...")
                    else:
                        msj = _("Advertencia!!!\nNo se pudo enviar el correo electrónico debido a que no se tienen servidores de correo configurados.")
                else:
                    msj = _('Advertencia !!!\nRevise que su plantilla de correo esté asignada al Servidor de correo.\nTambién revise que tenga asignado el reporte a usar.\nLa plantilla está asociada a la misma Compañía')

                
                invoice.write({'cfdi_last_message': invoice.cfdi_last_message + "\n-.-.-.-.-.-.-.-.-.-.-.-.-.\n" + \
                                                fields.Datetime.to_string(fields.Datetime.context_timestamp(
                                                invoice.with_context(tz=(self.env.user.partner_id.tz or 'Mexico/General')),
                                                datetime.datetime.now())
                                               ) + \
                                                ' => ' + msj,
                                })
                invoice.message_post(body=msj)
            _logger.info('Fin proceso Timbrado - Factura: %s', fname_invoice)
            
            
            # Se encontraron que los archivos PDF se duplican
            adjuntos2 = attachment_obj.search([('res_model', '=', 'account.move'), ('res_id', '=', invoice.id)])
            x = 0
            for attach in adjuntos2:
                if attach.name.endswith('.pdf'):
                    x and attach.unlink()
                    if x: 
                        break
                    x += 1
            self.env.cr.commit()
        return True
        # return {
        #             'type': 'ir.actions.client',
        #             'tag': 'reload',
        #         }
        
    
    def action_post(self):
        result = super(AccountMove, self).action_post()
        mail_compose_message_pool = self.env['mail.compose.message']
        attachment_obj = self.env['ir.attachment']
        for invoice in self.filtered(lambda w: w.journal_id.use_for_cfdi and \
                                     w.move_type in ('out_invoice','out_refund')):
            if invoice.cfdi_folio_fiscal:
                raise UserError(_('No puede validar la Factura o Nota de Crédito porque ya se encuentra timbrada. Genere un nuevo registro.'))

            serial_validate_ok = invoice.company_id.validate_app_serial()
            if not serial_validate_ok:
                raise UserError("La Licencia para la generación del Complemento de Carta Porte es invalida.")

            fname_invoice = invoice.fname_invoice
            _logger.info('Iniciando proceso para Timbrar factura: %s', fname_invoice)
            # Obtenemos el contenido del archivo XML a timbrar
            cfdi_state = invoice.cfdi_state
            if cfdi_state =='draft':
                _logger.info('Generando archivo XML a enviar a PAC. - Factura: %s', fname_invoice)
                fname, xml_data = invoice._get_facturae_invoice_xml_data()
                _logger.info('Archivo XML creado. - Factura: %s', fname_invoice)
                root = etree.fromstring(xml_data)
                _xml_data = etree.tostring(root, pretty_print=True).decode()
                _logger.info("xml_data: %s" % _xml_data)
                
                invoice.write({'cfdi_state' : 'xml_unsigned',
                               'xml_file_no_sign_index': _xml_data,
                               'cfdi_state'            : 'xml_unsigned',
                               'cfdi_last_message'     : fields.Datetime.to_string(fields.Datetime.context_timestamp(
                                   invoice.with_context(tz=(self.env.user.partner_id.tz or 'Mexico/General')),
                                   datetime.datetime.now())) + \
                                                        '=> Archivo XML generado exitosamente'
                    })
                invoice.message_post(body=_('Archivo XML a timbrar generado exitosamente'))
                cfdi_state = 'xml_unsigned'

            # Mandamos a Timbrar
            
            #invoice = self
            type = invoice.cfdi_pac
            if cfdi_state =='xml_unsigned' and not invoice.xml_file_signed_index:
                try:
                    index_xml = ''
                    msj = ''        
                    # Instanciamos la clase para la integración con el PAC
                    type__fc = invoice.get_driver_cfdi_sign()
                    _logger.info(str(type__fc))
                    type__fc = type__fc or False
                    if type in type__fc.keys():
                        fname_invoice = invoice.fname_invoice and invoice.fname_invoice + \
                            '.xml' or ''
                        if not 'fname' in locals() or not 'xml_data' in locals():
                            _logger.info('Re-intentando generar XML para timbrar - Factura: %s', fname_invoice)
                            fname, xml_data = invoice._get_facturae_invoice_xml_data()
                        else:
                            _logger.info('Listo archivo XML a timbrar en el PAC - Factura: %s', fname_invoice)
                        fdata = base64.encodebytes(str.encode(xml_data))
                        _logger.info('Solicitando a PAC el Timbre para Factura: %s', fname_invoice)
                        res = type__fc[type](fdata) #
                        _logger.info("res: %s" % res)
                        _logger.info('Timbre entregado por el PAC - Factura: %s', fname_invoice)
                        msj = tools.ustr(res.get('msg', False))
                        index_xml = res.get('cfdi_xml', False)
                        
                        root = etree.fromstring(str.encode(index_xml))
                        _index_xml = etree.tostring(root, pretty_print=True).decode()
                        _logger.info("index_xml: %s" % _index_xml)
                        
                        invoice.write({'xml_file_signed_index' : _index_xml})

                        ###### Recalculando la Cadena Original ############
                        cfdi_signed = fdata
                        cadena_tfd_signed = ""
                        try:
                            cadena_tfd_signed = invoice._get_einvoice_cadena_tfd(index_xml)
                        except:
                            cadena_tfd_signed = invoice.cfdi_cadena_original
                        invoice.cfdi_cadena_original = cadena_tfd_signed
                        ################ FIN ################

                        data_attach = {
                                'name'        : fname_invoice,
                                'datas'       : base64.encodebytes(str.encode(index_xml)),
                                'store_fname' : fname_invoice,
                                'description' : 'Archivo XML del Comprobante Fiscal Digital - Factura: %s' % (invoice.name),
                                'res_model'   : 'account.move',
                                'res_id'      : invoice.id,
                                'type'        : 'binary',
                            }
                        attach = attachment_obj.with_context({}).create(data_attach)
                        xres = invoice.do_something_with_xml_attachment(attach)
                        cfdi_state = 'xml_signed'
                    else:
                        msj += _("No se encontró el Driver del PAC para %s" % (type))
                        self.env.cr.commit()
                        return bool(invoice.state=='open')
                    
                    invoice.write({'cfdi_state' : 'xml_signed',
                                'cfdi_last_message': invoice.cfdi_last_message + "\n-.-.-.-.-.-.-.-.-.-.-.-.-.\n" + \
                                fields.Datetime.to_string(fields.Datetime.context_timestamp(
                                                                                invoice.with_context(tz=(self.env.user.partner_id.tz or 'Mexico/General')),
                                                                                datetime.datetime.now())
                                                                               ) + \
                                                                ' => ' + msj})
                    invoice.message_post(body=msj)
                    self.env.cr.commit()
                except Exception:
                    error = tools.ustr(traceback.format_exc())
                    invoice.write({'cfdi_last_message': invoice.cfdi_last_message + "\n-.-.-.-.-.-.-.-.-.-.-.-.-.\n" + \
                                fields.Datetime.to_string(fields.Datetime.context_timestamp(
                                                                                invoice.with_context(tz=(self.env.user.partner_id.tz or 'Mexico/General')),
                                                                                datetime.datetime.now())
                                                                               ) + \
                                                                ' => ' + error})
                    invoice.message_post(body=msj)
                    _logger.error(error)
                    self.env.cr.commit()
                    return bool(invoice.state=='open')
            # Generamos formato de Impresión
            if cfdi_state == 'xml_signed' or invoice.xml_file_signed_index:
                _logger.info('Generando PDF - Factura: %s', fname_invoice)
                cfdi_state = 'pdf'
                
            
            if cfdi_state == 'pdf' and invoice.partner_id.commercial_partner_id.envio_manual_cfdi:
                msj = _('No se enviaron los archivos por correo porque el Partner está marcado para no enviar automáticamente los archivos del CFDI (XML y PDF)')
                #cfdi_state = 'sent'
                #invoice.write({'cfdi_last_message': invoice.cfdi_last_message + "\n-.-.-.-.-.-.-.-.-.-.-.-.-.\n" + \
                #                                fields.Datetime.to_string(fields.Datetime.context_timestamp(
                #                                invoice.with_context(tz=(self.env.user.partner_id.tz or 'Mexico/General')),
                #                                datetime.datetime.now())
                #                               ) + \
                #                                ' => ' + msj,
                #                'cfdi_state': 'sent',
                #                })
                invoice.message_post(body=msj)
            # Enviamos al cliente los archivos de la factura
            elif cfdi_state == 'pdf' and not invoice.partner_id.commercial_partner_id.envio_manual_cfdi:
                _logger.info('Intentando enviar XML y PDF por mail al cliente - Factura: %s', fname_invoice)
                msj = ''
                state = ''
                partner_mail = invoice.partner_id.email or False
                user_mail = self.env.user.email or False

                company_id = invoice.company_id.id
                #invoice = self
                address_id = invoice.partner_id.address_get(['invoice'])['invoice']
                partner_invoice_address = address_id
                fname_invoice = invoice.fname_invoice or ''
                adjuntos = attachment_obj.search([('res_model', '=', 'account.move'), 
                                                  ('res_id', '=', invoice.id)])
                q = True
                attachments = []
                for attach in adjuntos:
                    if q and attach.name.endswith('.xml'):
                        attachments.append(attach.id)
                        break

                
                template_id = self.env['mail.template'].search([('model_id.model', '=', 'account.move'),
                                                                #('company_id','=', company_id),
                                                                ('name','not ilike', '%Portal%'),
                                                                # ('report_template.report_name', '=',report_name)
                                                               ], limit=1)                            

                if template_id:
                    mail_server_obj = self.env['ir.mail_server']
                    mail_servers = mail_server_obj.search([])
                    if mail_servers:
                        ctx = dict(
                            default_model='account.move',
                            default_res_id=invoice.id,
                            default_use_template=bool(template_id),
                            default_template_id=template_id.id,
                            default_composition_mode='comment',
                            mark_invoice_as_sent=True,
                        )
                        ## CHERMAN 
                        # if template_id.report_template:
                        #     if 'l10n_mx_edi_is_required' in template_id.report_template.attachment:
                        #         template_id.report_template.attachment = "((object.company_emitter_id.partner_id.vat or object.company_id.partner_id.vat) + '_' + (object.name or '').replace('/','_').replace(' ','_')  +'.pdf')"
                        context2 = dict(self._context)
                        if 'default_journal_id' in context2:
                            del context2['default_journal_id']
                        if 'default_type' in context2:
                            del context2['default_type']
                        if 'search_default_dashboard' in context2:
                            del context2['search_default_dashboard']                        

                        try:
                            xres = mail_compose_message_pool.with_context(context2)._onchange_template_id(template_id=template_id.id, composition_mode=None,
                                                                                 model='account.move', res_id=invoice.id)
                            try:
                                attachments.append(xres['value']['attachment_ids'][0][2][0])
                            except:
                                mail_attachments = (xres['value']['attachment_ids'])
                                for mail_atch in mail_attachments:
                                    if mail_atch[0] == 4:
                                        # attachments.append(mail_atch[1])
                                        attach_br = self.env['ir.attachment'].browse(mail_atch[1])
                                        if attach_br.name != fname_invoice+'.pdf':
                                            attach_br.write({'name': fname_invoice+'.pdf'})
                                        attachments.append(mail_atch[1])
                        except:
                            _logger.error('No se genero el PDF de la Factura, no se enviara al cliente. - Factura: %s', fname_invoice)
                        try:
                            xres['value'].update({'attachment_ids' : [(6, 0, attachments)]})
                            message = mail_compose_message_pool.with_context(ctx).create(xres['value'])
                            _logger.info('Antes de  enviar XML y PDF por mail al cliente - Factura: %s', fname_invoice)
                            xx = message.action_send_mail()
                            _logger.info('Despues de  enviar XML y PDF por mail al cliente - Factura: %s', fname_invoice)
                            invoice.write({'cfdi_state': 'sent'})
                            msj = _("La factura fue enviada exitosamente por correo electrónico...")
                            cfdi_state == 'sent'
                        except:
                            msj = _("Advertencia !!!\nRevise que su plantilla de correo este correcta ya que no pudo generarse el correo automático para el cliente...")
                    else:
                        msj = _("Advertencia!!!\nNo se pudo enviar el correo electrónico debido a que no se tienen servidores de correo configurados.")
                else:
                    msj = _('Advertencia !!!\nRevise que su plantilla de correo esté asignada al Servidor de correo.\nTambién revise que tenga asignado el reporte a usar.\nLa plantilla está asociada a la misma Compañía')

                
                invoice.write({'cfdi_last_message': invoice.cfdi_last_message + "\n-.-.-.-.-.-.-.-.-.-.-.-.-.\n" + \
                                                fields.Datetime.to_string(fields.Datetime.context_timestamp(
                                                invoice.with_context(tz=(self.env.user.partner_id.tz or 'Mexico/General')),
                                                datetime.datetime.now())
                                               ) + \
                                                ' => ' + msj,
                                })
                invoice.message_post(body=msj)
            _logger.info('Fin proceso Timbrado - Factura: %s', fname_invoice)
            
            
            # Se encontraron que los archivos PDF se duplican
            adjuntos2 = attachment_obj.search([('res_model', '=', 'account.move'), ('res_id', '=', invoice.id)])
            x = 0
            for attach in adjuntos2:
                if attach.name.endswith('.pdf'):
                    x and attach.unlink()
                    if x: 
                        break
                    x += 1
            self.env.cr.commit()
        return result
        

    ## Del modulo de Cancelacion de facturas
    def button_draft(self):
        context = self._context
        if 'default_payment_type' in context and context['default_payment_type']:
            res = super(AccountMove, self).button_draft()
            return res
        for invoice in self:
            if invoice.move_type in ('out_refund','out_invoice'):
                if invoice.cancel_wht_mailbox:
                    cancelation_message = "El CFDI %s no genero Cancelacion Fiscal en el SAT, debido a que se cancelo sin Solicitudes de Buzón Tributario." % invoice.cfdi_folio_fiscal
                    invoice.write({'cfdi_fecha_cancelacion':time.strftime('%Y-%m-%d %H:%M:%S'),
                                #'date_invoice_cancel': time.strftime('%Y-%m-%d %H:%M:%S'),
                                'cfdi_last_message': self.cfdi_last_message + "\n-.-.-.-.-.-.-.-.-.-.-.-.-.\n" + \
                                        fields.Datetime.to_string(fields.Datetime.context_timestamp(
                                                                                        self.with_context(tz=(self.env.user.partner_id.tz or 'America/Mexico_City')),
                                                                                        datetime.datetime.now())
                                                                                       ) + \
                                                                        ' => ' + cancelation_message, 
                                    })
                    res = super(AccountMove, self).button_draft()
                    if invoice.state == 'draft':
                        invoice.button_cancel()
                    return res
                if invoice.move_type in ('out_invoice', 'out_refund') and invoice.journal_id.use_for_cfdi and invoice.cfdi_folio_fiscal:
                    if invoice.cancelation_request_ids:
                        last_request = invoice.cancelation_request_ids[-1]
                        if last_request.state in ('rejected','no_cancel') and invoice.cancel_wht_mailbox == False:
                            raise UserError("El CFDI no puede ser Cancelado debido a un rechazo por el Cliente o el SAT.")
                    cancelation_id = False
                    if not invoice.cancelation_request_ids:
                        cancelation_id = invoice.cancelation_request_create()
                    if invoice.mailbox_state != 'done':
                        if invoice.cancel_wht_mailbox == True:
                            res = super(AccountMove, self).button_draft()
                            if invoice.state == 'draft':
                                invoice.button_cancel()
                            return res
                        if cancelation_id:
                            cancelation_message = "CFDI en proceso de Cancelacion. Mensaje del Proveedor: "+ str(cancelation_id.message_invisible)
                            invoice.write({'cfdi_fecha_cancelacion':time.strftime('%Y-%m-%d %H:%M:%S'),
                                #'date_invoice_cancel': time.strftime('%Y-%m-%d %H:%M:%S'),
                                'cfdi_last_message': self.cfdi_last_message + "\n-.-.-.-.-.-.-.-.-.-.-.-.-.\n" + \
                                        fields.Datetime.to_string(fields.Datetime.context_timestamp(
                                                                                        self.with_context(tz=(self.env.user.partner_id.tz or 'America/Mexico_City')),
                                                                                        datetime.datetime.now())
                                                                                       ) + \
                                                                        ' => ' + cancelation_message, 
                                    })
                            invoice.message_post(body=cancelation_message)
                        else:
                            cancelation_message = "CFDI en proceso de Cancelacion. Mensaje del Proveedor: "+ str(last_request.message_invisible if last_request.message_invisible else '' )
                            invoice.write({'cfdi_fecha_cancelacion':time.strftime('%Y-%m-%d %H:%M:%S'),
                                #'date_invoice_cancel': time.strftime('%Y-%m-%d %H:%M:%S'),
                                'cfdi_last_message': self.cfdi_last_message + "\n-.-.-.-.-.-.-.-.-.-.-.-.-.\n" + \
                                        fields.Datetime.to_string(fields.Datetime.context_timestamp(
                                                                                        self.with_context(tz=(self.env.user.partner_id.tz or 'America/Mexico_City')),
                                                                                        datetime.datetime.now())
                                                                                       ) + \
                                                                        ' => ' + cancelation_message, 
                                    })
                            invoice.message_post(body=cancelation_message)
                        return {}

                    cancelation_done = False
                    for request_cancel in invoice.cancelation_request_ids:
                        if request_cancel.state == 'done':
                            cancelation_done = request_cancel
                            break
                    if invoice.mailbox_state == 'done':
                        # res2 = type__fc[invoice.cfdi_pac]()[0]
                        if cancelation_done:
                            cancelation_message = cancelation_done.message_invisible
                            if cancelation_message:
                                cancelation_message = "CFDI cancelado correctamente. Mensaje del Proveedor: "+ cancelation_message
                            else:
                                cancelation_message = "CFDI cancelado correctamente. "+ cancelation_message
                            invoice.write({'cfdi_fecha_cancelacion':time.strftime('%Y-%m-%d %H:%M:%S'),
                                #'date_invoice_cancel': time.strftime('%Y-%m-%d %H:%M:%S'),
                                'cfdi_last_message': self.cfdi_last_message + "\n-.-.-.-.-.-.-.-.-.-.-.-.-.\n" + \
                                        fields.Datetime.to_string(fields.Datetime.context_timestamp(
                                                                                        self.with_context(tz=(self.env.user.partner_id.tz or 'America/Mexico_City')),
                                                                                        datetime.datetime.now())
                                                                                       ) + \
                                                                        ' => ' + cancelation_message, 
                                    })
                            invoice.message_post(body=cancelation_message)
                for cfdi_rel in invoice.type_rel_cfdi_ids:
                    cfdi_rel.invoice_id.write({'deposit_invoice_used': False, 'deposit_invoice_rel_id': False})
                if invoice.state == 'draft':
                    invoice.button_cancel()
        res = super(AccountMove, self).button_draft()
        if any(reg.mailbox_state == 'process' and not reg.cancel_wht_mailbox for reg in self):
            raise ValidationError("Error!\nNo se pudo generar la cancelacion del Comprobante.")
        return res
        
    def action_invoice_paid(self):
        for rec in self:
            if rec.mailbox_state == 'process' and rec.cancel_wht_mailbox == False:
                raise ValidationError("Error!\nNo se puede Pagar una Factura que tiene una Solicitud de Cancelacion.")
        res = super(AccountMove, self).action_invoice_paid()
        return res
    

    @api.constrains('cancelation_request_ids')
    def _constraint_cancelation_request_ids(self):
        for rec in self:
            if rec.cancelation_request_ids:
                if len(rec.cancelation_request_ids) > 3:
                    raise ValidationError(_('Error !\nSolo se pueden generar 3 Solicitudes de Cancelacion.'))
        return True


    def cancelation_request_create(self):
        for rec in self:
            if rec.move_type in ('out_invoice', 'out_refund') and rec.journal_id.use_for_cfdi and rec.cfdi_folio_fiscal:
                cancelation_obj = self.env['account.move.cancelation.record']
                date_request = fields.Datetime.now()
                cancelation_prev = False
                next_cancelation_enable = ""
                mensaje_cancelacion = "Se generó una solicitud de cancelación para buzón tributario SAT."
                rec.write({'cfdi_last_message': self.cfdi_last_message + "\n-.-.-.-.-.-.-.-.-.-.-.-.-.\n" + \
                                    fields.Datetime.to_string(fields.Datetime.context_timestamp(
                                                                                    self.with_context(tz=(self.env.user.partner_id.tz or 'America/Mexico_City')),
                                                                                    datetime.datetime.now())
                                                                                   ) + \
                                                                    ' => ' + mensaje_cancelacion
                                })

                if rec.cancelation_request_ids:
                    if len(rec.cancelation_request_ids) >= 3:
                        raise ValidationError(_('Error !\nSolo se pueden generar 3 Solicitudes de Cancelacion.'))

                    cancelation_prev = rec.cancelation_request_ids[-1]
                    cancelation_prev_date = cancelation_prev.date_request
                    next_cancelation_enable = str(cancelation_prev_date + timedelta(hours=24))
                    if str(date_request) < next_cancelation_enable:
                        raise UserError("Error!\nSolo se puede Generar una nueva Solicitud despues de 24 hrs de haber generado una previa.")
                for reqst in rec.cancelation_request_ids:
                    reqst.state = 'cancel'
                vals = {
                    'date_request': date_request,
                    'state': 'process',
                    'invoice_id': rec.id ,
                    'folio_fiscal': 'N/A',
                }
                cancelation_id = cancelation_obj.create(vals)
                ### Conectando con el PAC Instalado - SAT ####
                request_result = cancelation_id.solitud_cancelacion_asincrona()
                if cancelation_id.state == 'done':
                    ### Cancelamos ###
                    rec.with_context(success_done=True).button_draft()
                ### Debe retornar ###
                ### folio_fiscal ##
                ### state ###
                ### mensaje ###
                # if request_result:
                #     cancelation_id.write(request_result)
                return cancelation_id

    
    def cancelation_request_consult(self):
        for rec in self:
            if rec.move_type in ('out_invoice', 'out_refund') and rec.journal_id.use_for_cfdi and rec.cfdi_folio_fiscal:

                cancelation_obj = self.env['account.move.cancelation.record']
                date_request = fields.Datetime.now()
                cancelation_id = False
                if rec.cancelation_request_ids:
                    cancelation_id = rec.cancelation_request_ids[-1]
                else:
                    raise UserError("Error!\nNo existen solicitudes de Cancelacion.")
                ### Conectando con el PAC Instalado - SAT ####
                request_result = cancelation_id.solitud_cancelacion_consulta_status()
                cancelation_message = cancelation_id.message_invisible
                ## Ejecutando el Metodo Cancelar ##
                rec.button_draft()
                ### Debe retornar ###
                ### folio_fiscal ##
                ### state ###
                # if request_result:
                #     cancelation_id.write(request_result)

                return cancelation_id


class AccountMoveLine(models.Model):
    _name = 'account.move.line'
    _inherit ='account.move.line'

    
    ### Permite Añadir Complementos por Conceptos ###
    ############### CFDI 3.3 #################
    def add_complements_with_concept_cfdi(self, concepto):
        # invoice_line = linea de la Factura (Browse Record)
        # product = producto de la linea (Browse Record)
        return concepto

    
    
    
    def update_properties_concept(self, concepto):
        return concepto
