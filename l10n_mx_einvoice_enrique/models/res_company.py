# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _
import time
import logging
_logger = logging.getLogger(__name__)

class ResCompany(models.Model):
    _inherit = 'res.company'

    
    pac         = fields.Selection([], string="PAC", readonly=False)
    pac_user    = fields.Char(string="Usuario PAC", readonly=False)
    pac_password= fields.Char(string="Contraseña PAC", readonly=False)
    pac_testing = fields.Boolean(string="Testing", readonly=False)
    validate_schema = fields.Boolean(string="Validar Esquema XSD en Servidor Local", 
                                     readonly=False)
    
    regimen_fiscal_id = fields.Many2one('sat.regimen.fiscal', string="Régimen Fiscal")

    address_invoice_parent_company_id = fields.Many2one("res.partner", string='Invoice Company Address Parent', 
                                                        help="In this field should \
        placed the address of the parent company , independently if \
        handled a scheme Multi-company o Multi-Address.",
                                        domain="[('type', 'in', ('invoice','default','contact'))]")
    
    
    def _get_company_address_update(self, partner):
        res = super(ResCompany, self)._get_company_address_update(partner)
        res.update({'township_sat_id' : partner.township_sat_id,
                    'locality_sat_id' : partner.locality_sat_id,
                    'zip_sat_id'      : partner.zip_sat_id,
                    'colonia_sat_id'  : partner.colonia_sat_id,            
                    })
        return res
    

    
    def _inverse_township_sat_id(self):
        for company in self:
            company.partner_id.township_sat_id = company.township_sat_id.id

    def _inverse_locality_sat_id(self):
        for company in self:
            company.partner_id.locality_sat_id = company.locality_sat_id.id

    def _inverse_zip_sat_id(self):
        for company in self:
            company.partner_id.zip_sat_id = company.zip_sat_id.id

    def _inverse_colonia_sat_id(self):
        for company in self:
            company.partner_id.colonia_sat_id = company.colonia_sat_id.id


    township_sat_id = fields.Many2one('res.country.township.sat.code', string='Municipio', 
                                      compute='_compute_address', inverse='_inverse_township_sat_id')
    locality_sat_id = fields.Many2one('res.country.locality.sat.code', string='Localidad', 
                                      compute='_compute_address', inverse='_inverse_locality_sat_id',
                                     help='Indica el Codigo del Sat para Comercio Exterior.')
    zip_sat_id = fields.Many2one('res.country.zip.sat.code', string='CP Sat', 
                                 compute='_compute_address', inverse='_inverse_zip_sat_id',
                                 help='Indica el Codigo del Sat para Comercio Exterior.')
    colonia_sat_id = fields.Many2one('res.colonia.zip.sat.code', string='Colonia Sat', 
                                     compute='_compute_address', inverse='_inverse_colonia_sat_id',
                                     help='Indica el Codigo del Sat para Comercio Exterior.')

    country_code_rel = fields.Char('Codigo Pais', related="country_id.code")
    
    
    def get_address_invoice_parent_company_id(self):
        partner_obj = self.pool.get('res.partner')
        company_id = self
        partner_parent = company_id and company_id.parent_id and company_id.parent_id.partner_id or False
        if partner_parent:
            address_id = partner_parent.address_get(['invoice'])['invoice']
        elif company_id.company_address_main_id:
            address_id = company_id.company_address_main_id.id
        else:
            address_id = self.partner_id.address_get(['invoice'])['invoice']
        return address_id

    @api.onchange('colonia_sat_id')
    def onchange_colonia_sat_id(self):
        if self.colonia_sat_id:
            """
            colonia_name = "[ "+str(self.colonia_sat_id.code)+"] "+str(self.colonia_sat_id.zip_sat_code.code if self.colonia_sat_id.zip_sat_code else "")+"/ "+str(self.colonia_sat_id.name or "")

            self.street2 = colonia_name
            township_name = "[ "+self.colonia_sat_id.zip_sat_code.township_sat_code.code+" ] "+self.colonia_sat_id.zip_sat_code.township_sat_code.name
            self.city = township_name
            self.township_sat_id = self.colonia_sat_id.zip_sat_code.township_sat_code.id
            self.locality_sat_id = self.colonia_sat_id.zip_sat_code.locality_sat_code.id if self.colonia_sat_id.zip_sat_code.locality_sat_code else False
            self.zip_sat_id = self.colonia_sat_id.zip_sat_code.id
            self.zip_sat_id = self.colonia_sat_id.zip_sat_code.id
            
            #country_sat_code = self.colonia_sat_id.zip_sat_code.state_sat_code.country_sat_code.id
            #country_id = self.env['res.country'].search([('sat_code','=',country_sat_code)])
            country_id = self.colonia_sat_id.zip_sat_code.state_sat_code.country_id
            self.country_id = country_id.id if country_id else False
            """
            self.city = self.colonia_sat_id.zip_sat_code.township_sat_code.name
            self.street2 = self.colonia_sat_id.name

    @api.onchange('zip_sat_id')
    def onchange_zip_sat_id(self):
        if self.zip_sat_id:
            self.zip = self.zip_sat_id.code
            self.township_sat_id = self.zip_sat_id.township_sat_code.id
            self.locality_sat_id = self.zip_sat_id.locality_sat_code.id

            #state_sat_code = self.zip_sat_id.state_sat_code.id
            #state_id = self.env['res.country.state'].search([('sat_code','=',state_sat_code),('country_id','=',self.country_id.id)])
            state_id = self.zip_sat_id.state_sat_code
            if state_id:
                self.state_id = state_id.id
                self.country_id = state_id.country_id.id
            colonia_sat_id = self.env['res.colonia.zip.sat.code'].search([('zip_sat_code','=',self.zip_sat_id.id)], limit=1)
            if colonia_sat_id:
                self.colonia_sat_id = colonia_sat_id.id

    @api.onchange('state_id')
    def onchange_domain_sat_list(self):
        domain = {}
        if self.state_id:
            township_obj = self.env['res.country.township.sat.code']
            township_ids = township_obj.search([('state_sat_code.code','=',self.state_id.code)])
            if township_ids:
                domain.update(
                    {
                        'township_sat_id':[('id','in',[x.id for x in township_ids])]
                    })
            locality_obj = self.env['res.country.locality.sat.code']
            locality_ids = locality_obj.search([('state_sat_code.code','=',self.state_id.code)])
            if locality_ids:
                domain.update(
                    {
                        'locality_sat_id':[('id','in',[x.id for x in locality_ids])]
                    })

        return {'domain': domain}
    
    

