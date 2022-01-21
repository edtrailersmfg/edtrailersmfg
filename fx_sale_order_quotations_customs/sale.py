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

class WizardOrderRecompute(models.TransientModel):
    _name = 'wizard.order.recompute'
    _description = 'Asistente Calculo Avanzado Precio Cotizacion'

    @api.model  
    def default_get(self, fields):
        res = super(WizardOrderRecompute, self).default_get(fields)
        ctx = self._context
        active_ids = ctx.get('active_ids',False)
        sale_order = self.env['sale.order']
        sale_order_br = sale_order.browse(active_ids)[0]
        if sale_order_br.pricelist_id and sale_order_br.pricelist_id.currency_id:
            order_currency_id = sale_order_br.pricelist_id.currency_id.id
        else:
            order_currency_id = self.env.user.company_id.currency_id.id
        sale_order_name = sale_order_br.name+" "+sale_order_br.partner_id.name
        res.update(
                   sale_order_name=sale_order_name,
                   amount_total=sale_order_br.amount_total,
                   total_sale_order=sale_order_br.amount_total,
                   sale_order_id=sale_order_br.id,
                   currency_id=order_currency_id)
        return res

    sale_order_name = fields.Char('Referencia Cotización')

    sale_order_id = fields.Many2one('sale.order', 'Cotización')

    total_sale_order = fields.Monetary(
        'Total Original', default=0, digits=(16, 4),
        help="Total Original")

    currency_id = fields.Many2one('res.currency', 'Moneda')

    amount_total = fields.Monetary(
        'Total', default=0, digits=(16, 4),
        help="Total")

    amount_total_prev = fields.Monetary(
        'Total Previo', default=0, digits=(16, 4),
        help="Total Previo")

    order_updated = fields.Boolean('Orden Actualizada')

    price_surcharge = fields.Monetary(
        'Tarifa extra', digits='Product Price',
        help='Monto extra')

    price_surcharge_percentage = fields.Float(
        'Tarifa extra', digits='Product Price',
        help='Porcentaje Monto extra sobre el Total.')

    discount_amount = fields.Monetary(
        'Descuento', default=0, digits=(16, 2),
        help="Monto Descuento")

    discount_percent = fields.Float(
        'Descuento %', default=0, digits=(16, 2),
        help="Monto Descuento en Porcentaje")

    def compute_value(self):
        ctx = self._context
        active_ids = ctx.get('active_ids',False)

        if self.price_surcharge_percentage > 100:
            raise UserError("El porcentaje Maximo de Tarifa Extra es 100%")
        if self.discount_percent > 100:
            raise UserError("El porcentaje Maximo de Descuento es 100%")
        if not self.sale_order_id.order_line:
            raise UserError("No existe información en las Lineas de Cotización.")
        ########################## CHERMAN ############################
        final_advanced_price = 0.0

        base_amount = self.sale_order_id.amount_total
        discount_factor = (100 - self.discount_percent) / 100 
        surcharge = tools.format_amount(self.env, self.price_surcharge, self.currency_id)
        
        discount_amount = self.discount_amount

        price_surcharge_1_total =  self.price_surcharge
        if self.price_surcharge_percentage:
            price_surcharge_1_result =  base_amount * (self.price_surcharge_percentage/100)
            price_surcharge_1_total = price_surcharge_1_total + price_surcharge_1_result
        final_advanced_price = (( base_amount + price_surcharge_1_total) * discount_factor) - discount_amount
        # base_amount_surcharges = base_amount + price_surcharge_1_total
        # final_advanced_price = base_amount_surcharges * discount_factor 

        ########################## FIN ############################

        ########################## ESCRIBIMOS EL RESULTADO ############################
        self.amount_total_prev = self.amount_total
        self.amount_total = final_advanced_price
        self.order_updated = True
        return {
            "name": _("Calculo Cotización"),
            "view_mode": "form",
            "view_id": False,
            "view_type": "form",
            "res_id": self.id,
            "res_model": "wizard.order.recompute",
            "type": "ir.actions.act_window",
            "nodestroy": True,
            "target": "new",
            "context": ctx,
        }

    def compute_and_back(self):
        ctx = self._context
        active_ids = ctx.get('active_ids',False)
        if self.sale_order_id.state != 'draft':
            raise UserError("No se puede actualizar el total si el registro no es una Cotización (Borrador).")
        if not self.sale_order_id.order_line:
            raise UserError("No existe información en las Lineas de Cotización.")
        if self.amount_total != self.total_sale_order:
            difference_amount = self.total_sale_order - self.amount_total
            _logger.info("\n##### difference_amount: %s ", difference_amount)
            if difference_amount > 0.0:
                _logger.info("\n##### descuento positivo - disminuye precio >>>>>>> ")
                new_total_to_limit = self.total_sale_order - difference_amount
                _logger.info("\n##### new_total_to_limit: %s ", new_total_to_limit)
                percentage_global = 1-(new_total_to_limit/self.total_sale_order)
                _logger.info("\n##### percentage_global: %s ", percentage_global)
                if percentage_global:
                    for line in self.sale_order_id.order_line:
                        original_line_price = line.price_unit
                        new_line_price = original_line_price - (original_line_price * percentage_global)
                        line.write({'price_unit': new_line_price})
                ### Calculo Global ###
                # 100*(1-(11000/16378.39)) # Nos da el porcentaje de aumento
                # 1-(Nuevo Total/Total Orden) # Nos da el porcentaje de aumento
                ### Calculo Linea ###
                # 1180-(1180 * 0.38943937713047494)
                # Precio Linea-(Precio Linea * Representación Descuento)
            else:
                _logger.info("\n##### descuento negativo - aumenta precio >>>>>>> ")
                new_total_to_limit = self.total_sale_order + abs(difference_amount)
                _logger.info("\n##### new_total_to_limit: %s ", new_total_to_limit)
                percentage_global = abs(difference_amount) / self.total_sale_order
                _logger.info("\n##### percentage_global: %s ", percentage_global)
                if percentage_global:
                    for line in self.sale_order_id.order_line:
                        original_line_price = line.price_unit
                        new_line_price = original_line_price + (original_line_price * percentage_global)
                        line.write({'price_unit': new_line_price})
        # raise UserError("AQUI >>>> ")
        return {'type': 'ir.actions.act_window_close'}

    def update_prices(self):
        ctx = self._context
        active_ids = ctx.get('active_ids',False)
        if self.sale_order_id.state != 'draft':
            raise UserError("No se puede actualizar el total si el registro no es una Cotización (Borrador).")
        if not self.sale_order_id.order_line:
            raise UserError("No existe información en las Lineas de Cotización.")
        self.sale_order_id.update_prices()
        return {'type': 'ir.actions.act_window_close'}

