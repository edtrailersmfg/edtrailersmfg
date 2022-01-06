# -*- encoding: utf-8 -*-   
from odoo import api, fields, models, _, tools
from . import cancelation_codes ## Clase con Mucha Informacion
from zeep import Client
from odoo.exceptions import UserError, ValidationError

class AccountMove(models.Model):
    _inherit = 'account.move'

    #####################################
    cfdi_pac = fields.Selection(selection_add=[('pac_sf', 'Solución Factible - https://www.solucionfactible.com')], 
                                string='CFDI Pac', readonly=True, store=True, copy=False, default='pac_sf',
                                ondelete={'pac_sf': 'set null'})
    
    #####################################

    motivo_cancelacion = fields.Selection([
        ('01', '[01] Comprobantes emitidos con errores con relación'),
        ('02', '[02] Comprobantes emitidos con errores sin relación'),
        ('03', '[03] No se llevó a cabo la operación'),
        ('04', '[04] Operación nominativa relacionada en una factura global')
    ], required=False, string="Motivo Cancelación", copy=False)
    
    
    uuid_relacionado_cancelacion = fields.Char(string="UUID Relacionado en Cancelación", copy=False)
        
    def cancelation_request_create(self):
        if self.journal_id.use_for_cfdi and self.cfdi_folio_fiscal and not self.motivo_cancelacion:
            raise UserError("Debe ingresar el motivo de la cancelación desde la pestaña CFDI Info")
        return super(AccountMove, self).cancelation_request_create()

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    #####################################
    cfdi_pac = fields.Selection(selection_add=[('pac_sf', 'Solución Factible - https://www.solucionfactible.com')], 
                                string='CFDI Pac', readonly=True, store=True, copy=False, default='pac_sf',
                                ondelete={'pac_sf': 'set null'})
    #####################################        

    motivo_cancelacion = fields.Selection([
        ('01', '[01] Comprobantes emitidos con errores con relación'),
        ('02', '[02] Comprobantes emitidos con errores sin relación'),
        ('03', '[03] No se llevó a cabo la operación'),
        ('04', '[04] Operación nominativa relacionada en una factura global')
    ], required=False, string="Motivo Cancelación", copy=False)
    
    
    uuid_relacionado_cancelacion = fields.Char(string="UUID Relacionado en Cancelación", copy=False)
        

    def action_cancel(self):
        if self.journal_id.use_for_cfdi and self.cfdi_folio_fiscal and not self.motivo_cancelacion:
            raise UserError("Debe ingresar el motivo de la cancelación desde la pestaña CFDI Info")
        return super(AccountPayment, self).action_cancel()

