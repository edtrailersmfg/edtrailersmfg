# -*- encoding: utf-8 -*-
#


class CancelationSFCodes:

    def return_message_by_code(self, code):
        code_dict = {
            '201':'La solicitud de cancelación se registró exitosamente.',
            '202':'Comprobante cancelado previamente.',
            '211':'Comprobante enviado a cancelar exitosamente.',
            '205':'El comprobante aún no se encuentra reportado en el SAT.',
            '402': 'El UUID enviado no tiene un formato correcto.',
            '300': 'Token no es válido',
            '301' : 'Token no registrado para esta empresa',
            '302' : 'Token ha caducado',
        }

        return code_dict[code]

    def return_message_by_code_consulta_sat(self, code):
        code_dict = {
            '201':'La solicitud de cancelación se registró exitosamente.',
            '202':'Comprobante cancelado previamente.',
            '211':'Comprobante enviado a cancelar exitosamente.',
            '205':'El comprobante aún no se encuentra reportado en el SAT.',
            '402': 'El UUID enviado no tiene un formato correcto.',
            '300': 'Token no es válido',
            '301' : 'Token no registrado para esta empresa',
            '302' : 'Token ha caducado',
        }


        return code_dict[code]