# -*- coding:utf-8 -*-
from odoo import fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'


    def simulate_materials_requirement(self):
        # filtrar pedidos que no esten confirmados
        not_allowed_state = self.filtered(
            lambda ln: ln.state == 'cancel'
        )
        if len(not_allowed_state):
            raise UserError(
                'Elija únicamente pedidos confirmados o cotizaciones'
            )

        BoM = self.env['mrp.bom']
        
        # verificar que todos los productos sean a producir 
        non_manufactured_prods = []
        bomless_prods = []
        all_prods_ids = self.mapped('order_line').mapped('product_id') 
        for prod in all_prods_ids:
            # buscar nombre "manufacture" como bandera que indica a producir
            has_manufacture = prod.route_ids.filtered(
                lambda r: 'manufacture' in r.name.lower() \
                    or 'fabrica' in r.name.lower() \
                    or 'produc' in r.name.lower()
            )
            if not has_manufacture:
                non_manufactured_prods.append(
                    f'* {prod.name}'
                )
            # verificar tambien si existe una BoM para el producto
            bom_id = BoM.search(
                [('product_tmpl_id.id', '=', prod.product_id)]
            )
            if not len(bom_id):
                bomless_prods.append(
                    f'* {prod.id} - {prod.default_code}'
                )


        # lanzar excepcion si hay productos mal configurados
        if len(non_manufactured_prods):
            msg = 'Configure los siguientes productos para producir:\n'
            msg += '\n'.join(non_manufactured_prods)
            raise UserError(msg)
        # lanzar excepcion si hay productos sin BoM
        if len(bomless_prods):
            msg = 'Configure una lista de materiales para los productos:\n'
            msg += '\n'.join(bomless_prods)
            raise UserError(msg)

        MaterialsReqSimulation = self.env['materials.requirement.simulation']
        # elimina las lineas que haya generado este usuario previamente
        MaterialsReqSimulation\
            .search([('user_id', '=', self.env.user.id)])\
            .unlink()
            
        # iterar sobre las ordenes
        for order in self:
            order_exploded_qtys = {}
            # iterar sobre partidas en la orden
            for line in order.order_line:
                if not line.product_uom_qty:
                    # algunas partidas pueden ir en cero (?????)
                    continue
                # obtener bom del producto y explotarla
                # lo relevante son solo las lineas (index=1)
                bom_id = BoM.search(
                    [('product_tmpl_id', '=', line.product_id.id)]
                )
                exploded_product_qtys = bom_id.explode(
                    line.product_id, line.product_uom_qty
                )[1]
                # agrupar los productos explotados con sus cantidades
                for prod_line in exploded_product_qtys:
                    current_qty = order_exploded_qtys.get(
                        prod_line[0].product_id, False
                    )
                    order_exploded_qtys[prod_line[0].product_id] = \
                        current_qty + prod_line[1]['qty']
            # todas las partidas estan explotadas y agrupadas
            # crear registros de simulacion
            for product_id, qty in order_exploded_qtys.items():
                purchase_qty = qty - product_id.virtual_available
                MaterialsReqSimulation.create({
                    'order_id' : order.id,
                    'partner_id' : order.partner_id.id,
                    'delivery_date' : order.fecha_compromiso,
                    'product_id' : product_id.id,
                    'qty_available' : product_id.qty_available,
                    'virtual_available' : product_id.virtual_available,
                    'required_qty' : qty,
                    'purchase_qty' : purchase_qty,
                    'user_id' : self.env.user.id,
                    'required_total_cost' : qty * product_id.standard_price,
                    'purchase_total_cost' : purchase_qty * product_id.standard_price
                })

        return {
            'type' : 'ir.actions.act_window',
            'res_model' : 'materials.requirement.simulation',
            'name' : 'Simulación de requerimiento de material',
            'view_mode' : 'tree',
            'context' : {'search_default_grp_product' : 1},
            'domain' : [('user_id', '=', self.env.user.id)]
        }