# -*- coding: utf-8 -*-

import base64
import logging
import ssl
import subprocess
import tempfile
from datetime import datetime

_logger = logging.getLogger(__name__)

try:
    from OpenSSL import crypto
except ImportError:
    _logger.warning('OpenSSL library not found. If you plan to use l10n_mx_edi, please install the library from https://pypi.python.org/pypi/pyOpenSSL')

from pytz import timezone

from odoo import _, api, fields, models, tools
from odoo.exceptions import ValidationError, UserError
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT

CER_TO_PFX_CMD = 'openssl pkcs12 -export -out %s -inkey %s -in %s -passout pass:%s'
KEY_TO_PEM_CMD = 'openssl pkcs8 -in %s -inform der -outform pem -out %s -passin file:%s'

class Certificate(models.Model):
    _inherit = 'l10n_mx_edi.certificate'
    
    pfx = fields.Binary(
        string='PFX',
        help='Certificate PFX',
        required=False,
        attachment=False,)

    
    def convert_key_cer_to_pem(self, key, password):
        with tempfile.NamedTemporaryFile('wb', suffix='.key', prefix='mx_einvoice.') as key_file, \
             tempfile.NamedTemporaryFile('wb', suffix='.txt', prefix='mx_einvoice.') as pwd_file, \
             tempfile.NamedTemporaryFile('rb', suffix='.key', prefix='mx_einvoice.') as keypem_file:
            key_file.write(key)
            key_file.flush()
            pwd_file.write(password)
            pwd_file.flush()
            subprocess.call((KEY_TO_PEM_CMD % (key_file.name, keypem_file.name, pwd_file.name)).split())
            key_pem = keypem_file.read()
        return key_pem


    def convert_cer_to_pfx(self, cer_pem, key_pem, password):
        ### Corrección de la generación del Archivo PFX el password lo recibe como bytes string allpi radicaba el error - German P.####
        password =  password.decode("utf-8") 
        with tempfile.NamedTemporaryFile('wb', suffix='.cer_pem', prefix='mx_einvoice.') as cer_pem_file, \
             tempfile.NamedTemporaryFile('wb', suffix='.key_pem', prefix='mx_einvoice.') as key_pem_file, \
             tempfile.NamedTemporaryFile('rb', suffix='.pfx', prefix='mx_einvoice.') as pfx_file:
            cer_pem_file.write(cer_pem)
            cer_pem_file.flush()
            key_pem_file.write(key_pem)
            key_pem_file.flush()
            ##print(CER_TO_PFX_CMD % (pfx_file.name, 
            #                                   key_pem_file.name, 
            #                                   cer_pem_file.name, 
            #                                   password))
            subprocess.call((CER_TO_PFX_CMD % (pfx_file.name, 
                                               key_pem_file.name, 
                                               cer_pem_file.name, 
                                               password)).split())
            pfx_pem = pfx_file.read()
        return pfx_pem    
    
    
    
    @api.constrains('content', 'key', 'password')
    def _check_credentials(self):
        super(Certificate, self)._check_credentials()
        for record in self:
            cer_pem_b64 = ssl.DER_cert_to_PEM_cert(base64.decodebytes(record.content)).encode('UTF-8')
            key_pem_b64 = record.convert_key_cer_to_pem(base64.decodebytes(record.key),
                                                        str.encode(record.password))
            if not key_pem_b64:
                key_pem_b64 = record.convert_key_cer_to_pem(base64.decodebytes(record.key),
                                                            record.password+ ' ')
            pfx_pem_b64 = record.convert_cer_to_pfx(cer_pem_b64, key_pem_b64,
                                                    str.encode(record.password))
            
            self.pfx = base64.b64encode(pfx_pem_b64)
    