# -*- coding: utf-8 -*-

from odoo import api, fields, models, _, tools
from odoo.exceptions import ValidationError, UserError
from datetime import date
from datetime import datetime

### HERENCIA ###

class ProductTemplate(models.Model):

	_inherit ='purchase.order'

	#fecha_tc = fields.Date(compute="_compute_fecha", string="Fecha Tipo Cambio")
	fecha_tc = fields.Date(string="Fecha TC")
	tipo_cambio = fields.Float(compute="_compute_tipo_cambio", string="Tipo Cambio")
	importe_usd = fields.Float(compute="_compute_importe_usd", string="Importe USD")
	importe_mxn = fields.Float(compute="_compute_importe_mxn", string="Importe MXN")

	#def _compute_fecha(self):
	#	self.fecha_tc = date.today()

	def _compute_tipo_cambio(self):
		reg = self.env['res.currency.rate'].search([('id', '>', 0)], limit=1, order="id desc")
		if reg:
			for record in reg:
				#raise UserError("Fecha %s" % (record.inverse_company_rate) )
				tipo_de_cambio = record.inverse_company_rate
				fecha_tipocambio = record.create_date

		self.tipo_cambio = tipo_de_cambio
		self.fecha_tc = fecha_tipocambio
		#self.x_studio_tipo_de_cambio = tipo_de_cambio

	def _compute_importe_usd(self):
		for record in self:
			if len(self) == 1:
				if record.tipo_cambio > 0:
					record.importe_usd = record.amount_total_signed / record.tipo_cambio
					#if record.currency_id.name == "USD":
					#	record.amount_total_in_currency_signed = record.importe_usd

	def _compute_importe_mxn(self):
		for record in self:
			if len(self) == 1:
				if record.tipo_cambio > 0:
					record.importe_mxn = record.amount_total_signed * ( record.tipo_cambio / record.tipo_cambio )
					#if record.currency_id.name == "MXN":
					#	record.amount_total_in_currency_signed = record.importe_mxn