class WizardOrderLineRecompute(models.TransientModel):
    _name = 'wizard.order.line.recompute'
    _description = 'Asistente Calculo Avanzado Precio Linea'

    @api.model  
    def default_get(self, fields):
        res = super(WizardOrderLineRecompute, self).default_get(fields)
        ctx = self._context
        active_ids = ctx.get('active_ids',False)
        sale_order_line = self.env['sale.order.line']
        sale_order_line_br = sale_order_line.browse(active_ids)[0]
        if sale_order_line_br.order_id.pricelist_id and sale_order_line_br.order_id.pricelist_id.currency_id:
            order_currency_id = sale_order_line_br.order_id.pricelist_id.currency_id.id
        else:
            order_currency_id = self.env.user.company_id.currency_id.id
        res.update(product_id=sale_order_line_br.product_id.id,
                   price_unit=sale_order_line_br.price_unit,
                   price_sale_order=sale_order_line_br.price_unit,
                   sale_order_line_id=sale_order_line_br.id,
                   currency_id=order_currency_id)
        return res

    sale_order_line_id = fields.Many2one('sale.order.line', 'Linea Presupuesto')

    price_sale_order = fields.Monetary(
        'Precio Original', default=0, digits=(16, 4),
        help="Precio Original")

    product_id = fields.Many2one('product.product', 'Producto')

    currency_id = fields.Many2one('res.currency', 'Moneda')

    price_unit = fields.Monetary(
        'Precio Unitario', default=0, digits=(16, 4),
        help="Precio Unitario")

    price_unit_prev = fields.Monetary(
        'Precio Previo', default=0, digits=(16, 4),
        help="Precio Previo")

    price_updated = fields.Boolean('Precio Actualizado')

    price_surcharge = fields.Monetary(
        'Tarifa extra', digits='Product Price',
        help='Monto extra')

    price_surcharge_percentage = fields.Float(
        'Tarifa extra', digits='Product Price',
        help='Porcentaje Monto extra sobre el subtotal.')

    discount_amount = fields.Monetary(
        'Descuento', default=0, digits=(16, 2),
        help="Monto Descuento")

    discount_percent = fields.Float(
        'Descuento %', default=0, digits=(16, 2),
        help="Monto Descuento en Porcentaje")

    def compute_value(self):
        ctx = self._context
        active_ids = ctx.get('active_ids',False)

        if self.price_surcharge_percentage > 100:
            raise UserError("El porcentaje Maximo de Tarifa Extra es 100%")
        if self.discount_percent > 100:
            raise UserError("El porcentaje Maximo de Descuento es 100%")
        ########################## CHERMAN ############################
        final_advanced_price = 0.0

        base_amount = self.sale_order_line_id.price_unit
        discount_factor = (100 - self.discount_percent) / 100 
        surcharge = tools.format_amount(self.env, self.price_surcharge, self.currency_id)
        
        discount_amount = self.discount_amount

        price_surcharge_1_total =  self.price_surcharge
        if self.price_surcharge_percentage:
            price_surcharge_1_result =  base_amount * (self.price_surcharge_percentage/100)
            price_surcharge_1_total = price_surcharge_1_total + price_surcharge_1_result

        final_advanced_price = (( base_amount + price_surcharge_1_total) * discount_factor) - discount_amount
        # base_amount_surcharges = base_amount + price_surcharge_1_total
        # final_advanced_price = base_amount_surcharges * discount_factor 

        ########################## FIN ############################

        ########################## ESCRIBIMOS EL RESULTADO ############################
        self.price_unit_prev = self.price_unit
        self.price_unit = final_advanced_price
        self.price_updated = True
        return {
            "name": _("Calculo Precio"),
            "view_mode": "form",
            "view_id": False,
            "view_type": "form",
            "res_id": self.id,
            "res_model": "wizard.order.line.recompute",
            "type": "ir.actions.act_window",
            "nodestroy": True,
            "target": "new",
            "context": ctx,
        }

    def compute_and_back(self):
        ctx = self._context
        active_ids = ctx.get('active_ids',False)
        if self.sale_order_line_id.state != 'draft':
            raise UserError("No se puede actualizar el precio si el registro no es una Cotización (Borrador).")
        if self.price_unit != self.price_sale_order:
            self.sale_order_line_id.write({
                                        'price_unit': self.price_unit
                                    })

        return {'type': 'ir.actions.act_window_close'}


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    team_id = fields.Many2one('crm.team', 'Equipo de Ventas')
    user_id = fields.Many2one('res.users', 'Vendedor')

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        cr = self.env.cr
        team_ids = False
        team_pricelist_ids = []
        user_pricelist_ids = []
        generic_pricelist_ids = []
        finally_pricelist_ids = []
        cr.execute("""
                select crm_team_id from crm_team_member where user_id=%s group by crm_team_id;
            """, (self.env.user.id,))
        cr_res = cr.fetchall()
        if cr_res and cr_res[0] and cr_res[0][0]:
            team_ids = [x[0] for x in cr_res]
        ### Tarifas de Equipos de Venta #####
        if team_ids:
            cr_res = False
            if len(team_ids) == 1:
                cr.execute("""
                    select id from product_pricelist where team_id=%s;
                """, (self.env.user.id,))
                cr_res = cr.fetchall()
            else:
                cr.execute("""
                    select id from product_pricelist where team_id in %s;
                """, (tuple(team_ids),))
                cr_res = cr.fetchall()
            if cr_res and cr_res[0] and cr_res[0][0]:
                team_pricelist_ids = [x[0] for x in cr_res]
        ##### Tarifas de Usuarios ######
        cr.execute("""
            select id from product_pricelist where user_id=%s;
        """, (self.env.user.id,))
        cr_res = cr.fetchall()
        if cr_res and cr_res[0] and cr_res[0][0]:
            user_pricelist_ids = [x[0] for x in cr_res]

        ##### Tarifas Generales ######
        # generic_pricelist_ids
        cr.execute("""
            select id from product_pricelist where user_id is null and team_id is null;
        """, (self.env.user.id,))
        cr_res = cr.fetchall()
        if cr_res and cr_res[0] and cr_res[0][0]:
            generic_pricelist_ids = [x[0] for x in cr_res]

        ### Sumando todas las Tarifas ###
        finally_pricelist_ids = team_pricelist_ids + user_pricelist_ids + generic_pricelist_ids
        if finally_pricelist_ids:
            args.append(('id', 'in', finally_pricelist_ids))
        res = super(ProductPricelist, self)._search(args, offset=offset, limit=limit,
                                                    order=order, count=count, access_rights_uid=access_rights_uid)

        return res

