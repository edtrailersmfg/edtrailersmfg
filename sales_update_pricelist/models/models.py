# -*- coding: utf-8 -*-

from odoo import api, fields, models, _, tools
from odoo.exceptions import ValidationError, UserError

### HERENCIA ###

class ProductPricelist(models.Model):

	_inherit ='product.pricelist.item'

	costo_usd = fields.Float(compute="_compute_costo_usd", string="Cost USD")
	costo_mxn = fields.Float(string="Cost MXN")
	profit = fields.Float(string="Profit")
	margin = fields.Float(string="Margin %")

	def _compute_costo_usd(self):
		location_model = self.env["product.template"]

		for record in self:
			id_producto = record.product_tmpl_id.id
			product_cost = location_model.search([("id", "=", record.product_tmpl_id.id)])
			record.costo_usd = product_cost.costo_usd
			record.costo_mxn = product_cost.standard_price
			record.profit = record.fixed_price - record.costo_usd
			if record.costo_usd > 0:
				record.margin = (record.profit / record.costo_usd) * 100




