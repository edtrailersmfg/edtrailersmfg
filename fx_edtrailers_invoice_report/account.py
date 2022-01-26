# -*- coding: utf-8 -*-
# Coded by German Ponce Dominguez 
#     ▬▬▬▬▬.◙.▬▬▬▬▬  
#       ▂▄▄▓▄▄▂  
#    ◢◤█▀▀████▄▄▄▄▄▄ ◢◤  
#    █▄ █ █▄ ███▀▀▀▀▀▀▀ ╬  
#    ◥ █████ ◤  
#     ══╩══╩═  
#       ╬═╬  
#       ╬═╬ Dream big and start with something small!!!  
#       ╬═╬  
#       ╬═╬ You can do it!  
#       ╬═╬   Let's go...
#    ☻/ ╬═╬   
#   /▌  ╬═╬   
#   / \
# Cherman Seingalt - german.ponce@outlook.com

from odoo import api, fields, models, _, tools, SUPERUSER_ID
from odoo.tools import float_repr, format_datetime
from odoo.tools.misc import get_lang
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta

import logging
_logger = logging.getLogger(__name__)



class AccountMoveLine(models.Model):
    _name = 'account.move.line'
    _inherit ='account.move.line'


    def get_info_previous_sections(self):
        _logger.info("\n############# get_info_previous_sections >>>>>>>>>>>> ")
        invoice_id = self.move_id
        adicional_info_dict = {

                              }
        adicional_info = ""
        previous_line = False
        for invoice_line in invoice_id.invoice_line_ids:
            if invoice_line.product_id:
                previous_line = invoice_line
            if invoice_line.id == self.id:
                break
        _logger.info("\n############# previous_line: %s " % previous_line)
        if previous_line:
            #if 'SERIE' in self.name:
            arancel = previous_line.product_id.sat_arancel_id.name if previous_line.product_id.sat_arancel_id else ''
            udm_sat = previous_line.product_uom_id.sat_uom_id.code if previous_line.product_uom_id.sat_uom_id else ''
            quantity = previous_line.quantity
            price_unit = str(previous_line.price_unit)+" "+invoice_id.currency_id.name
            price_subtotal = str(previous_line.price_subtotal)+" "+invoice_id.currency_id.name
            adicional_info = "Fracción arancelaria: %s  Unidad aduana: %s Cantidad Aduana: %s Valor unitario aduana:%s  Valor:%s" % ( arancel,
                                                                                                                                      udm_sat,
                                                                                                                                      quantity,
                                                                                                                                      price_unit,
                                                                                                                                      price_subtotal)
        
            adicional_info_dict = {
                                    'arancel': arancel,
                                    'udm_sat': udm_sat,
                                    'quantity': quantity,
                                    'price_unit': price_unit,
                                    'price_subtotal': price_subtotal,
                                  }
        _logger.info("\n############# adicional_info: %s " % adicional_info)
        return adicional_info_dict