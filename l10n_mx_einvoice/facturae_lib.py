# -*- encoding: utf-8 -*-
#

from odoo import _, api, fields, models, tools

import os
import sys
import time
import tempfile
import base64
import binascii
import logging
_logger = logging.getLogger(__name__)

### Python Sello ####

from base64 import b64encode
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

## Prueba 2
import base64
from lxml import etree
from lxml.objectify import fromstring
from OpenSSL import crypto
import hashlib
import os
import subprocess
#from Crypto.PublicKey import RSA
#from Crypto.Signature import PKCS1_v1_5
#from Crypto.Hash import SHA256
### Fin Sello ####

import ssl


KEY_TO_PEM_CMD = 'openssl pkcs8 -in %s -inform der -outform pem -out %s -passin file:%s'
CER_TO_PFX_CMD = 'openssl pkcs12 -export -out %s -inkey %s -in %s -passout pass:%s'
  
        
# def exec_command_pipe(*args):
#     # Agregue esta funcion, ya que con la nueva funcion original, de tools no funciona
# # TODO: Hacer separacion de argumentos, no por espacio, sino tambien por "
# # ", como tipo csv, pero separator espace & delimiter "
#     cmd = ' '.join(args)
#     if os.name == "nt":
#         cmd = cmd.replace(
#             '"', '')  # provisionalmente, porque no funcionaba en win32
#     res = subprocess.getstatusoutput(cmd)
#     return res


# openssl_path = ''
# xsltproc_path = ''
# xmllint_path = ''
# all_paths = tools.config["addons_path"].split(",")
# for my_path in all_paths:
#     if os.path.isdir(os.path.join(my_path, 'l10n_mx_einvoice', 'depends_app')):
#         openssl_path = my_path and os.path.join(my_path, 'l10n_mx_einvoice', 'depends_app', u'openssl_win') or ''
#         xsltproc_path = my_path and os.path.join(my_path, 'l10n_mx_einvoice', 'depends_app', u'xsltproc_win') or ''
#         xmllint_path = my_path and os.path.join(my_path, 'l10n_mx_einvoice', 'depends_app', u'xmllint_win') or ''
        

# if os.name == "nt":
#     app_xsltproc = 'xsltproc.exe'
#     app_openssl = 'openssl.exe'
#     app_xmllint = 'xmllint.exe'
# else:
#     app_xsltproc = 'xsltproc'
#     app_openssl = 'openssl'
#     app_xmllint = 'xmllint'

# app_openssl_fullpath = os.path.join(openssl_path, app_openssl)
# if not os.path.isfile(app_openssl_fullpath):
#     app_openssl_fullpath = tools.find_in_path(app_openssl)
#     if not os.path.isfile(app_openssl_fullpath):
#         app_openssl_fullpath = False
#         _logger.warning('Install openssl "sudo apt-get install openssl" to use l10n_mx_einvoice module.')

# app_xsltproc_fullpath = os.path.join(xsltproc_path, app_xsltproc) or False
# try:
#     if not os.path.isfile(app_xsltproc_fullpath):
#         app_xsltproc_fullpath = tools.find_in_path(app_xsltproc) or False
#         if not os.path.isfile(app_xsltproc_fullpath):
#             app_xsltproc_fullpath = False
#             _logger.warning('Install xsltproc "sudo apt-get install xsltproc" to use l10n_mx_einvoice module.')
# except:
#     _logger.warning("Install xsltproc 'sudo apt-get install xsltproc' to use l10n_mx_einvoice module.")

# app_xmllint_fullpath = os.path.join(xmllint_path, app_xmllint)
# if not os.path.isfile( app_xmllint_fullpath ):
#     app_xmllint_fullpath = tools.find_in_path( app_xmllint )
#     if not app_xmllint_fullpath:
#         app_xmllint_fullpath = False
#         _logger.warning('Install xmllint "sudo apt-get install xmllint" to use l10n_mx_einvoice module.')