class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    price_surcharge_percentage = fields.Float(
        'Tarifa extra 2', digits='Product Price',
        help='Porcentaje Monto extra sobre el subtotal.')

    price_surcharge_02 = fields.Float(
        'Tarifa extra 2', digits='Product Price',
        help='Monto extra')

    price_surcharge_02_percentage = fields.Float(
        'Tarifa extra 2', digits='Product Price',
        help='Porcentaje Monto extra sobre el subtotal.')

    utility_percentage = fields.Float(
        'Utilidad', default=0, digits=(16, 2),
        help="Porcentaje de la utilidad requerida.")


    @api.constrains('utility_percentage')
    def _constraint_utility_percentage(self):
        if self.utility_percentage > 100:
            raise UserError("El porcentaje Maximo Utilidad es 100%")
        return True

    @api.constrains('price_surcharge_percentage')
    def _constraint_price_surcharge_percentage(self):
        if self.price_surcharge_percentage > 100:
            raise UserError("El porcentaje Maximo de Tarifa Extra 1 es 100%")
        return True

    @api.constrains('price_surcharge_02_percentage')
    def _constraint_price_surcharge_02_percentage(self):
        if self.price_surcharge_02_percentage > 100:
            raise UserError("El porcentaje Maximo de Tarifa Extra 2 es 100%")
        return True
    

    @api.depends_context('lang')
    @api.depends('compute_price', 'price_discount', 'price_surcharge', 'base', 'price_round', 'price_surcharge_02', 'utility_percentage', 'price_surcharge_percentage', 'price_surcharge_02_percentage')
    def _compute_rule_tip(self):
        base_selection_vals = {elem[0]: elem[1] for elem in self._fields['base']._description_selection(self.env)}
        self.rule_tip = False
        for item in self:
            if item.compute_price != 'formula':
                continue
            base_amount = 100
            discount_factor = (100 - item.price_discount) / 100
            discounted_price = base_amount * discount_factor
            if item.price_round:
                discounted_price = tools.float_round(discounted_price, precision_rounding=item.price_round)
            surcharge = tools.format_amount(item.env, item.price_surcharge, item.currency_id)
            surcharge2 = tools.format_amount(item.env, item.price_surcharge_02, item.currency_id)

            price_surcharge_1_total =  item.price_surcharge
            if item.price_surcharge_percentage:
                price_surcharge_1_result =  base_amount * (item.price_surcharge_percentage/100)
                price_surcharge_1_total = price_surcharge_1_total + price_surcharge_1_result

            price_surcharge_2_total =  item.price_surcharge_02
            if item.price_surcharge_02_percentage:
                price_surcharge_2_result =  base_amount * (item.price_surcharge_02_percentage/100)
                price_surcharge_2_total = price_surcharge_2_total + price_surcharge_2_result

            utility_percentage = item.utility_percentage
            utility_percentage_factor = (100 + utility_percentage) / 100 if utility_percentage else 1.0
            
            total_amount_utilidad_descuento = 0.0
            total_amount_utilidad = 0.0
            if item.utility_percentage and item.price_discount:
                total_amount_utilidad_descuento = ( ( 100 * utility_percentage_factor ) + price_surcharge_1_total + price_surcharge_2_total) * discount_factor
            if item.utility_percentage:
                total_amount_utilidad = ( 100 * utility_percentage_factor ) + price_surcharge_1_total + price_surcharge_2_total
            
            base_amount_surcharges = base_amount + price_surcharge_1_total + price_surcharge_2_total
            recompute_base_price = base_amount_surcharges * discount_factor 

            if not total_amount_utilidad_descuento:
                total_amount_utilidad_descuento = recompute_base_price
            if not total_amount_utilidad:
                total_amount_utilidad = recompute_base_price

            surcharge_r2 = tools.format_amount(item.env, price_surcharge_1_total, item.currency_id)
            surcharge2_r2 = tools.format_amount(item.env, price_surcharge_2_total, item.currency_id)

            item.rule_tip = _(
                "%(base)s por una utilidad %(utility_percentage)s  y un %(discount)s %% descuento mas %(surcharge)s TE 1 y %(surcharge2)s TE 2\n"
                "Ejemplo (descuento y utilidad): ((%(amount)s * %(utility_percentage_factor)s ) + %(price_surcharge)s + %(price_surcharge2)s) *  %(discount_charge)s → %(total_amount)s \n"
                "Ejemplo (utilidad): (%(amount2)s * %(utility_percentage_factor2)s) + %(price_surcharge3)s + %(price_surcharge4)s → %(total_amount2)s \n",
                base=base_selection_vals[item.base],
                utility_percentage=utility_percentage,
                discount=item.price_discount,
                surcharge=surcharge_r2,
                surcharge2=surcharge2_r2,
                amount=tools.format_amount(item.env, 100, item.currency_id),
                utility_percentage_factor=utility_percentage_factor,
                discount_charge=discount_factor,
                price_surcharge=surcharge_r2,
                price_surcharge2=surcharge2,
                total_amount=tools.format_amount(
                    item.env, total_amount_utilidad_descuento, item.currency_id),
                amount2=tools.format_amount(item.env, 100, item.currency_id),
                utility_percentage_factor2=utility_percentage_factor,
                discount_charge2=discount_factor,
                price_surcharge3=surcharge_r2,
                price_surcharge4=surcharge2_r2,
                total_amount2=tools.format_amount(
                    item.env, total_amount_utilidad, item.currency_id),
            )

    @api.onchange('compute_price')
    def _onchange_compute_price(self):
        res = super(ProductPricelistItem, self)._onchange_compute_price()
        if self.compute_price != 'formula':
            self.update({
                'price_surcharge_02': 0.0,
                'utility_percentage': 0.0,
            })
        return res

    def _compute_price(self, price, price_uom, product, quantity=1.0, partner=False):
        """Compute the unit price of a product in the context of a pricelist application.
           The unused parameters are there to make the full context available for overrides.
        """

        self.ensure_one()
        convert_to_price_uom = (lambda price: product.uom_id._compute_price(price, price_uom))
        if self.compute_price == 'fixed':
            price = convert_to_price_uom(self.fixed_price)
        elif self.compute_price == 'percentage':
            price = (price - (price * (self.percent_price / 100))) or 0.0
        else:
            ########################## CHERMAN ############################
            final_advanced_price = 0.0

            base_amount = price
            discount_factor = (100 - self.price_discount) / 100 
            discounted_price = base_amount * discount_factor
            surcharge = tools.format_amount(self.env, self.price_surcharge, self.currency_id)
            surcharge2 = tools.format_amount(self.env, self.price_surcharge_02, self.currency_id)

            utility_percentage = self.utility_percentage
            utility_percentage_factor = (100 + utility_percentage) / 100 if utility_percentage else 1.0
            
            price_surcharge_1_total =  self.price_surcharge
            if self.price_surcharge_percentage:
                price_surcharge_1_result =  base_amount * (self.price_surcharge_percentage/100)
                price_surcharge_1_total = price_surcharge_1_total + price_surcharge_1_result

            price_surcharge_2_total =  self.price_surcharge_02
            if self.price_surcharge_02_percentage:
                price_surcharge_2_result =  base_amount * (self.price_surcharge_02_percentage/100)
                price_surcharge_2_total = price_surcharge_2_total + price_surcharge_2_result

            if self.utility_percentage:
                if self.price_discount:
                    final_advanced_price = ( ( base_amount * utility_percentage_factor ) + price_surcharge_1_total + price_surcharge_2_total) * discount_factor
                
                else:
                    final_advanced_price = ( base_amount * utility_percentage_factor ) + price_surcharge_1_total + price_surcharge_2_total
            else:
                base_amount_surcharges = base_amount + price_surcharge_1_total + price_surcharge_2_total
                final_advanced_price = base_amount_surcharges * discount_factor 

            ########################## FIN ############################

            # complete formula
            price_limit = price
            price = final_advanced_price
            # price = (price - (price * (self.price_discount / 100))) or 0.0
            if self.price_round:
                price = tools.float_round(price, precision_rounding=self.price_round)

            # if self.price_surcharge:
            #     price_surcharge = convert_to_price_uom(self.price_surcharge)
            #     price += price_surcharge

            if self.price_min_margin:
                price_min_margin = convert_to_price_uom(self.price_min_margin)
                price = max(price, price_limit + price_min_margin)

            # if self.price_max_margin:
            #     price_max_margin = convert_to_price_uom(self.price_max_margin)
            #     price = min(price, price_limit + price_max_margin)
        return price