class ResCompanyGetCFDICountWizard(models.TransientModel):
    _name = 'res.company.getcfdicount'
    _description = "Wizard - CFDIs consumidos de una fecha al dia de hoy"
    
    
    date = fields.Date(string="Desde", default=fields.Date.context_today)
    state    = fields.Selection([('step1','Paso 1'), ('step2', 'Paso 2')],
                                   default='step1', string="Estado")
    conteo = fields.Integer("CFDIs consumidos")
    
    def get_cfdi_count(self):
        self.ensure_one()
        invoices = self.env['account.move'].search([('move_type','in',('out_invoice','out_refund')),
                                                       ('cfdi_folio_fiscal','!=',False),
                                                       ('invoice_date','>=',self.date)])
        payments = self.env['account.payment'].search([('payment_type','=','inbound'),
                                                       ('cfdi_folio_fiscal','!=',False),
                                                       ('date','>=',self.date)])
        
        self.write({'state' : 'step2',
                    'conteo' : len(list(invoices)) + len(list(payments))})
    
        return self._reopen_wizard(self.id)

    
    def _reopen_wizard(self, res_id):
        return {'type'      : 'ir.actions.act_window',
                'res_id'    : res_id,
                'view_mode' : 'form',
                'view_type' : 'form',
                'res_model' : 'res.company.getcfdicount',
                'target'    : 'new',
                'name'      : 'Conteo de CFDIs consumidos'}
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:    