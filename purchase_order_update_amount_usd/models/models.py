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
	tipo_cambio = fields.Float(string="Tipo Cambio", default=1)
	importe_usd = fields.Float(string="Importe USD")
	importe_mxn = fields.Float(string="Importe MXN")

	#def _compute_fecha(self):
	#	self.fecha_tc = date.today()

	@api.onchange('tipo_cambio')
	def on_change_tipo_cambio(self):
		if self.tipo_cambio > 0:
			if self.currency_id.name == "MXN":
				self.importe_usd = self.amount_total / self.tipo_cambio
				self.importe_mxn = self.amount_total
			else:
				self.importe_usd = self.amount_total
				self.importe_mxn = self.amount_total * self.tipo_cambio

	#def _compute_tipo_cambio(self):
		#reg = self.env['res.currency.rate'].search([('id', '>', 0)], limit=1, order="id desc")
		#if reg:
			#for record in reg:
				#raise UserError("Fecha %s" % (record.inverse_company_rate) )
				#tipo_de_cambio = record.inverse_company_rate
				#fecha_tipocambio = record.create_date

		#self.tipo_cambio = tipo_de_cambio
		#self.fecha_tc = fecha_tipocambio
		#self.x_studio_tipo_de_cambio = tipo_de_cambio

	#def _compute_importe_usd(self):
		#for record in self:
			#if len(self) == 1:
				#if record.tipo_cambio > 0:
					#record.importe_usd = record.amount_total / record.tipo_cambio
					#if record.currency_id.name == "USD":
					#	record.amount_total_in_currency_signed = record.importe_usd

	#def _compute_importe_mxn(self):
		#for record in self:
			#if len(self) == 1:
				#if record.tipo_cambio > 0:
					#record.importe_mxn = record.amount_total * ( record.tipo_cambio / record.tipo_cambio )
					#if record.currency_id.name == "MXN":
					#	record.amount_total_in_currency_signed = record.importe_mxn



class RequisitionTemplate(models.Model):

	_inherit ='purchase.requisition'

	#fecha_tc = fields.Date(compute="_compute_fecha", string="Fecha Tipo Cambio")
	fecha_tc = fields.Date(string="Fecha TC")
	tipo_cambio = fields.Float(string="Tipo Cambio", default=1)
	importe_usd = fields.Float(string="Importe USD")
	importe_mxn = fields.Float(string="Importe MXN")