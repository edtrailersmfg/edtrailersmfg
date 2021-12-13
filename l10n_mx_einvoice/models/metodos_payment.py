# -*- encoding: utf-8 -*-
from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
import os
import re
import xml
import codecs
import operator
import pytz
import jinja2
import tempfile
import time as ti
import datetime
import traceback
import base64

from lxml import etree
from lxml.objectify import fromstring
from xml.dom.minidom import parse, parseString

CFDI_XSLT_CADENA_TFD = 'l10n_mx_einvoice/SAT/cadenaoriginal_3_3/cadenaoriginal_TFD_1_1.xslt'

import logging
_logger = logging.getLogger(__name__)


# class AccountMove(models.Model):
#     _name = 'account.move'
#     _inherit ='account.move'

#     def _post(self, soft=True):
#         print ("### _post >>>>>>>>>> ")
#         print ("### soft >>>>>>>>>> ", soft)
#         res = super(AccountMove, self)._post(soft=soft)
#         for rec in self:
#             print ("### REC >>>>>>>>> ",rec)
#             print ("### REC MOVE TYPE >>>>>>>>> ",rec.move_type)
#             if rec.move_type == 'entry':
#                 payment_inst = self.env['account.payment'].browse(rec.id)
#                 print ("####### payment_inst >>>>>>>>> ",payment_inst)
#                 print ("####### payment_inst.reconciled_invoice_ids >>>>>>>>> ",payment_inst.reconciled_invoice_ids)
#                 raise UserError("### AQUI >>>> ")
#         return res


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    def search_invoices_from_payment(self, payment):
        stored_payment = payment.id
        if not stored_payment:
            return[]       

        self._cr.execute('''
            SELECT
                payment.id,
                ARRAY_AGG(DISTINCT invoice.id) AS invoice_ids,
                invoice.move_type
            FROM account_payment payment
            JOIN account_move move ON move.id = payment.move_id
            JOIN account_move_line line ON line.move_id = move.id
            JOIN account_partial_reconcile part ON
                part.debit_move_id = line.id
                OR
                part.credit_move_id = line.id
            JOIN account_move_line counterpart_line ON
                part.debit_move_id = counterpart_line.id
                OR
                part.credit_move_id = counterpart_line.id
            JOIN account_move invoice ON invoice.id = counterpart_line.move_id
            JOIN account_account account ON account.id = line.account_id
            WHERE account.internal_type IN ('receivable', 'payable')
                AND payment.id = %(payment_id)s
                AND line.id != counterpart_line.id
                AND invoice.move_type in ('out_invoice', 'out_refund', 'in_invoice', 'in_refund', 'out_receipt', 'in_receipt')
            GROUP BY payment.id, invoice.move_type
        ''', {
            'payment_id': stored_payment,
        })
        query_res = self._cr.dictfetchall()
        result_invoice_ids = []
        for res in query_res:
            pay = self.browse(res['id'])
            if res['move_type'] in self.env['account.move'].get_sale_types(True):
                invoice_ids = res.get('invoice_ids', [])
                result_invoice_ids = result_invoice_ids + invoice_ids
        return result_invoice_ids

    ### Se migro la funcion ya que ahora los pagos son una extension de las Polizas, como las facturas ####
    # def action_post(self):
    #     res = super(AccountPayment, self).action_post()
    #     print ("### RES >>>>>>>>>> ",res)
    #     payment_line_obj = self.env['account.payment.invoice']
    #     invoice_obj = self.env['account.move']
    #     for payment in self:
    #         if payment.payment_type!='inbound' or not payment.journal_id.use_for_cfdi:
    #             continue
    #         payment.create_cfdi_data_from_payment()
    #         if payment.generar_cfdi and not payment.get_cfdi():
    #             raise UserError(_('Advertencia !!!\nOcurrió un error al intentar obtener el CFDI de Recepción de Pagos para el Pago: %s') % (payment.name))
    #         print ("######### payment.payment_invoice_line_ids >>>>>>> ",payment.payment_invoice_line_ids)
    #     return res

    ### Por los errores de la conciliacion de los movs. de pagos y facturas ahora se tuvo que usar esta funcion #####
    def _synchronize_from_moves(self, changed_fields):
        res = super(AccountPayment, self)._synchronize_from_moves(changed_fields)
        payment_line_obj = self.env['account.payment.invoice']
        invoice_obj = self.env['account.move']
        for payment in self:
            if payment.payment_type !='inbound' or not payment.journal_id.use_for_cfdi:
                continue
            if not payment.generar_cfdi:
                continue
            if not payment.payment_invoice_line_ids:
                payment.create_cfdi_data_from_payment()
            if not payment.payment_invoice_line_ids:
                raise UserError(_('Advertencia !!!\nNo se pudo generar el CFDI desde este asistente.\nGenere el pago y timbrelo desde el registro de pago.'))
            if payment.generar_cfdi and not payment.get_cfdi():
                raise UserError(_('Advertencia !!!\nOcurrió un error al intentar obtener el CFDI de Recepción de Pagos para el Pago: %s') % (payment.name))
            
        return res
    
    
    def action_cancel(self):
        res = super(AccountPayment, self).action_cancel()
        for payment in self:
            if not payment.journal_id.use_for_cfdi or not payment.cfdi_folio_fiscal:
                continue
            type__fc = payment.get_driver_cfdi_cancel()
            if payment.cfdi_pac in type__fc.keys():
                res2 = type__fc[payment.cfdi_pac]()
                payment.write({'cfdi_fecha_cancelacion':ti.strftime('%Y-%m-%d %H:%M:%S'),
                    #'date_invoice_cancel': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'cfdi_last_message': payment.cfdi_last_message + "\n-.-.-.-.-.-.-.-.-.-.-.-.-.\n" + \
                            fields.Datetime.to_string(fields.Datetime.context_timestamp(
                                                                            payment.with_context(tz=(self.env.user.partner_id.tz or 'America/Mexico_City')),
                                                                            datetime.datetime.now())
                                                                           ) + \
                                                            ' => ' + res2['message'] + u'\nCódigo: ' + res2['status_uuid']
                        })
                payment.payment_invoice_line_ids.unlink()
        #self.write({'state':'cancelled'})#, 'name' : 'Cancelado'})
        
        return res    
    
    def _get_file_globals(self):
        invoice_obj = self.env['account.move']
        ctx = self._context.copy()
        file_globals = {}
        ctx.update({'date_work': self.date_payment_tz})
        _logger.info("self.date_payment_tz: %s" % self.date_payment_tz)
        _logger.info("self.date_payment_tz.date(): %s" % self.date_payment_tz.date())
        if not (self.journal_id.date_start <= self.date_payment_tz.date() and self.journal_id.date_end >= self.date_payment_tz.date()):
            raise UserError(_("Error !!!\nLa fecha del Pago está fuera del rango de Vigencia del Certificado, por favor revise."))
        
        """
        self.env.cr.execute("select encode(certificate_file_pem, 'base64') certificate_file_pem, "
            "encode(certificate_key_file_pem, 'base64') certificate_key_file_pem, "
            "encode(certificate_file, 'base64') certificate_file, "
            "encode(certificate_key_file, 'base64') certificate_key_file, "
            "encode(certificate_pfx_file, 'base64') certificate_pfx_file "
            "from account_journal where id=%s;" % self.journal_id.id)
        resx = self.env.cr.fetchone()        
        certificate_file_pem     = base64.b64decode(str.encode(resx[0]))
        certificate_key_file_pem = base64.b64decode(str.encode(resx[1]))
        certificate_file         = base64.b64decode(str.encode(resx[2]))
        certificate_key_file     = base64.b64decode(str.encode(resx[3]))
        certificate_pfx_file     = base64.b64decode(str.encode(resx[4]))
        """
        certificate_file_pem     = self.journal_id.certificate_file_pem
        certificate_key_file_pem = self.journal_id.certificate_key_file_pem
        certificate_file         = self.journal_id.certificate_file
        certificate_key_file     = self.journal_id.certificate_key_file
        certificate_pfx_file     = self.journal_id.certificate_pfx_file

        
        fname_cer_pem = False
        #try:
        fname_cer_pem = invoice_obj.binary2file(certificate_file_pem, 'odoo_' + (self.journal_id.serial_number or '') + '__certificate__','.cer.pem')
        #except:
        #    raise UserError(_("Error !!! \nEl archivo del Certificado no existe en formato PEM"))
        
        file_globals['fname_cer'] = fname_cer_pem
        # - - - - - - - - - - - - - - - - - - - - - - -
        fname_key_pem = False
        #try:
        fname_key_pem = invoice_obj.binary2file(certificate_key_file_pem, 'odoo_' + (self.journal_id.serial_number or '') + '__certificate__','.key.pem')
        #except:
        #    raise UserError(_("Error !!! \nEl archivo de la llave (KEY) del Certificado no existe en formato PEM"))

        file_globals['fname_key'] = fname_key_pem
        # - - - - - - - - - - - - - - - - - - - - - - -
        fname_cer_no_pem = False
        #try:
        fname_cer_no_pem = invoice_obj.binary2file(certificate_file, 'odoo_' + (self.journal_id.serial_number or '') + '__certificate__','.cer')
        #except:
        #    pass
        file_globals['fname_cer_no_pem'] = fname_cer_no_pem
        # - - - - - - - - - - - - - - - - - - - - - - -
        fname_key_no_pem = False
        #try:
        fname_key_no_pem = invoice_obj.binary2file(certificate_key_file, 'odoo_' + (self.journal_id.serial_number or '') + '__certificate__', '.key')
        #except:
        #    pass
        file_globals['fname_key_no_pem'] = fname_key_no_pem
        # - - - - - - - - - - - - - - - - - - - - - - -
        fname_pfx = False
        #try:
        fname_pfx = invoice_obj.binary2file(certificate_pfx_file, 'odoo_' + (self.journal_id.serial_number or '') + '__certificate__', '.pfx')
        #except:
        #    raise UserError(_("Error !!! \nEl archivo del Certificado no existe en formato PFX"))

        file_globals['fname_pfx'] = fname_pfx
        # - - - - - - - - - - - - - - - - - - - - - - -
        file_globals['password'] = self.journal_id.certificate_password
        # - - - - - - - - - - - - - - - - - - - - - - -
        if self.journal_id.fname_xslt:
            if (self.journal_id.fname_xslt[0] == os.sep or \
                self.journal_id.fname_xslt[1] == ':'):
                file_globals['fname_xslt'] = self.journal_id.fname_xslt
            else:
                file_globals['fname_xslt'] = os.path.join(
                    tools.config["root_path"], self.journal_id.fname_xslt)
        else:
            # Search char "," for addons_path, now is multi-path
            all_paths = tools.config["addons_path"].split(",")
            for my_path in all_paths:
                if os.path.isdir(os.path.join(my_path,'l10n_mx_einvoice', 'SAT')):
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

        file_globals['serial_number'] = self.journal_id.serial_number
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
    
    
    def get_jinja_template_path(self, xml_template):
        ftemplate = False
        all_paths = tools.config["addons_path"].split(",")
        for my_path in all_paths:
            if os.path.isdir(os.path.join(my_path, 'l10n_mx_einvoice', 'template')):
                ftemplate = (my_path and os.path.join(my_path, 'l10n_mx_einvoice', 'template', xml_template)) or ''
                break
        return ftemplate

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
        #cfdi = str.encode(cfdi_signed)
        cfdi = fromstring(cfdi_signed)
        cfdi = self.account_invoice_tfd_node(cfdi)
        #return the cadena
        return self.get_cfdi_cadena(xslt_path, cfdi)

    @api.model
    def account_invoice_tfd_node(self, cfdi):
        attribute = 'tfd:TimbreFiscalDigital[1]'
        namespace = {'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital'}
        node = cfdi.Complemento.xpath(attribute, namespaces=namespace)
        return node[0] if node else None


    def create_cfdi_data_from_payment(self):
        #if self.payment_type!='inbound' or not payment.journal_id.use_for_cfdi:
        #    return False
        payment_line_obj = self.env['account.payment.invoice']
        invoice_obj = self.env['account.move']
        payment = self
        monto_aplicado = 0.0    
        invoices_related_to_payment = payment.reconciled_invoice_ids
        if not invoices_related_to_payment:
            invoices_related_to_payment = invoice_obj.search([('payment_id','=',payment.id)])
        for invoice in invoices_related_to_payment.sorted(key=lambda x: (x.invoice_date_due, x.name)):
            monto_aplicado = 0.0 
            data = {'payment_id': payment.id,
                    'invoice_id': invoice.id,
                   }
            monto_pago = 0.0
            for xline in payment.move_id.line_ids:
                for r in xline.matched_debit_ids:
                    _logger.info("=====================")
                    for x in r._fields:
                        _logger.info("%s: %s" % (x, r[x]))
                    if r.debit_move_id.move_id.id == invoice.id:
                        if invoice.currency_id == invoice.company_id.currency_id == payment.currency_id:
                            monto_pago = r.amount
                        elif (invoice.company_id.currency_id == payment.currency_id and \
                            invoice.currency_id != invoice.company_id.currency_id) or \
                            invoice.currency_id == payment.currency_id:
                            monto_pago = r.debit_amount_currency
                        else:
                            monto_pago = invoice.company_id.currency_id.with_context({'date': invoice.date_invoice}).compute(r.amount, invoice.currency_id)
            last_data = {}
            _logger.info("monto_pago: %s" % monto_pago)
            if monto_pago:
                ##########
                pagos = invoice._get_reconciled_info_JSON_values()
                _logger.info("pagos: %s" %  pagos)
                for xdata in pagos:
                    _logger.info("data: %s" % xdata)    
                
                saldo_anterior = invoice.amount_residual + monto_pago
                data.update({'parcialidad'  : len(invoice._get_reconciled_payments().filtered(lambda p: p.state not in ('draft', 'cancelled') and not p.move_id.line_ids.mapped('move_id.reversed_entry_id')).ids),
                            'saldo_anterior': saldo_anterior,
                            'monto_pago'    : monto_pago,
                            })
                xres = payment_line_obj.create(data)
        return True

    def get_cfdi(self):
        attachment_obj = self.env['ir.attachment']
        for payment in self:
            if not payment.payment_invoice_line_ids:
                payment.create_cfdi_data_from_payment()
            currency = payment.currency_id
            rate = payment.currency_id.with_context({'date': self.date}).rate
            rate = rate != 0 and 1.0/rate or 0.0
            if rate == 1.0:
                rate = 1
            ## Guardando el Tipo de Cambio ##
            payment.write({'tipo_cambio'        : float('%.4f' % rate), 
                           'user_id'            : self.env.user.id,
                           'payment_datetime'   : fields.datetime.now()})            
            fname_payment = payment.fname_payment
            cfdi_state = payment.cfdi_state
            if cfdi_state =='draft':
                fname, xml_data = payment.get_xml_to_sign()
                if not xml_data:
                    raise UserError(_('Error al generar el archivo XML para mandar a Timbrar. Por favor revise el LOG'))
                payment.write({
                            'xml_file_no_sign_index': xml_data,
                            'cfdi_state'            : 'xml_unsigned',
                            'cfdi_last_message'     : fields.Datetime.to_string(fields.Datetime.context_timestamp(
                                                                                payment.with_context(tz=(self.env.user.partner_id.tz or 'America/Mexico_City')),
                                                                                datetime.datetime.now())
                                                                               ) + \
                                                        '=> Archivo XML generado exitosamente'
                    })
                cfdi_state = 'xml_unsigned'

            # Mandamos a Timbrar
            type = payment.cfdi_pac
            if cfdi_state =='xml_unsigned' and not payment.xml_file_signed_index:
                try:
                    index_xml = ''
                    msj = ''        
                    # Instanciamos la clase para la integración con el PAC
                    type__fc = payment.get_driver_cfdi_sign()
                    if type in type__fc.keys():
                        fname_payment = payment.fname_payment and payment.fname_payment + \
                            '.xml' or ''
                        if not 'fname' in locals() or not 'xml_data' in locals():
                            _logger.info('Re-intentando generar XML para timbrar - Pago: %s', fname_payment)
                            fname, xml_data = payment.get_xml_to_sign()
                        else:
                            _logger.info('Listo archivo XML a timbrar en el PAC - Pago: %s', fname_payment)

                        fdata = base64.encodebytes(xml_data)
                        _logger.info('Solicitando a PAC el Timbre para Pago: %s', fname_payment)
                        res = type__fc[type](fdata) #
                        _logger.info('Timbre entregado por el PAC - Pago: %s', fname_payment)
                        msj = tools.ustr(res.get('msg', False))
                        index_xml = res.get('cfdi_xml', False)
                        if isinstance(index_xml, str):
                            index_xml = str.encode(index_xml)
                        payment.write({'xml_file_signed_index' : index_xml})
                        ###### Recalculando la Cadena Original ############
                        cfdi_signed = fdata
                        cadena_tfd_signed = ""
                        try:
                            cadena_tfd_signed = payment._get_einvoice_cadena_tfd(index_xml)
                        except:
                            cadena_tfd_signed = payment.cfdi_cadena_original
                        payment.cfdi_cadena_original = cadena_tfd_signed
                        ################ FIN ################
                        data_attach = {
                                'name'        : fname_payment,
                                'datas'       : base64.encodebytes(index_xml),
                                'store_fname' : fname_payment,
                                'description' : 'Archivo XML del Comprobante Fiscal Digital - Pago: %s' % (payment.name),
                                'res_model'   : 'account.payment',
                                'res_id'      : payment.id,
                                'type'        : 'binary',
                            }
                        attach = attachment_obj.with_context({}).create(data_attach)
                        xres = payment.do_something_with_xml_attachment(attach)
                        cfdi_state = 'xml_signed'
                    else:
                        msj += _("No se encontró el Driver del PAC para %s" % (type))
                    payment.write({'cfdi_last_message': payment.cfdi_last_message + "\n-.-.-.-.-.-.-.-.-.-.-.-.-.\n" + \
                                fields.Datetime.to_string(fields.Datetime.context_timestamp(
                                                                                payment.with_context(tz=(self.env.user.partner_id.tz or 'America/Mexico_City')),
                                                                                datetime.datetime.now())
                                                                               ) + \
                                                                ' => ' + msj})                
                except Exception:
                    error = tools.ustr(traceback.format_exc())
                    payment.write({'cfdi_last_message': payment.cfdi_last_message + "\n-.-.-.-.-.-.-.-.-.-.-.-.-.\n" + \
                                fields.Datetime.to_string(fields.Datetime.context_timestamp(
                                                                                payment.with_context(tz=(self.env.user.partner_id.tz or 'America/Mexico_City')),
                                                                                datetime.datetime.now())
                                                                               ) + \
                                                                ' => ' + error})
                    _logger.error(error)
                    return False
                payment.write({'cfdi_state': 'xml_signed'})
            # Generamos formato de Impresión
            if cfdi_state == 'xml_signed' or payment.xml_file_signed_index:
                _logger.info('Generando PDF - Pago: %s', fname_payment)
                cfdi_state = 'pdf'
                
                try:
                    msj = ''
                    self.write({
                               'cfdi_last_message': self.cfdi_last_message + "\n-.-.-.-.-.-.-.-.-.-.-.-.-.\n" + \
                                fields.Datetime.to_string(fields.Datetime.context_timestamp(
                                                                                self.with_context(tz=(self.env.user.partner_id.tz or 'America/Mexico_City')),
                                                                                datetime.datetime.now())
                                                                               ) + \
                                                                u' => Archivo PDF generado satisfactoriamente',
                               })
                    cfdi_state = 'pdf'
                    _logger.info('PDF generado - Pago: %s', fname_payment)
                except:
                    error = tools.ustr(traceback.format_exc())
                    self.write({'cfdi_last_message': self.cfdi_last_message + "\n-.-.-.-.-.-.-.-.-.-.-.-.-.\n" + \
                                fields.Datetime.to_string(fields.Datetime.context_timestamp(
                                                                                self.with_context(tz=(self.env.user.partner_id.tz or 'America/Mexico_City')),
                                                                                datetime.datetime.now())
                                                                               ) + \
                                                                u' => No se pudo generar el formato de Impresión, revise el siguiente Traceback:\n\n' + \
                                                                error})

                    _logger.error(error)
                payment.write({'cfdi_state': 'pdf'})
                
            
            if cfdi_state == 'pdf' and payment.partner_id.commercial_partner_id.envio_manual_cfdi:
                msj = _('No se enviaron los archivos por correo porque el Partner está marcado para no enviar automáticamente los archivos del CFDI (XML y PDF)')
                cfdi_state == 'sent'
                payment.write({'cfdi_last_message': payment.cfdi_last_message + "\n-.-.-.-.-.-.-.-.-.-.-.-.-.\n" + \
                                                fields.Datetime.to_string(fields.Datetime.context_timestamp(
                                                payment.with_context(tz=(self.env.user.partner_id.tz or 'America/Mexico_City')),
                                                datetime.datetime.now())
                                               ) + \
                                                ' => ' + msj,
                                'cfdi_state': 'sent',
                                })
            # Enviamos al cliente los archivos de la factura
            elif cfdi_state == 'pdf' and not payment.partner_id.commercial_partner_id.envio_manual_cfdi:
                _logger.info('Intentando enviar XML y PDF por mail al cliente - Pago: %s', fname_payment)
                msj = ''
                state = ''
                partner_mail = payment.partner_id.email or False
                user_mail = self.env.user.email or False
                company_id = payment.company_id.id
                address_id = payment.partner_id.address_get(['invoice'])['invoice']
                partner_invoice_address = address_id
                fname_payment = payment.fname_payment or ''
                adjuntos = attachment_obj.search([('res_model', '=', 'account.payment'), 
                                                  ('res_id', '=', payment.id)])
                q = True
                attachments = []
                for attach in adjuntos:
                    if q and attach.name.endswith('.xml'):
                        attachments.append(attach.id)
                        break

                mail_compose_message_pool = self.env['mail.compose.message']
                #report_ids = payment.journal_id.report_id or False 
                #if report_ids:
                #    report_name = report_ids.report_name
                #    if report_name:
                template_id = self.env['mail.template'].search([('model_id.model', '=', 'account.payment')], limit=1)                            

                if template_id:
                    ctx = dict(
                        default_model='account.payment',
                        default_res_id=payment.id,
                        default_use_template=bool(template_id),
                        default_template_id=template_id.id,
                        default_composition_mode='comment',
                    )
                    ## CHERMAN 
                    context2 = dict(self._context)
                    if 'default_journal_id' in context2:
                        del context2['default_journal_id']
                    if 'default_type' in context2:
                        del context2['default_type']
                    if 'search_default_dashboard' in context2:
                        del context2['search_default_dashboard']

                    xres = mail_compose_message_pool.with_context(context2)._onchange_template_id(template_id=template_id.id, 
                                                                                                 composition_mode=None,
                                                                                                 model='account.payment', 
                                                                                                 res_id=payment.id)
                    try:
                        try:
                            attachments.append(xres['value']['attachment_ids'][0][2][0])
                        except:
                            mail_attachments = (xres['value']['attachment_ids'])
                            for mail_atch in mail_attachments:
                                if mail_atch[0] == 4:
                                    # attachments.append(mail_atch[1])
                                    attach_br = self.env['ir.attachment'].browse(mail_atch[1])
                                    if attach_br.name != fname_payment+'.pdf':
                                        attach_br.write({'name': fname_payment+'.pdf'})
                                    attachments.append(mail_atch[1])
                    except:
                        _logger.error('No se genero el PDF del CFDI, no se enviara al cliente. - Pago: %s', fname_payment)
                    xres['value'].update({'attachment_ids' : [(6, 0, attachments)]})
                    message = mail_compose_message_pool.with_context(ctx).create(xres['value'])
                    _logger.info('Antes de  enviar XML y PDF por mail al cliente - Pago: %s', fname_payment)
                    xx = message.action_send_mail()
                    _logger.info('Despues de  enviar XML y PDF por mail al cliente - Pago: %s', fname_payment)
                    payment.write({'cfdi_state': 'sent'})
                    msj = _("El CFDI fue enviado exitosamente por correo electrónico...")
                    cfdi_state == 'sent'
                else:
                    msj = _('Advertencia !!!\nRevise que su plantilla de correo esté asignada al Servidor de correo.\nTambién revise que tenga asignado el reporte a usar.\nLa plantilla está asociada a la misma Compañía')

                payment.write({'cfdi_last_message': payment.cfdi_last_message + "\n-.-.-.-.-.-.-.-.-.-.-.-.-.\n" + \
                                                fields.Datetime.to_string(fields.Datetime.context_timestamp(
                                                payment.with_context(tz=(self.env.user.partner_id.tz or 'America/Mexico_City')),
                                                datetime.datetime.now())
                                               ) + \
                                                ' => ' + msj,
                                })
            _logger.info('Fin proceso Timbrado - Pago: %s', fname_payment)
            
            
            # Se encontraron que los archivos PDF se duplican
            adjuntos2 = attachment_obj.search([('res_model', '=', 'account.payment'), ('res_id', '=', payment.id)])
            x = 0
            for attach in adjuntos2:
                if attach.name.endswith('.pdf'):
                    x and attach.unlink()
                    if x: 
                        break
                    x += 1
        self.env.cr.commit()
        _logger.info('Se forzo el volcado del Pago Timbrado: %s', fname_payment)
        return True
    
    
    
    def get_xml_to_sign(self):    
        self.ensure_one()
        context = self._context.copy()
        facturae_version = "3.3"
        if not self.pay_method_id:
            raise UserError(_('Error !!!\nNo ha definido el método de Pago. Recuerde que este Método de Pago es diferente al de Contabilidad Electrónica (Definido en el diario contable de Pago)'))
        invoice_obj = self.env['account.move']
        if not self.journal_id.use_for_cfdi:
            return False
        context.update(self._get_file_globals())
        cert_str = invoice_obj._get_certificate_str(context['fname_cer'])
        if not cert_str:
            raise UserError(_("Error en Certificado !!!\nNo puedo obtener el Certificado del Comprobante. Revise su configuración."))        
        cert_str = cert_str.replace('\n\r', '').replace('\r\n', '').replace('\n', '').replace('\r', '').replace(' ', '')
        noCertificado = self.journal_id.serial_number       
        if not noCertificado:
            raise UserError(_("Error !!!\n\nNo se pudo obtener el Número de Certificado para generar el CFDI. Por favor revise la configuración del Diario de Pago"))
        # Folio
        try:
            number_work = self.name.split('/%s/' % str(datetime.now().year))[1]
        except:
            xnumber_work = re.findall('\d+', self.name) or False
            number_work = xnumber_work and xnumber_work[0] or xnumber_work
        #Emisor
        address_payment = self.address_issued_id or False
        address_payment_parent = self.company_emitter_id and self.company_emitter_id.address_invoice_parent_company_id or False
        if not address_payment_parent:
            address_payment_parent = self.company_emitter_id.partner_id
        if not address_payment:
            raise UserError(_('Advertencia !!\nNo ha definido dirección de emisión...'))
        if not address_payment_parent:
            raise UserError(_('Advertencia !!\nNo ha definido la dirección de la Compañía...'))
        if not address_payment_parent.vat:
            raise UserError(_('Advertencia !!\nNo ha definido el RFC de la Compañía...'))
        invoice_obj.check_partner_data(self.partner_id, True)
        invoice_obj.check_partner_data(self.address_issued_id, True)
        invoice_obj.check_partner_data(address_payment_parent, False)  
        # Validamos el Regimen Fiscal
        if not self.env.company.regimen_fiscal_id:
            raise UserError(_('No ha definido el Régimen Fiscal de la Compañía Emisora'))            
        # Receptor
        parent_obj = self.partner_id.commercial_partner_id
        if not parent_obj.vat:
            raise UserError(_('Advertencia !!\nNo ha definido el RFC para la Empresa [%s] !') % (parent_obj.name))
        receptor_nombre = parent_obj.name
        if parent_obj.country_id.code != 'MX':
            receptor_rfc = 'XEXX010101000'
        else:
            receptor_rfc = parent_obj.vat
            if 'cfdi_complemento' in self._fields and self.cfdi_complemento=='factoraje' and \
                'supplier_factor' in self._fields and self.supplier_factor:
                receptor_rfc = self.supplier_factor.vat
                receptor_nombre = self.supplier_factor.name
        address_invoice = self.partner_id
        ResidenciaFiscal, NumRegIdTrib = False, False
        if address_invoice.country_id.sat_code.upper() != 'MEX':
            if not address_invoice.num_reg_trib:
                raise UserError(_("Error!\nPara clientes con dirección en el extranjero es necesario ingresar el registro de identidad fiscal."))
            ResidenciaFiscal = address_invoice.country_id.sat_code
            NumRegIdTrib = address_invoice.num_reg_trib
        fecha = self.date_payment_tz.strftime('%Y-%m-%dT%H:%M:%S') or ''
        fecha_recepcion = self.date_payment_reception_tz.strftime('%Y-%m-%dT%H:%M:%S') or ''
        #fecha = ti.strftime('%Y-%m-%dT%H:%M:%S', ti.strptime(str(self.date_payment_tz), '%Y-%m-%d %H:%M:%S'))
        #fecha_recepcion = ti.strftime('%Y-%m-%dT%H:%M:%S', ti.strptime(str(self.date_payment_reception_tz), '%Y-%m-%d %H:%M:%S'))
        if self.date_2_cfdi_tz:
            date_2_cfdi_tz = self.date_2_cfdi_tz.strftime('%Y-%m-%dT%H:%M:%S') or ''
            #date_2_cfdi_tz = ti.strftime('%Y-%m-%dT%H:%M:%S', ti.strptime(str(self.date_2_cfdi_tz), '%Y-%m-%d %H:%M:%S'))
        else:
            tz = self.env.user.partner_id.tz or 'America/Mexico_City'
            payment_datetime_to_sign = fields.Datetime.context_timestamp(
                                            self.with_context(tz=(self.env.user.partner_id.tz or 'America/Mexico_City')),
                                            datetime.datetime.now())
            date_2_cfdi_tz = payment_datetime_to_sign.strftime('%Y-%m-%dT%H:%M:%S') or ''
            #date_2_cfdi_tz = ti.strftime('%Y-%m-%dT%H:%M:%S', ti.strptime(str(payment_datetime_to_sign), '%Y-%m-%d %H:%M:%S'))
        if not self.env.company.regimen_fiscal_id:
            raise UserError("Error!\nLa Compañía %s no tiene definido un Regimen Fiscal, por lo cual no puede emitir el Recibo CFDI." % address_payment_parent.name)
        dictargs2 = {
            'o'             : self,
            'time'          : ti,
            'emisor_rfc'    : address_payment_parent.vat,
            'emisor_nombre' : address_payment_parent.name,
            'emisor_regimen': self.env.company.regimen_fiscal_id.code,
            'receptor_rfc'  : receptor_rfc.upper(),
            'receptor_nombre': receptor_nombre or '',
            'ResidenciaFiscal' : ResidenciaFiscal,
            'NumRegIdTrib'  : NumRegIdTrib,
            'noCertificado' : noCertificado,
            'certificado'   : cert_str,
            'serie'         : (self.journal_id.code or '').replace('-', '').replace('/','').replace(' ','').replace('.',''),
            'folio'         : number_work, #int(number_work),
            'fecha'         : fecha,
            'date_2_cfdi_tz': date_2_cfdi_tz,
            'fecha_recepcion' : fecha_recepcion,
            }

        ### Datos Bancarios en XML ###
        #if self.cmpl_type in ('transfer','check'):
        if self.pay_method_id.code in ('02','03'):
            if self.no_data_bank_in_xml:
                dictargs2.update({
                    'rfcemisorctaord': '',
                    'nombancoordext': '',
                    'ctaordenante': '',
                    'rfcemisorctaben': '',
                    'ctabeneficiario': '',
                    })
            else:
                if not self.journal_id.bank_account_id:
                    raise UserError("El Diario %s\n No cuenta con el Numero de Cuenta establecido." % self.journal_id.name)
                if not self.journal_id.bank_id:
                    raise UserError("El Diario %s\n No cuenta con el Banco de la Cuenta establecida." % self.journal_id.name)
                if not self.journal_id.bank_id.vat:
                    raise UserError("El Banco %s\n No tiene definido el RFC, este dato es necesario para el complemento de pagos." % self.journal_id.bank_id.name)
                if not self.partner_bank_id:
                    raise UserError("No se ha definido cuenta Bancaria para el Complemento")
                if not self.partner_bank_id.bank_id.vat:
                    raise UserError("El Banco %s del Cliente\n No tiene definido el RFC, este dato es necesario para el complemento." % self.partner_bank_id.bank_id.name)
                if self.pay_method_id.code == '03':
                    _estructura_cuenta = re.compile('[0-9]{10}|[0-9]{16}|[0-9]{18}')
                    if not _estructura_cuenta.match(self.partner_bank_id.acc_number):
                        raise UserError("La Cuenta %s del Cliente\n No cumple con la estructura del SAT." % self.partner_bank_id.acc_number )
                dictargs2.update({
                    'rfcemisorctaord': self.partner_bank_id.bank_id.vat,
                    'nombancoordext': self.partner_bank_id.bank_id.name,
                    'ctaordenante': self.partner_bank_id.acc_number,
                    'rfcemisorctaben': self.journal_id.bank_id.vat,
                    'ctabeneficiario': self.journal_id.bank_account_id.acc_number,
                    })

                
        context.update({'fecha': self.date_payment_tz.strftime('%Y-%m-%dT%H:%M:%S') or ''})
        fname_jinja_tmpl = self.get_jinja_template_path('jinja_cfdi.xml')
        (fileno_xml, fname_xml) = tempfile.mkstemp('.xml', 'odoo_' + '__facturae_pay__')
        with open(fname_jinja_tmpl, 'r') as f_jinja_tmpl:
            jinja_tmpl_str = f_jinja_tmpl.read()
            tmpl = jinja2.Template( jinja_tmpl_str )
            with open(fname_xml, 'w') as new_xml:
                new_xml.write( tmpl.render(**dictargs2) )
                new_xml.close()
        with open(fname_xml,'rb') as b:
            data_xml = b.read() #.encode('UTF-8')
        b.close()

        fname_txt = fname_xml + '.txt'
        (fileno_sign, fname_sign) = tempfile.mkstemp('.txt', 'odoo_' + '__facturae_pay_txt_md5__')
        os.close(fileno_sign)
        #Agregar nodo Pagos en nodo Complemento
        doc_xml = xml.dom.minidom.parseString(data_xml)
        doc_xml_full = doc_xml.toxml().encode('ascii', 'xmlcharrefreplace')
        data_xml2 = xml.dom.minidom.parseString(doc_xml_full)
        f = codecs.open(fname_xml,'w','utf-8')
        data_xml2.writexml(f, indent='    ', addindent='    ', newl='\r\n', encoding='UTF-8')
        f.close()
        context.update({
            'fname_xml': fname_xml,
            'fname_txt': fname_txt,
            'fname_sign': fname_sign,
        })
        context.update({'xml_prev':doc_xml_full})#doc_xml.toxml('UTF-8')})
        txt_str = invoice_obj.with_context(context)._xml2cad_orig()
        if not txt_str:
            raise UserError(_("Error en la Cadena Original !!!\nNo puedo obtener la Cadena Original del Comprobante. Revise su configuración."))
        context.update({'cadena_original': txt_str})
        self.write({'cfdi_cadena_original':txt_str, 'no_certificado':noCertificado})
        #context.update({'fecha': date_now or ''})
        sign_str = invoice_obj.with_context(context)._get_sello()
        nodeComprobante = data_xml2.getElementsByTagName("cfdi:Comprobante")[0]
        nodeComprobante.setAttribute("Sello", sign_str)
        self.write({'sello':sign_str})
        data_xml = data_xml2.toxml('UTF-8')
        #~data_xml = codecs.BOM_UTF8 + data_xml
        data_xml = data_xml.replace(b'<?xml version="1.0" encoding="UTF-8"?>', b'<?xml version="1.0" encoding="UTF-8"?>\n')
        #if self.company_id.validate_schema:
        #    invoice_obj.validate_scheme_facturae_xml([data_xml], facturae_version)
        return fname_xml, data_xml
    
    
    ################################################
    
    
    def do_something_with_xml_attachment(self, attach):
        return True
    
    
    
    @api.depends('amount','currency_id')
    def _get_amount_to_text(self):
        for rec in self:
            currency_inst = False
            if rec.company_id:
                currency = rec.company_id.currency_id.name.upper()
                currency_inst = rec.company_id.currency_id
            else:
                currency  =  self.env.user.company_id.currency_id.name.upper()
                currency_inst = self.env.user.company_id.currency_id
            # M.N. = Moneda Nacional (National Currency)
            # M.E. = Moneda Extranjera (Foreign Currency)
            currency_type = 'M.N' if currency == 'MXN' else 'M.E.'
            # Split integer and decimal part
            amount_i, amount_d = divmod(rec.amount, 1)
            amount_d = round(amount_d, 2)
            amount_d = int(amount_d * 100)
            words = currency_inst.with_context(lang=self.env.user.partner_id.lang or 'es_ES').amount_to_text(amount_i).upper()
            invoice_words = '%(words)s %(amount_d)02d/100 %(curr_t)s' % dict(
                words=words, amount_d=amount_d, curr_t=currency_type)
            if rec.currency_id.name.upper() != 'MXN':
                invoice_words = invoice_words.replace('PESOS', rec.currency_id.name.upper())
                invoice_words = invoice_words.replace('M.N','M.E.')
                invoice_words = invoice_words.replace('M.N.','M.E.')
            rec.amount_to_text = invoice_words
        
        
        
    
    @api.depends('journal_id')
    def _get_address_issued_invoice(self):
        for rec in self:
            rec.address_issued_id = rec.journal_id.address_invoice_company_id or \
                                    (rec.journal_id.company2_id and rec.journal_id.company2_id.address_invoice_parent_company_id) or \
                                    rec.journal_id.company_id.address_invoice_parent_company_id or False
            rec.company_emitter_id = rec.journal_id.company2_id or rec.journal_id.company_id or False
        
    def get_server_timezone(self):
        return "UTC"
    
    
    def server_to_local_timestamp(self, fecha, dst_tz_name,
            tz_offset=True, ignore_unparsable_time=True):
        if not fecha:
            return False
        res = fecha
        server_tz = self.get_server_timezone()
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
            hours = pytz.timezone(userstz)
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
    
    
