# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    
    def _prepare_invoice_line(self, **optional_values):
        res = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)
        tracking_ids = []
        for move in self.move_ids:
            if move.state != 'done' or move.facturado:
                _logger.info("No tiene movimientos hechos o ya fueron facturados previamente")
                continue
            for link in move.move_line_ids:
                if link.product_id.tracking!='none' and link.lot_id.import_id: # NS o Lote
                    tracking_ids.append(link.lot_id.import_id.id)
                elif link.package_id and link.package_id.import_id:
                    tracking_ids.append(link.package_id.import_id.id)
            move.facturado = True
        if tracking_ids:
            res.update({'import_ids': [(6,0,tracking_ids)]})
        return res