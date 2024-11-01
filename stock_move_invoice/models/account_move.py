# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2020-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Sayooj A O(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    picking_id = fields.Many2one('stock.picking', string='Albaran')




class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    sale_line_origin_id = fields.Many2one('sale.order.line', string='Linea Origen')

    dev_prod_lot_ids  = fields.Many2many(
        "stock.production.lot",
        "account_move_line_dev_lots_rel",
        "account_move_line_id",
        "lot_id",
        string="Lotes Devoluciones",
    )

    stock_prod_lot_ids  = fields.Many2many(
        "stock.production.lot",
        "account_move_line_sock_lots_rel",
        "account_move_line_id",
        "lot_id",
        string="Lotes Factura Albaran",
    )