class AccountMoveCancelationRecord(models.Model):
    _inherit = 'account.move.cancelation.record'


    production_url  = 'https://solucionfactible.com/ws/services/Cancelacion?wsdl'
    testing_url     = 'https://testing.solucionfactible.com/ws/services/Cancelacion?wsdl'   
    
    
    def solitud_cancelacion_asincrona(self):
        for rec in self:
            if rec.invoice_id:
                msg = ''
                state = ''
                folio_fiscal = ''
                message_invisible = ''
                invoice_rec = rec.invoice_id
                if invoice_rec.company_id.pac_testing or (invoice_rec.company_id.pac_user and invoice_rec.company_id.pac_password):
                    file_globals = invoice_rec._get_file_globals()
                    user        = invoice_rec.company_id.pac_testing and 'testing@solucionfactible.com' or invoice_rec.company_id.pac_user
                    password    = invoice_rec.company_id.pac_testing and 'timbrado.SF.16672' or invoice_rec.company_id.pac_password
                    ### Inicio Belchez
                    # Se agrega un espacio al password de Belchez
                    if invoice_rec.company_id.partner_id.vat == 'TBE740319AP4':
                        password += ' '
                    ### FIN Belchez
                    wsdl_url    = self.testing_url if invoice_rec.company_id.pac_testing else self.production_url
                    rfc_emisor  = invoice_rec.company_id.partner_id.vat
                    if 'MX' in rfc_emisor[0:2]:
                        rfc_emisor = rfc_emisor[2:]
                    email_emisor  = invoice_rec.company_id.partner_id.email
                    if not email_emisor:
                        raise UserError("Error!\nLa Compañia no cuenta con una direccion de correo.")
                    fcer = open(file_globals['fname_cer_no_pem'], "rb")
                    fkey = open(file_globals['fname_key_no_pem'], "rb")
                    cerCSD = fcer.read()
                    keyCSD = fkey.read()
                    fcer.close()
                    fkey.close()
                    contrasenaCSD = invoice_rec.journal_id.certificate_password
                    #if invoice_rec.company_id.partner_id.vat == 'TBE740319AP4':
                    #    contrasenaCSD += ' '
                    client = Client(wsdl_url)
                    isZipFile = 0
                    # print("######### (user, password, invoice_rec.cfdi_folio_fiscal, rfc_emisor, email_emisor, cerCSD, keyCSD, contrasenaCSD) >>>>> \n",(user, password, invoice_rec.cfdi_folio_fiscal, rfc_emisor, email_emisor, cerCSD, keyCSD, contrasenaCSD))
                    try:
                        uuid_cancelacion_motivo = '%s|%s|%s' % (invoice_rec.cfdi_folio_fiscal, invoice_rec.motivo_cancelacion, 
                                                 invoice_rec.uuid_relacionado_cancelacion or '')
                        resultado = client.service.cancelarAsincrono(user, password, uuid_cancelacion_motivo, rfc_emisor, email_emisor, cerCSD, keyCSD, contrasenaCSD)
                    except WebFault as f:
                        raise UserError(_('Advertencia !!!\nOcurrió un error al intentar Cancelar el CFDI.'))
                    code_result = resultado.status
                    msg_result = resultado.mensaje
                    instance_class_codes = cancelation_codes.CancelationSFCodes()
                    msg_code = instance_class_codes.return_message_by_code(str(code_result))
                    if code_result == 204:
                        invoice_rec.mailbox_state = 'no_cancel'
                        invoice_rec.cfdi_state = 'uuid_no_cancel'
                        rec.state = 'no_cancel'
                        rec.folio_fiscal = msg_result 
                        rec.message_invisible = '204 - '+ msg_code
                    if code_result == 213:
                        invoice_rec.mailbox_state = 'rejected'
                        invoice_rec.cfdi_state = 'uuid_no_cancel_by_customer'
                        rec.state = 'rejected'
                        rec.folio_fiscal = msg_result 
                        rec.message_invisible = '213 - '+ msg_code
                    
                    if resultado.status == 200:
                        msg +=  '\n- Cancelación Exitosa.\n- UUID Cancelado es: %s\nMensaje: %s' % (invoice_rec.cfdi_folio_fiscal, msg_code)
                        status_uuid = msg_code
                        status = True
                        rec.state = 'done'
                        rec.folio_fiscal = msg_result 
                        rec.message_invisible = str(code_result)+' - '+ msg_code
                        invoice_rec.mailbox_state = 'done'
                        invoice_rec.cfdi_state = 'cancel'
                    else:
                        msg +=  '\n- Cancelación en Proceso.\n- UUID Cancelado es: %s\nMensaje: %s' % (invoice_rec.cfdi_folio_fiscal, msg_code)
                        status_uuid = msg_code
                        status = True
                        rec.state = 'process'
                        rec.folio_fiscal = msg_result 
                        rec.message_invisible = str(code_result)+' - '+ msg_code
                        invoice_rec.mailbox_state = 'process'
                        invoice_rec.cfdi_state = 'in_process_cancel'
                        #raise UserError(_('Advertencia!\nCódigo de Cancelación: %s. - Mensaje: %s') % (resultado.status, resultado.mensaje))
                else:
                    msg = _('No se configuró correctamente los datos del PAC, revise los parámetros del PAC')
                return {
                        'state': state,
                        'folio_fiscal': folio_fiscal,
                        'message_invisible': message_invisible,
                    }



    
    
    def solitud_cancelacion_consulta_status(self):
        ## Se deja Abierta la Conexion para la Consulta con el PAC ###
        for rec in self:
            if rec.invoice_id:
                msg = ''
                state = ''
                folio_fiscal = ''
                message_invisible = ''
                invoice_rec = rec.invoice_id
                if invoice_rec.company_id.pac_testing or (invoice_rec.company_id.pac_user and invoice_rec.company_id.pac_password):
                    file_globals = invoice_rec._get_file_globals()
                    user        = invoice_rec.company_id.pac_testing and 'testing@solucionfactible.com' or invoice_rec.company_id.pac_user
                    password    = invoice_rec.company_id.pac_testing and 'timbrado.SF.16672' or invoice_rec.company_id.pac_password
                    wsdl_url    = self.testing_url if invoice_rec.company_id.pac_testing else self.production_url
                    rfc_emisor  = invoice_rec.company_id.partner_id.vat
                    if 'MX' in rfc_emisor[0:2]:
                        rfc_emisor = rfc_emisor[2:]
                    email_emisor  = invoice_rec.company_id.partner_id.email
                    if not email_emisor:
                        raise UserError("Error!\nLa Compañia no cuenta con una direccion de correo.")
                    fcer = open(file_globals['fname_cer_no_pem'], "rb")
                    fkey = open(file_globals['fname_key_no_pem'], "rb")
                    cerCSD = fcer.read()
                    keyCSD = fkey.read()
                    fcer.close()
                    fkey.close()
                    contrasenaCSD = invoice_rec.journal_id.certificate_password
                    if invoice_rec.company_id.partner_id.vat == 'TBE740319AP4':
                        contrasenaCSD += ' '
                    client = Client(wsdl_url)
                    isZipFile = 0
                    # print("######### (user, password, invoice_rec.cfdi_folio_fiscal, rfc_emisor, email_emisor, cerCSD, keyCSD, contrasenaCSD) >>>>> \n",(user, password, invoice_rec.cfdi_folio_fiscal, rfc_emisor, email_emisor, cerCSD, keyCSD, contrasenaCSD))
                    try:
                        resultado = client.service.getStatusCancelacionAsincrona(user, password, invoice_rec.cfdi_folio_fiscal)
                    except WebFault as f:
                        raise UserError(_('Advertencia !!!\nOcurrió un error al intentar Cancelar el CFDI.'))
                    code_result = resultado.status
                    msg_result = resultado.mensaje
                    try:
                        acusesat = resultado.acuseSat
                    except:
                        acusesat = ""
                    instance_class_codes = cancelation_codes.CancelationSFCodes()
                    msg_code = instance_class_codes.return_message_by_code_get_status(str(code_result))
                    if code_result == 204:
                        invoice_rec.mailbox_state = 'no_cancel'
                        invoice_rec.cfdi_state = 'uuid_no_cancel'
                        rec.state = 'no_cancel'
                        rec.folio_fiscal = msg_result 
                        rec.message_invisible = '204 - '+ msg_code + ' ---- Acuse SAT: '+str(acusesat)
                    if code_result == 213:
                        invoice_rec.mailbox_state = 'rejected'
                        invoice_rec.cfdi_state = 'uuid_no_cancel_by_customer'
                        rec.state = 'rejected'
                        rec.state = 'rejected'
                        rec.folio_fiscal = msg_result 
                        rec.message_invisible = '213 - '+ msg_code + ' ---- Acuse SAT: '+str(acusesat)
                    
                    if resultado.status == 200:
                        msg +=  '\n- Cancelación Exitosa.\n- UUID Cancelado es: %s\nMensaje: %s' % (invoice_rec.cfdi_folio_fiscal, msg_code)
                        status_uuid = msg_code
                        status = True
                        rec.state = 'done'
                        #rec.folio_fiscal = msg_result
                        rec.folio_fiscal = acusesat 
                        rec.message_invisible = str(code_result)+' - '+ msg_code + ' ---- Acuse SAT: '+str(acusesat)
                        invoice_rec.mailbox_state = 'done'
                        invoice_rec.cfdi_state = 'cancel'
                    else:
                        msg +=  '\n- Cancelación en Proceso.\n- UUID Cancelado es: %s\nMensaje: %s' % (invoice_rec.cfdi_folio_fiscal, msg_code)
                        status_uuid = msg_code
                        status = True
                        rec.state = 'process'
                        rec.folio_fiscal = msg_result 
                        rec.message_invisible = str(code_result)+' - '+ msg_code + ' ---- Acuse SAT: '+str(acusesat)
                        invoice_rec.mailbox_state = 'process'
                        invoice_rec.cfdi_state = 'in_process_cancel'
                        #raise UserError(_('Advertencia!\nCódigo de Cancelación: %s. - Mensaje: %s') % (resultado.status, resultado.mensaje))
                else:
                    msg = _('No se configuró correctamente los datos del PAC, revise los parámetros del PAC')
                return {
                        'state': state,
                        'folio_fiscal': folio_fiscal,
                        'message_invisible': message_invisible,
                    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:    
