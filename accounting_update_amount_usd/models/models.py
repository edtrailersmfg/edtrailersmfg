# -*- coding: utf-8 -*-

from odoo import api, fields, models, _, tools
from odoo.exceptions import ValidationError, UserError
from datetime import date
from datetime import datetime

### HERENCIA ###

class ProductTemplate(models.Model):

	_inherit ='account.move'

	#fecha_tc = fields.Date(compute="_compute_fecha", string="Fecha Tipo Cambio")
	fecha_tc = fields.Date(string="Fecha Tipo Cambio")
	tipo_cambio = fields.Float(compute="_compute_tipo_cambio", string="Tipo de Cambio")
	importe_usd = fields.Float(compute="_compute_importe_usd", string="Importe en USD")
	importe_mxn = fields.Float(compute="_compute_importe_mxn", string="Importe en MXN")

	#def _compute_fecha(self):
	#	self.fecha_tc = date.today()

	def _compute_tipo_cambio(self):
		if self.invoice_date:
			current_date = self.invoice_date
		else:
			current_date = str(datetime.now().date())
		location_model = self.env["res.currency.rate"]
		tc = location_model.search([("currency_id", "=", "USD"),("name","=",current_date)])
		self.tipo_cambio = tc.inverse_company_rate
		self.fecha_tc = tc.create_date
		self.x_studio_tipo_de_cambio = tc.inverse_company_rate
		#raise UserError("tipo de cambio " + str(tc.inverse_company_rate))

	def _compute_importe_usd(self):
		for record in self:
			if len(self) == 1:
				if record.tipo_cambio > 0:
					record.importe_usd = record.amount_total_signed / record.tipo_cambio
					if record.currency_id.name == "USD":
						record.amount_total_in_currency_signed = record.importe_usd

	def _compute_importe_mxn(self):
		for record in self:
			if len(self) == 1:
				if record.tipo_cambio > 0:
					record.importe_mxn = record.amount_total_signed * ( record.tipo_cambio / record.tipo_cambio )
					if record.currency_id.name == "MXN":
						record.amount_total_in_currency_signed = record.importe_mxn


class RegisterPayments(models.Model):

	_inherit ='account.payment'

	fecha_tc = fields.Date(string="Fecha Tipo Cambio")
	tipo_cambio = fields.Float(compute="_compute_tipo_cambio", string="Tipo de Cambio")
	importe_usd = fields.Float(compute="_compute_importe_usd", string="Importe en USD")
	importe_mxn = fields.Float(compute="_compute_importe_mxn", string="Importe en MXN")
	x_studio_tc = fields.Float(string="Tipo de Cambio")


	def _compute_tipo_cambio(self):
		if self.date:
			current_date = self.date
		else:
			current_date = str(datetime.now().date())
		location_model = self.env["res.currency.rate"]
		tc = location_model.search([("currency_id", "=", "USD"),("name","=",current_date)])
		self.tipo_cambio = tc.inverse_company_rate
		self.fecha_tc = tc.create_date
		self.x_studio_tc = tc.inverse_company_rate
		#raise UserError("tipo de cambio " + str(tc.inverse_company_rate))

	def _compute_importe_usd(self):
		for record in self:
			if len(self) == 1:
				if record.tipo_cambio > 0:
					record.importe_usd = record.amount_total_signed / record.tipo_cambio
					if record.currency_id.name == "USD":
						record.amount_total_in_currency_signed = record.importe_usd

	def _compute_importe_mxn(self):
		for record in self:
			if len(self) == 1:
				if record.tipo_cambio > 0:
					record.importe_mxn = record.amount_total_signed * ( record.tipo_cambio / record.tipo_cambio )
					if record.currency_id.name == "MXN":
						record.amount_total_in_currency_signed = record.importe_mxn



