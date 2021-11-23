# -*- encoding: utf-8 -*-   
from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError
from suds.client import Client, WebFault
from suds.plugin import MessagePlugin
from xml.dom.minidom import parse, parseString
from . import cancelation_codes ## Clase con Mucha Informacion
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

    
class AccountMove(models.Model):
    _inherit = 'account.move'

    #####################################
    cfdi_pac                = fields.Selection(selection_add=[('pac_sifei', 'SIFEI - https://www.sifei.com.mx')], string='CFDI Pac', readonly=True, store=True, copy=False, default='pac_sifei',
                                               ondelete={'pac_sifei': 'set null'})
    #####################################
        
class AccountPayment(models.Model):
    _inherit = 'account.payment'

    #####################################
    cfdi_pac                = fields.Selection(selection_add=[('pac_sifei', 'SIFEI - https://www.sifei.com.mx')], string='CFDI Pac', readonly=True, store=True, copy=False, default='pac_sifei',
                                               ondelete={'pac_sifei': 'set null'})
    #####################################        
    
    
class AccountMoveCancelationRecord(models.Model):
    _name = 'account.move.cancelation.record'
    _inherit = 'account.move.cancelation.record'


    production_url  = 'https://sat.sifei.com.mx:9000/CancelacionSIFEI/Cancelacion?wsdl'
    testing_url     = 'http://devcfdi.sifei.com.mx:8888/CancelacionSIFEI/Cancelacion?wsdl'   
    
    
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

                    user        = invoice_rec.company_id.pac_testing and invoice_rec.company_id.pac_user_4_testing or invoice_rec.company_id.pac_user
                    password    = invoice_rec.company_id.pac_testing and invoice_rec.company_id.pac_password_4_testing or invoice_rec.company_id.pac_password
                    equipo_id   = invoice_rec.company_id.pac_testing and invoice_rec.company_id.pac_equipo_id_4_testing or invoice_rec.company_id.pac_equipo_id

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
                    # fname_pfx = open(file_globals['fname_pfx'], "rb")
                    # certificate_pfx = fname_pfx.read()
                    # fname_pfx.close()
                    certificate_pfx = invoice_rec.journal_id.certificate_pfx_file.decode("utf-8")
                    contrasenaCSD = invoice_rec.journal_id.certificate_password
                    client = Client(wsdl_url, plugins=[LogPlugin()])
                    isZipFile = 0
                    code_result = ""

                    try:
                        resultado = client.service.cancelaCFDI(user, password, rfc_emisor,
                                                           certificate_pfx, file_globals['password'], invoice_rec.cfdi_folio_fiscal)
                        xml_respuesta = parseString(resultado)
                        if xml_respuesta.getElementsByTagName('Acuse'):
                            timbre = xml_respuesta.getElementsByTagName('Acuse')[0]
                            if timbre.getElementsByTagName('Folios'):
                                folios = timbre.getElementsByTagName('Folios')[0]
                                if folios.getElementsByTagName('EstatusUUID'):
                                    estatusuuid = folios.getElementsByTagName('EstatusUUID')[0].firstChild
                                    code_result = estatusuuid.data

                    except WebFault as f:
                        raise UserError(_('Advertencia !!!\nOcurrió un error al intentar Cancelar el Timbre. \n\nCódigo: %s\nError: %s\nMensaje: %s') % 
                                        (f.fault.detail.SifeiException.codigo,f.fault.detail.SifeiException.error, "Error en Cancelación."))
            
                    # try:
                    #     resultado = client.service.cancelaCFDI(user, password, rfc_emisor,
                    #                                    certificate_pfx, file_globals['password'], invoice_rec.cfdi_folio_fiscal)
                    # except WebFault as f:
                    #     raise UserError(_('Advertencia !!!\nOcurrió un error al intentar Cancelar el Timbre. \n\nCódigo: %s\nError: %s\nMensaje: %s') % 
                    #                     (f.fault.detail.SifeiException.codigo,f.fault.detail.SifeiException.error, "Error en Cancelación."))
            
                    # except WebFault as f:
                    #     raise UserError(_('Advertencia !!!\nOcurrió un error al intentar Cancelar el CFDI.'))

                    msg_result = ""
                    instance_class_codes = cancelation_codes.CancelationSFCodes()
                    msg_code = instance_class_codes.return_message_by_code(str(code_result))
                    if code_result == '201':
                        # msg +=  '\n- Cancelación Exitosa.\n- UUID Cancelado es: %s\nMensaje: %s' % (invoice_rec.cfdi_folio_fiscal, msg_code)
                        # status_uuid = msg_code
                        # status = True
                        # rec.state = 'done'
                        # rec.folio_fiscal = invoice_rec.cfdi_folio_fiscal 
                        # rec.message_invisible = str(code_result)+' - '+ msg_code
                        # invoice_rec.mailbox_state = 'done'
                        # invoice_rec.cfdi_state = 'cancel'
                        ### le damos otra revisada al mismo tiempo 
                        consulta_status_sat = rec.solitud_cancelacion_consulta_status()
                        return consulta_status_sat
                    elif code_result == '202':
                        msg +=  '\n- Cancelación Exitosa.\n- UUID Cancelado es: %s\nMensaje: %s' % (invoice_rec.cfdi_folio_fiscal, msg_code)
                        status_uuid = msg_code
                        status = True
                        rec.state = 'done'
                        rec.folio_fiscal = invoice_rec.cfdi_folio_fiscal 
                        rec.message_invisible = str(code_result)+' - '+ msg_code
                        invoice_rec.mailbox_state = 'done'
                        invoice_rec.cfdi_state = 'cancel'
                        ## le damos otra revisada al mismo tiempo 
                    else:
                        msg +=  '\n- Cancelación en Proceso.\n- UUID Cancelado es: %s\nMensaje: %s' % (invoice_rec.cfdi_folio_fiscal, msg_code)
                        status_uuid = msg_code
                        status = True
                        rec.state = 'process'
                        rec.folio_fiscal = invoice_rec.cfdi_folio_fiscal 
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

                    user        = invoice_rec.company_id.pac_testing and invoice_rec.company_id.pac_user_4_testing or invoice_rec.company_id.pac_user
                    password    = invoice_rec.company_id.pac_testing and invoice_rec.company_id.pac_password_4_testing or invoice_rec.company_id.pac_password
                    equipo_id   = invoice_rec.company_id.pac_testing and invoice_rec.company_id.pac_equipo_id_4_testing or invoice_rec.company_id.pac_equipo_id

                    wsdl_url    = self.testing_url if invoice_rec.company_id.pac_testing else self.production_url
                    rfc_emisor  = invoice_rec.company_id.partner_id.vat
                    if 'MX' in rfc_emisor[0:2]:
                        rfc_emisor = rfc_emisor[2:]
                    email_emisor  = invoice_rec.company_id.partner_id.email
                    if not email_emisor:
                        raise UserError("Error!\nLa Compañia no cuenta con una direccion de correo.")
                    rfc_receptor  = invoice_rec.partner_id.vat
                    if 'MX' in rfc_receptor[0:2]:
                        rfc_receptor = rfc_receptor[2:]
                    email_receptor  = invoice_rec.partner_id.email
  
                    fcer = open(file_globals['fname_cer_no_pem'], "rb")
                    fkey = open(file_globals['fname_key_no_pem'], "rb")
                    cerCSD = fcer.read()
                    keyCSD = fkey.read()
                    fcer.close()
                    fkey.close()
                    # fname_pfx = open(file_globals['fname_pfx'], "rb")
                    # certificate_pfx = fname_pfx.read()
                    # fname_pfx.close()
                    certificate_pfx = invoice_rec.journal_id.certificate_pfx_file.decode("utf-8")           
                    contrasenaCSD = invoice_rec.journal_id.certificate_password
                    client = Client(wsdl_url, plugins=[LogPlugin()])
                    isZipFile = 0

                    amount_consult = invoice_rec.amount_total
                    amount_total_split = str(amount_consult).split('.')
                    part_float = self.return_total_in_decimals(amount_total_split[1])
                    part_integer = self.return_total_in_integers(amount_total_split[0])
                    amount_total_to_sat = part_integer+'.'+part_float
                    cfdi_sello = invoice_rec.cfdi_sello
                    cfdi_sello_sat = cfdi_sello[len(cfdi_sello)-8:]
                    code_result = ""
                    msg_code = ""
                    msg_estado = ""
                    CodigoEstatus = ""
                    EsCancelable = ""
                    Estado = ""
                    EstatusCancelacion = ""

                    try:
                        resultado = client.service.consultaSATCFDI(user, password, invoice_rec.cfdi_folio_fiscal,
                                                            rfc_emisor, rfc_receptor, amount_total_to_sat, cfdi_sello_sat)
                        
                        xml_respuesta = parseString(resultado)                        
                        _logger.info("Resultado de la Consulta en el SAT: \n")
                        _logger.info(xml_respuesta)
                        if xml_respuesta.getElementsByTagName('ConsultaResult'):
                            timbre = xml_respuesta.getElementsByTagName('ConsultaResult')[0]
                            if timbre.getElementsByTagName('ns1:CodigoEstatus'):

                                status_sat = timbre.getElementsByTagName('ns1:CodigoEstatus')[0].firstChild
                                sat_consulta_res = status_sat.data
                                if ':' in sat_consulta_res:
                                    sat_consulta_res_split = sat_consulta_res.split(':')
                                else:
                                    sat_consulta_res_split = sat_consulta_res.split('-')
                                code_result = sat_consulta_res_split[0]
                                msg_code = str(sat_consulta_res_split[1])
                                CodigoEstatus = msg_code
                            if timbre.getElementsByTagName('ns1:EsCancelable'):
                                es_cancelable = timbre.getElementsByTagName('ns1:EsCancelable')[0].firstChild
                                if es_cancelable:
                                    EsCancelable = str(es_cancelable.data)
                                    msg_code += " - EsCancelable: "+EsCancelable
                                else:
                                    msg_code += " - EsCancelable: NA"
                            if timbre.getElementsByTagName('ns1:Estado'):
                                stado_sat = timbre.getElementsByTagName('ns1:Estado')[0].firstChild
                                msg_estado = str(stado_sat.data)
                                Estado = msg_estado
                                msg_code += " - Estado: "+Estado
                            if timbre.getElementsByTagName('ns1:EstatusCancelacion'):
                                status_cancelacion = timbre.getElementsByTagName('ns1:EstatusCancelacion')[0].firstChild
                                if status_cancelacion:
                                    try:
                                        EstatusCancelacion = str(status_cancelacion.data)
                                    except:
                                        EstatusCancelacion = ""
                                msg_code += " - EstatusCancelacion: "+EstatusCancelacion
                        _logger.info("\nCodigoEstatus: %s \n" % CodigoEstatus)
                        _logger.info("\nEsCancelable: %s \n" % EsCancelable )
                        _logger.info("\nEstado: %s \n" % Estado)
                        _logger.info("\nEstatusCancelacion: %s \n" % EstatusCancelacion)
                    except WebFault as f:
                        raise UserError(_('Advertencia !!!\nOcurrió un error al intentar Cancelar el Timbre. \n\nCódigo: %s\nError: %s\nMensaje: %s') % 
                                        (f.fault.detail.SifeiException.codigo,f.fault.detail.SifeiException.error, "Error en Cancelación."))
        
                    msg_result = ""
                    _logger.info("\Resultado de msg_estado: %s " % msg_estado)
                    # instance_class_codes = cancelation_codes.CancelationSFCodes()
                    # msg_code = instance_class_codes.return_message_by_code_consulta_sat(str(code_result))
                    if invoice_rec.state == 'cancel':
                        invoice_rec.write({'cfdi_fecha_cancelacion':time.strftime('%Y-%m-%d %H:%M:%S'),
                            #'date_invoice_cancel': time.strftime('%Y-%m-%d %H:%M:%S'),
                            'cfdi_last_message': invoice_rec.cfdi_last_message + "\n-.-.-.-.-.-.-.-.-.-.-.-.-.\n" + \
                                    fields.Datetime.to_string(fields.Datetime.context_timestamp(
                                                                                    self.with_context(tz=(self.env.user.partner_id.tz or 'America/Mexico_City')),
                                                                                    datetime.now())
                                                                                   ) + \
                                                                    ' => ' + str(code_result)+' - '+ msg_code, 
                                })
                    if msg_estado == 'Cancelado':
                        msg +=  '\n- Cancelación Exitosa.\n- UUID Cancelado es: %s\nMensaje: %s' % (invoice_rec.cfdi_folio_fiscal, msg_code)
                        status_uuid = msg_code
                        status = True
                        rec.state = 'done'
                        rec.folio_fiscal = invoice_rec.cfdi_folio_fiscal 
                        rec.message_invisible = str(code_result)+' - '+ msg_code
                        invoice_rec.mailbox_state = 'done'
                        invoice_rec.cfdi_state = 'cancel'
                    elif msg_estado == 'Vigente' and EstatusCancelacion == 'En proceso':
                        msg +=  '\n- Cancelación en Proceso.\n- UUID Cancelado es: %s\nMensaje: %s' % (invoice_rec.cfdi_folio_fiscal, msg_code)
                        status_uuid = msg_code
                        status = True
                        rec.state = 'process'
                        rec.folio_fiscal = invoice_rec.cfdi_folio_fiscal 
                        rec.message_invisible = str(code_result)+' - '+ msg_code
                        invoice_rec.mailbox_state = 'process'
                        invoice_rec.cfdi_state = 'in_process_cancel'
                    elif EstatusCancelacion == 'Plazo vencido':
                        msg +=  '\n- Cancelación Exitosa por Vencimiento de Plazo.\n- UUID Cancelado es: %s\nMensaje: %s' % (invoice_rec.cfdi_folio_fiscal, msg_code)
                        status_uuid = msg_code
                        status = True
                        rec.state = 'done'
                        rec.folio_fiscal = invoice_rec.cfdi_folio_fiscal 
                        rec.message_invisible = str(code_result)+' - '+ msg_code
                        invoice_rec.mailbox_state = 'done'
                        invoice_rec.cfdi_state = 'cancel'
                    elif msg_estado == 'Vigente' and EsCancelable == 'No Cancelable':
                        msg +=  '\n- Cancelación Rechazada.\n- UUID No Cancelable: %s\nMensaje: %s' % (invoice_rec.cfdi_folio_fiscal, msg_code)
                        status_uuid = msg_code
                        status = True
                        rec.state = 'no_cancel'
                        rec.folio_fiscal = invoice_rec.cfdi_folio_fiscal 
                        rec.message_invisible = str(code_result)+' - '+ msg_code
                        invoice_rec.mailbox_state = 'no_cancel'
                        invoice_rec.cfdi_state = 'uuid_no_cancel'
                    else:
                        msg +=  '\n- Cancelación en Proceso.\n- UUID Cancelado es: %s\nMensaje: %s' % (invoice_rec.cfdi_folio_fiscal, msg_code)
                        status_uuid = msg_code
                        status = True
                        rec.state = 'process'
                        rec.folio_fiscal = invoice_rec.cfdi_folio_fiscal 
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

    def return_total_in_decimals(self,decimales):
        index = 6
        if len(decimales) > index:
            decimales_result = decimales[0:6]
            return decimales_result
        if len(decimales) == index:
            return decimales
        i = 6 - len(decimales)
        decimales_result = decimales
        while(i > 0):
            decimales_result += '0'
            i = i -1
        return  decimales_result


    def return_total_in_integers(self,numeric):
        index = 18
        if len(numeric) == index:
            return numeric
        i = 18 - len(numeric)
        numeric_res = numeric
        integer_part = ''
        while(i > 0):
            integer_part += '0'
            i = i -1
        numeric_res = integer_part + numeric_res
        return  numeric_res
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:    