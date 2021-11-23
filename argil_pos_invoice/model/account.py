# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError
from odoo import release
  

class account_journal(models.Model):
    _inherit = 'account.journal'
    """
    Adds check to indicate if Cash Account Journal will not create Account Entries
    """

    pos_dont_create_entries     = fields.Boolean(string="No crear Pólizas de Tickets del POS", 
                                           help="Si marca esta casilla entonces no se van a generar pólizas de\n"+\
                                                "los Ticketsde TPV (en el funcionamiento estándar se genera póliza\n"+\
                                                "contable por cada Ticket de Venta, pero de alguna manera se\n"+\
                                                "duplican las partidas cuando se crean las Facturas.")
    pos_payments_remove_entries = fields.Boolean(string="Eliminar Pagos del POS",
                                            help="Las partidas contables generadas por los pagos de una TPV\n"+\
                                                 "se eliminarán cuando se haga el cierre de Caja")


# class ProductProduct(models.Model):
#     _name = 'product.product'
#     _inherit ='product.product'

#     product_for_global = fields.Boolean('Producto Factura Global')

