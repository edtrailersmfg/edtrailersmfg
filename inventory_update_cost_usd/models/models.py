# -*- coding: utf-8 -*-

from odoo import api, fields, models, _, tools
from odoo.exceptions import ValidationError, UserError
from datetime import date
from datetime import datetime

### HERENCIA ###

class ProductTemplate(models.Model):

	_inherit ='product.template'

	#fecha_tc = fields.Date(compute="_compute_fecha", string="Fecha Tipo Cambio")
	fecha_tc = fields.Date(string="Fecha Tipo Cambio")
	tipo_cambio = fields.Float(compute="_compute_tipo_cambio", string="Tipo de Cambio")
	costo_usd = fields.Float(compute="_compute_costo_usd", string="Costo en USD")

	#def _compute_fecha(self):
	#	self.fecha_tc = date.today()

	def _compute_tipo_cambio(self):
		current_date = str(datetime.now().date())
		location_model = self.env["res.currency.rate"]
		tc = location_model.search([("currency_id", "=", "USD")], order="id desc")[0]
		self.tipo_cambio = tc.inverse_company_rate
		self.fecha_tc = tc.create_date
		#raise UserError("tipo de cambio " + str(tc.inverse_company_rate))


	def _compute_costo_usd(self):
		for record in self:
			record.costo_usd = record.standard_price / record.tipo_cambio





class ProductPricelist(models.Model):

	_inherit ='product.pricelist.item'

	costo_usd = fields.Float(string="Costo en USD")




