# -*- coding:utf-8 -*-
from odoo import fields, models
from odoo.exceptions import UserError

from datetime import datetime


class MaterialsRequirementSimulation(models.Model):
    _name = 'materials.requirement.simulation'

    order_id = fields.Many2one('sale.order', 'Orden de venta')
    partner_id = fields.Many2one('res.partner', 'Cliente')
    delivery_date = fields.Date('Fecha de entrega')
    product_id = fields.Many2one('product.product', 'Material')
    qty_available = fields.Float('Cantidad a mano')
    virtual_available = fields.Float('Cantidad pronosticada')
    required_qty = fields.Float('Cantidad requerida')
    purchase_qty = fields.Float('Cantidad a comprar')
    user_id = fields.Many2one('res.user', 'Usuario')
    required_total_cost = fields.Float('Costo ctd requerida')
    purchase_total_cost = fields.Float('Costo ctd a comprar')

    def create_draft_purchase_orders(self):
        # verificar que todos los productos tengan proveedor
        non_seller_ids = self.filtered(
            lambda ln: not len(ln.product_id.seller_ids)
        )
        if non_seller_ids:
            # lanzar error informando que productos requieren proveedor
            prod_names = list(map(
                lambda name: f'* {name}', 
                non_seller_ids.mapped('product_id.name')
            ))
            msg = 'Configure un proveedor para los productos:\n\n'
            msg += '\n'.join(prod_names)
            raise UserError(msg)
        # mapear cada producto a su proveedor
        supplier_and_prods = {}
        # lista sin repeticiones de producto, con cantidad > 0
        product_ids = self.filtered(
                lambda ln: ln.purchase_qty > 0    
            ).mapped('product_id')
        for prod in product_ids:
            # obtener el primer proveedor configurado
            supplier_id = prod.seller_ids.sorted(
                    lambda seller: seller.id
                )[0].name
            # obtener los productos mapeados a este proveedor
            # o una lista vacia default
            current_prods = supplier_and_prods.get(
                supplier_id, []
            )
            # sumar cantidadas para todo registro del producto
            filter = lambda rec: rec.product_id == prod
            prod_qty = sum(
                self.filtered(filter).mapped('required_qty')
            )
            # agregar a la lista el producto actual y asignar al mapeo
            current_prods.append((prod, prod_qty))
            supplier_and_prods[supplier_id] = current_prods
        # generar una orden de compra por cada proveedor mapeado
        PurchaseOrder = self.env['purchase.order']
        for supplier_id, products in supplier_and_prods.items():
            order_ref = f"Simulación {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}, {self.env.user.name}"
            PurchaseOrder.create({
                'partner_id' : supplier_id.id,
                'origin' : order_ref,
                'order_line' : [
                                (0, 0,  {
                                            'product_id' : prod.id,
                                            'product_qty' : qty
                                        }) 
                                for prod, qty in products
                                ]
            })
        # informar al usuario
        return self.env['wizard.display.message']\
            .get_message_act('Las órdenes de compra han sido creadas exitosamente')