# def library_openssl_xsltproc_xmllint():
#     msj = ''
#     app_openssl_fullpath = os.path.join(openssl_path, app_openssl)
#     if not os.path.isfile(app_openssl_fullpath):
#         app_openssl_fullpath = tools.find_in_path(app_openssl)
#         if not os.path.isfile(app_openssl_fullpath):
#             app_openssl_fullpath = False
#             _logger.warning('Install openssl "sudo apt-get install openssl" to use l10n_mx_einvoice module.')
#             msj += 'Install openssl "sudo apt-get install openssl" to use l10n_mx_einvoice module.'
    
#     app_xsltproc_fullpath = os.path.join(xsltproc_path, app_xsltproc) or False
#     if not os.path.isfile(app_xsltproc_fullpath):
#         app_xsltproc_fullpath = tools.find_in_path(app_xsltproc) or False
#         try:
#             if not os.path.isfile(app_xsltproc_fullpath):
#                 app_xsltproc_fullpath = False
#                 _logger.warning("Install xsltproc 'sudo apt-get install xsltproc' to use l10n_mx_einvoice module.")
#                 msj =  "Install xsltproc 'sudo apt-get install xsltproc' to use l10n_mx_einvoice module."
#         except:
#             _logger.warning("Install xsltproc 'sudo apt-get install xsltproc' to use l10n_mx_einvoice module.")
#             msj +=  "Install xsltproc 'sudo apt-get install xsltproc' to use l10n_mx_einvoice module."

#     app_xmllint_fullpath = os.path.join(xmllint_path, app_xmllint)
#     if not os.path.isfile( app_xmllint_fullpath ):
#         app_xmllint_fullpath = tools.find_in_path( app_xmllint )
#         if not app_xmllint_fullpath:
#             app_xmllint_fullpath = False
#             _logger.warning('Install xmllint "sudo apt-get install xmllint" to use l10n_mx_einvoice module.')
#             msj += 'Install xmllint "sudo apt-get install xmllint" to use l10n_mx_einvoice module.'
#     return msj, app_xsltproc_fullpath, app_openssl_fullpath, app_xmllint_fullpath
        

