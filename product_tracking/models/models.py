# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from datetime import datetime

class Product(models.Model):
    _name = 'product_tracking.delivery'
    _rec_name = 'product_tracking_delivery'
    _description = 'Product Tracking Delivery'
    
    order = fields.Many2one('sale.order.name', "Order") 

