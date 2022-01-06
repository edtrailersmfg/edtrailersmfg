# -*- encoding: utf-8 -*-
#

#from openerp.tools.translate import _
#from openerp.osv import fields, osv


class CancelationSFCodes:

    def return_message_by_code(self, code):
        code_dict = {
            '200':'La solicitud de cancelación se registró exitosamente.',
            '306':'Las llaves utilizadas para sellar no corresponden a un CSD.',
            '308':'El certificado CSD no fue emitido por la Autoridad de SAT.',
            '305':'La fecha de cancelación no está dentro del la vigencia del CSD del emisor.',
            '303':'El certificado CSD no corresponde al RFC del contribuyente.',
            '402':'El RFC del contribuyente no existe conforme al régimen autorizado LCO.',
            '500':'Han ocurrido errores internos que han impedido que se registre la solicitud de cancelación, reintentar.',
            '501':'Ha ocurrido un error interno de comunicación con la base de datos, reintentar.',
            '601':'Error de autenticación, el nombre de usuario o contraseña son incorrectos.',
            '602':'La cuenta de usuario se encuentra bloqueada.',
            '603':'La contraseña de la cuenta ha expirado.',
            '604':'Se ha superado el número máximo permitido de intentos fallidos de autenticación.',
            '605':'El usuario se encuentra inactivo.',
            '611':'Los datos recibidos están incompletos o no se encuentran donde se esperarían.',
            '620':'Permiso denegado.',
            '621':'Los datos recibidos no son válidos.',
            '623': 'El UUID proporcionado no se encuentra en el panel de timbrado del usuario.',
            '633':'Uso indebido de cuenta de producción en pruebas o cuenta de prueba en producción.',
            '701':'Ya existe una transacción asíncrona para el UUID especificado.',
            # Cancelacion 2018 #
            '204':'El comprobante no se puede cancelar',
            '211':'La cancelación está en proceso',
            '213':'La solicitud de cancelación fue rechazada por el receptor',
            '1701' : 'La llave privada y la llave pública del CSD no corresponden.',
            '1702' : 'La llave privada de la contraseña es incorrecta.',
            '1703' : 'La llave privada no cumple con la estructura esperada.',
            '1704' : 'La llave Privada no es una llave RSA.',
            '1710' : 'La estructura del certificado no cumple con la estructura X509 esperada.',
            '1711' : 'El certificado no esá vigente todavía.',
            '1712' : 'El certificado ha expirado.',
            '1713' : 'La llave pública contenida en el certificado no es una llave RSA.',
            '1803' : 'El dato no es un UUID válido.',
        }

        return code_dict[code]

    def return_message_by_code_get_status(self, code):
        code_dict = {
            '200': 'La solicitud de cancelación se registró exitosamente.',
            '500': 'Han ocurrido errores que no han permitido completar el proceso de obtener el estado de la cancelación, reintentar.',
            '501': 'Ha ocurrido un error de conexión a la base de datos de procesamiento asíncrono, reintentar.',
            '601': 'Error de autenticación, el nombre de usuario o contraseña son incorrectos.',
            '602': 'La cuenta de usuario se encuentra bloqueada.',
            '603': 'La contraseña de la cuenta ha expirado.',
            '604': 'Se ha superado el número máximo permitido de intentos fallidos de autenticación.',
            '605': 'El usuario se encuentra inactivo.',
            '611': 'Los datos recibidos están incompletos o no se encuentran donde se esperarían.',
            '620': 'Permiso denegado.',
            '621': 'Los datos recibidos no son válidos de acuerdo a la estructura o tipo de dato esperado.',
            '633': 'Uso indebido de cuenta de producción en pruebas o cuenta de prueba en producción.',
            '702': 'No se encuentra la transacción con el UUID especificado.',
            '1801': 'No se pudo cargar el mensaje de cancelación o no se pudo validar la firma.',
            '1802': 'La firma de la solicitud de cancelación no ha pasado la validación criptográfica.',
            '204': 'El comprobante no se puede cancelar',
            '211': 'La cancelación está en proceso',
            '213': 'La solicitud de cancelación fue rechazada por el receptor',
            '1701' : 'La llave privada y la llave pública del CSD no corresponden.',
            '1702' : 'La llave privada de la contraseña es incorrecta.',
            '1703' : 'La llave privada no cumple con la estructura esperada.',
            '1704' : 'La llave Privada no es una llave RSA.',
            '1710' : 'La estructura del certificado no cumple con la estructura X509 esperada.',
            '1711' : 'El certificado no esá vigente todavía.',
            '1712' : 'El certificado ha expirado.',
            '1713' : 'La llave pública contenida en el certificado no es una llave RSA.',
            '1803' : 'El dato no es un UUID válido.',
        }

        return code_dict[code]