class facturae_certificate_library(models.Model):
    _name = 'facturae.certificate.library'
    _description = "Libreria para el manejo de CFDI"
    
    name = fields.Char('Dummy')
    # Agregar find subpath

    def convert_key_cer_to_pem(self, key, password):
        with tempfile.NamedTemporaryFile('wb', suffix='.key', prefix='mx_einvoice.') as key_file, \
             tempfile.NamedTemporaryFile('wb', suffix='.txt', prefix='mx_einvoice.') as pwd_file, \
             tempfile.NamedTemporaryFile('rb', suffix='.key', prefix='mx_einvoice.') as keypem_file:
            key_file.write(key)
            key_file.flush()
            _logger.info("type(password): %s - %s " % (password, type(password)))
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
    
    
    
    
    def b64str_to_tempfile(self, b64_str=None, file_suffix=None, file_prefix=None):
        """
        @param b64_str : Text in Base_64 format for add in the file
        @param file_suffix : Sufix of the file
        @param file_prefix : Name of file in TempFile
        """
        (fileno, fname) = tempfile.mkstemp(file_suffix, file_prefix)
        f = open(fname, 'wb')
        f.write(base64.decodebytes(b64_str or str.encode('')))
        f.close()
        os.close(fileno)
        return fname

    def _read_file_attempts(self, file_obj, max_attempt=12, seconds_delay=0.5):
        """
        @param file_obj : Object with the path of the file, more el mode
            of the file to create (read, write, etc)
        @param max_attempt : Max number of attempt
        @param seconds_delay : Seconds valid of delay
        """
        fdata = False
        cont = 1
        while True:
            time.sleep(seconds_delay)
            try:
                fdata = file_obj.read()
            except:
                pass
            if fdata or max_attempt < cont:
                break
            cont += 1
        return fdata

    def _transform_der_to_pem(self, fname_der, fname_out, fname_password_der=None, type_der='cer'):
        """
        @param fname_der : File.cer configurated in the company
        @param fname_out : Information encrypted in Base_64from certificate
            that is send
        @param fname_password_der : File that contain the password configurated
            in this Certificate
        @param type_der : cer or key
        """
        if not app_openssl_fullpath:
            raise UserError(_("Error!"), _(
                "Failed to find in path '%s' app. This app is required for sign Mexican Electronic Invoice"%(app_openssl) ))
        cmd = ''
        result = ''
        if type_der == 'cer':
            cmd = '"%s" x509 -inform DER -outform PEM -in "%s" -pubkey -out "%s"' % (
                app_openssl_fullpath, fname_der, fname_out)
        elif type_der == 'key':
            cmd = '"%s" pkcs8 -inform DER -outform PEM -in "%s" -passin file:%s -out "%s"' % (
                app_openssl_fullpath, fname_der, fname_password_der, fname_out)
        if cmd:
            args = tuple(cmd.split(' '))
            input, output = exec_command_pipe(*args)
            result = self._read_file_attempts(open(fname_out, "r"))
            try:
                input.close()
                output.close()
            except:
                pass
        return result

    
    def _transform_pem_to_pfx(self, fname_cer_pem, fname_key_pem, fname_out, pfx_password):
        """
        @param fname_cer_pem : File.cer.pem configurated in the company
        @param fname_key_pem : File.key.pem configurated in the company
        @param fname_out : PFX file
        @param fname_password_der : File that contain the password configurated
            in this Certificate
        @param type_der : cer or key
        """
        if not app_openssl_fullpath:
            raise UserError(_("Error!"), _(
                "Failed to find in path '%s' app. This app is required for sign Mexican Electronic Invoice"%(app_openssl) ))
        cmd = ''
        result = ''
        cmd = '%s pkcs12 -export -out %s -inkey %s -in %s -passout pass:%s' % (
                app_openssl_fullpath, fname_out, fname_key_pem, fname_cer_pem, str.decode(pfx_password))
        #cms = 'openssl pkcs12 -export -out archivopfx.pfx -inkey llave.pem -in certificado.pem -passout pass:clavedesalida'
        #cmd = '"%s" x509 -inform DER -outform PEM -in "%s" -pubkey -out "%s"' % (
        #    app_openssl_fullpath, fname_der, fname_out)

        if cmd:
            args = tuple(cmd.split(' '))
            # input, output = tools.exec_command_pipe(*args)
            input, output = exec_command_pipe(*args)
            result = self._read_file_attempts(open(fname_out, "r"))
            input.close()
            output.close()
        return result    
    
    
    # def _get_param_serial(self, fname, fname_out=None, type='DER'):
    #     """
    #     @param fname : File.PEM with the information of the certificate
    #     @param fname_out : File.xml that is send
    #     """
    #     result = self._get_params(fname, params=['serial'], fname_out=fname_out, type=type)
    #     result = result and result.replace('serial=', '').replace(
    #         '33', 'B').replace('3', '').replace('B', '3').replace(
    #         ' ', '').replace('\r', '').replace('\n', '').replace('\r\n', '') or ''
    #     return result

    def _transform_xml(self, fname_xml, fname_xslt, fname_out):
        context = self._context.copy() or {}
        cfdi_file = open(fname_xml, 'r')
        cfdi_str = cfdi_file.read()
        cfdi = str.encode(cfdi_str)
        cfdi_xml = fromstring(cfdi)
        xslt_root = etree.parse(tools.file_open(fname_xslt))
        cadena_original = str(etree.XSLT(xslt_root)(cfdi_xml))
        #print("cadena_original: %s - \n cadena_original type: %s" % (cadena_original, type(cadena_original)))
        return cadena_original
        """
        numero_certificado = context['serial_number']
        archivo_cer = context['fname_cer_no_pem']
        archivo_pem = context['fname_key']
        #cadena_original = context['cadena_original']
        keys = RSA.load_key(archivo_pem)
        cert_file = open(archivo_cer, 'r')
        cert = base64.b64encode(cert_file.read())
        
        xdoc = etree.fromstring(cfdi)
        comp = xdoc.get('Comprobante')
        xdoc.attrib['Certificado'] = cert
        xdoc.attrib['NoCertificado'] = numero_certificado
        fname_xslt = context['fname_xslt']
        xsl_root = etree.parse(fname_xslt)
        xsl = etree.XSLT(xsl_root)
        result = xsl(xdoc)
        return result
        """
        
    # def _get_param_dates(self, fname, fname_out=None, date_fmt_return='%Y-%m-%d %H:%M:%S', type='DER'):
    #     """
    #     @param fname : File.cer with the information of the certificate
    #     @params fname_out : Path and name of the file.txt with info encrypted
    #     @param date_fmt_return : Format of the date used
    #     @param type : Type of file
    #     """
    #     months = {'Jan':'01',
    #               'Feb':'02',
    #               'Mar':'03',
    #               'Apr':'04',
    #               'May':'05',
    #               'Jun':'06',
    #               'Jul':'07', 
    #               'Aug':'08',
    #               'Sep':'09',
    #               'Oct':'10',
    #               'Nov':'11',
    #               'Dec':'12'}
    #     result_dict = self._get_params_dict(fname, params=['dates'], fname_out=fname_out, type=type)
    #     translate_key = {
    #         'notAfter': 'enddate',
    #         'notBefore': 'startdate',
    #     }
    #     result2 = {}
    #     if result_dict:
    #         date_fmt_src = "%b %d %H:%M:%S %Y GMT"
    #         for key in result_dict.keys():
    #             date = result_dict[key]
    #             dia = (date[:6][-2:]).replace(' ', '0')
    #             new_date = date[:-4][-4:] + '-' + months[date[:3]] + '-' + dia #date[:6][-2:]
    #             result2[translate_key[key]] = new_date
    #     return result2

    # def _get_params_dict(self, fname, params=None, fname_out=None, type='DER'):
    #     """
    #     @param fname : File.cer with the information of the certificate
    #     @param params : List of params used for this function
    #     @param fname_out : Path and name of the file.txt with info encrypted
    #     @param type : Type of file
    #     """
    #     result = self._get_params(fname, params, fname_out, type)
    #     result = result.replace('\r\n', '\n').replace('\r', '\n')
    #     result = result.rstrip('\n').lstrip('\n').rstrip(' ').lstrip(' ')
    #     result_list = result.split('\n')
    #     params_dict = {}
    #     for result_item in result_list:
    #         if result_item:
    #             key, value = result_item.split('=')
    #             params_dict[key] = value
    #     return params_dict

    # def _get_params(self, fname, params=None, fname_out=None, type='DER'):
    #     """
    #     @params: list [noout serial startdate enddate subject issuer dates]
    #     @type: str DER or PEM
    #     """
    #     msj, app_xsltproc_fullpath, app_openssl_fullpath, app_xmllint_fullpath = library_openssl_xsltproc_xmllint()
    #     if not app_openssl_fullpath:
    #         raise UserError(_("Error!"), _(
    #             "Failed to find in path '%s' app. This app is required for sign Mexican Electronic Invoice"%(app_openssl) ))
    #     cmd_params = ' -'.join(params)
    #     cmd_params = cmd_params and '-' + cmd_params or ''
    #     cmd = '"%s" x509 -inform "%s" -in "%s" -noout "%s" -out "%s"' % (
    #         app_openssl_fullpath, type, fname, cmd_params, fname_out)
    #     args = tuple(cmd.split(' '))
    #     # input, output = tools.exec_command_pipe(*args)
    #     input, output = exec_command_pipe(*args)
    #     result = self._read_file_attempts(output)
    #     try:
    #         input.close()
    #     except:
    #         pass
    #     try:
    #         output.close()
    #     except:
    #         pass
    #     return result

    """
    def _sign_sello(self, cadena):
        key_pem = self.get_pem_key(self.key, self.password)
        private_key = crypto.load_privatekey(crypto.FILetreeYPE_PEM, key_pem)
        version = cadena.split('|')[2]
        encrypt = 'sha256WithRSAEncryption' if version == '3.3' else 'sha1'
        cadena_crypted = crypto.sign(private_key, cadena, encrypt)
        return base64.b64encode(cadena_crypted)    
    """
    
    
    def _sign_sello(self):
        context = self._context.copy() or {}
        
        xslt_root = etree.parse(tools.file_open(context['fname_xslt']))
        cfdi_as_tree = fromstring(context['xml_prev'])
        cadena_original = str(etree.XSLT(xslt_root)(cfdi_as_tree))
        
        file_pem = open(context['fname_key'],'r')
        key = RSA.importKey(file_pem.read())
        digest = SHA256.new()
        digest.update(cadena_original.encode('UTF-8'))
        signer = PKCS1_v1_5.new(key)
        sign = signer.sign(digest)
        return base64.b64encode(sign)


    # def _sign(self, fname, fname_xslt, fname_key, fname_out, encrypt='sha256', type_key='PEM'):
    #     """
    #      @params fname : Path and name of the XML of Facturae
    #      @params fname_xslt : Path where is located the file 'Cadena Original'.xslt
    #      @params fname_key : Path and name of the file.pem with data of the key
    #      @params fname_out : Path and name of the file.txt with info encrypted
    #      @params encrypt : Type of encryptation for file
    #      @params type_key : Type of KEY
    #     """
    #     msj, app_xsltproc_fullpath, app_openssl_fullpath, app_xmllint_fullpath = \
    #                 library_openssl_xsltproc_xmllint()
    #     result = ""
    #     cmd = ''
    #     if type_key == 'PEM':
    #         if not app_xsltproc_fullpath:
    #             raise UserError(_("Error!\nFailed to find in path '%s' app. This app is required for sign Mexican Electronic Invoice"%(app_xsltproc) ))
    #         cmd = '"%s" "%s" "%s" | "%s" dgst -%s -sign "%s" | "%s" enc -base64 -A -out "%s"' % (
    #             app_xsltproc_fullpath, fname_xslt, fname, app_openssl_fullpath,
    #                 encrypt, fname_key, app_openssl_fullpath, fname_out)

    #     elif type_key == 'DER':
    #         # TODO: Dev for type certificate DER
    #         pass
    #     if cmd:
    #         input, output = exec_command_pipe(cmd)
    #         #### Revisar este Timesleep
    #         time.sleep(5)
    #         ####
    #         result = self._read_file_attempts(open(fname_out, "r"))
    #         input.close()
    #         output.close()
    #     return result

    # def check_xml_scheme(self, fname_xml, fname_scheme, fname_out, type_scheme="xsd"):
    #     #xmllint val -e --xsd cfdv2.xsd cfd_example.xml
    #     msj, app_xsltproc_fullpath, app_openssl_fullpath, app_xmllint_fullpath = library_openssl_xsltproc_xmllint()
    #     if app_xmllint_fullpath:

    #         cmd = ''
    #         if type_scheme == 'xsd':
    #             cmd = '"%s" --noout --schema "%s" "%s" 1>"%s" 2>"%s"'%(app_xmllint_fullpath, fname_scheme, fname_xml, fname_out+"1", fname_out)
    #             #cmd = '"%s" val -e --%s "%s" "%s" 1>"%s" 2>"%s"'%(app_xmllint_fullpath, type_scheme, fname_scheme, fname_xml, fname_out+"1", fname_out)
    #         if cmd:
    #             args = tuple( cmd.split(' ') )
    #             input, output = exec_command_pipe(*args)
    #             result = self._read_file_attempts( open(fname_out, "r") )
    #             if "valid" in result and "error" not in result:
    #                 result =""
    #             try:
    #                 input.close()
    #             except:
    #                 pass
    #             try:
    #                 output.close()
    #             except:
    #                 pass
    #     else:
    #         _logger.warning("Failed to find in path 'xmllint' app. Can't validate xml structure. You should make a manual check to xml file.")
    #         result = ""
    #     return result

    # Funciones en desuso
    def binary2file(self, binary_data=False, file_prefix="", file_suffix=""):
        """
        @param binary_data : Field binary with the information of certificate
            of the company
        @param file_prefix : Name to be used for create the file with the
            information of certificate
        @file_suffix : Sufix to be used for the file that create in this function
        """
        (fileno, fname) = tempfile.mkstemp(file_suffix, file_prefix)
        f = open(fname, 'wb')
        f.write(base64.decodebytes(binary_data))
        f.close()
        os.close(fileno)
        return fname

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
