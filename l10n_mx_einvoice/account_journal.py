# -*- encoding: utf-8 -*-
from odoo import api, fields, models, _
import base64
import ssl
from OpenSSL import crypto
import logging
_logger = logging.getLogger(__name__)


class account_journal(models.Model):
    _inherit = 'account.journal'

    address_invoice_company_id = fields.Many2one(
        'res.partner', string='Dirección de Emisión', 
        domain="[('type', 'in', ('invoice','default','contact'))]",
        help="Si este campo es capturado, la factura electrónica tomará los datos de la dirección del partner seleccionado para generar el CFDI")

    company2_id = fields.Many2one('res.company', string='Compañía Emisora',
        help="Si este campo es capturado, la factura electrónica tomará los datos de la Compañía seleccionada como Compañía emisora del CFDI")

    use_for_cfdi = fields.Boolean(string="Usar para CFDIs", 
                                  help="Si activa la casilla entonces se podrá usar para generar Factura Electrónica (CFDI)")
    """
    serie_cfdi_invoice = fields.Char(string="Serie Factura", size=12, help="Indique la Serie a utilizar para el CFDI (Opcional)")
    serie_cfdi_refund  = fields.Char(string="Serie Nota de Crédito", size=12, help="Indique la Serie a utilizar para el CFDI (Opcional)")
    
    report_id   = fields.Many2one('ir.actions.report', 'Reporte', 
                                 help="Esta plantilla de reporte se usará para la generación de la representación del PDF del CFDI")
    report_name = fields.Char(string='Nombre Técnico', related='report_id.report_name',  readonly=True)
    """
    certificate_file = fields.Binary(string='Certificado (*.cer)',
                    #filters='*.cer,*.certificate,*.cert', 
                    help='Seleccione el archivo del Certificado de Sello Digital (CSD). Archivo con extensión .cer')
    certificate_key_file = fields.Binary(string='Llave del Certificado (*.key)',
                    #filters='*.key', 
                    help='Seleccione el archivo de la Llave del Certificado de Sello Digital (CSD). Archivo con extensión .key')
    certificate_password = fields.Char(string='Contraseña Certificado', size=64,
                    invisible=False, 
                    help='Especifique la contraseña de su CSD')
    certificate_file_pem = fields.Binary(string='Certificado (PEM)',
                    #filters='*.pem,*.cer,*.certificate,*.cert', 
                    help='Este archivo es generado a partir del CSD (.cer)')
    certificate_key_file_pem = fields.Binary(
        string='Llave del Certificado (PEM)',
        #filters='*.pem,*.key', 
        help='Este archivo es generado a partir del CSD (.key)')
    certificate_pfx_file = fields.Binary(string='Certificado (PFX)',
                     #filters='*.pfx', 
                     help='Este archivo es generado a partir del CSD (.cer)')
    date_start  = fields.Date(string='Vigencia de', help='Fecha de inicio de vigencia del CSD')
    date_end    = fields.Date(string='Vigencia hasta',  help='Fecha de fin de vigencia del CSD')
    serial_number = fields.Char(string='Número de Serie', size=64, 
                                help='Number of serie of the certificate')
    fname_xslt  = fields.Char('Path Parser (.xslt)', size=256, 
                             help='Directorio donde encontrar los archivos XSLT. Dejar vacío para que se usen las opciones por defecto')
    
    bank_acc_number = fields.Char('Número de Cuenta', size=128, store=True)
    bank_id = fields.Many2one('res.bank', 'Banco', store=True)


    @api.onchange('bank_account_id')
    def onchange_cfdi_bank_account_id(self):
        if self.bank_account_id:
            self.bank_acc_number = self.bank_account_id.acc_number
            self.bank_id = self.bank_account_id.bank_id.id
    
    @api.onchange('certificate_password')
    def _onchange_certificate_password(self):
        warning = {}
        certificate_lib = self.env['facturae.certificate.library']
        certificate_file_pem = False
        certificate_key_file_pem = False
        cer_der_b64str  = self.certificate_file  or False
        key_der_b64str  = self.certificate_key_file  or False
        password        = self.certificate_password or False
        self.certificate_file_pem = False
        self.certificate_key_file_pem = False
        self.certificate_pfx_file = False
        #_logger.info("self.use_for_cfdi: %s" % self.use_for_cfdi)
        if cer_der_b64str and key_der_b64str and password:
            cer_pem_b64 = ssl.DER_cert_to_PEM_cert(base64.decodebytes(self.certificate_file)).encode('UTF-8')
            key_pem_b64 = certificate_lib.convert_key_cer_to_pem(base64.decodebytes(self.certificate_key_file),
                                                                str.encode(self.certificate_password))
            if not key_pem_b64:
                key_pem_b64 = certificate_lib.convert_key_cer_to_pem(base64.decodebytes(self.certificate_key_file),
                                                                self.certificate_password+ ' ')
            pfx_pem_b64 = certificate_lib.convert_cer_to_pfx(cer_pem_b64, key_pem_b64,
                                                             str.encode(self.certificate_password))
            cert = crypto.load_certificate(crypto.FILETYPE_PEM, cer_pem_b64)
            x = hex(cert.get_serial_number())
            self.serial_number = x[1::2].replace('x','')
            date_start = cert.get_notBefore().decode("utf-8") 
            date_end = cert.get_notAfter().decode("utf-8") 
            self.date_start = date_start[:4] + '-' + date_start[4:][:2] + '-' + date_start[6:][:2]
            self.date_end = date_end[:4] + '-' + date_end[4:][:2] + '-' + date_end[6:][:2]
            self.certificate_file_pem       = base64.b64encode(cer_pem_b64)
            self.certificate_key_file_pem   = base64.b64encode(key_pem_b64)
            self.certificate_pfx_file       = base64.b64encode(pfx_pem_b64)

        elif self.use_for_cfdi:
                warning = {
                    'title': _('Advertencia!'),
                    'message': _('Falta algún dato, revise que tenga el Certificado, la Llave y la contraseña correspondiente')
                }
        return {'warning': warning}