# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    @api.model
    def _address_fields(self):
        """Returns the list of address fields that are synced from the parent."""
        return super(ResPartner, self)._address_fields() + ['township_sat_id', 'locality_sat_id', 'zip_sat_id', 'colonia_sat_id']
    
    def _get_default_country_id(self):
        country_obj = self.env['res.country']
        country = country_obj.search([('code', '=', 'MX'), ], limit=1)
        return country and country.id or False
    
    
    country_id      = fields.Many2one('res.country', string='Country', ondelete='restrict', default=_get_default_country_id)
    envio_manual_cfdi = fields.Boolean(string="Envío manual del CFDI", 
                                       help="Si marca la casilla entonces las facturas que genere a este cliente NO serán"
                                       "enviadas automáticamente al validar la factura, sino que manualmente tendrá que"
                                       "presionar el Botón de Envío correspondiente. Esto es útil si maneja Addendas o si"
                                       "el CFDI debe ser subido a algún portal del Cliente.")
    

    pay_method_id   = fields.Many2one('pay.method', string='Forma de Pago',
            help='Indica la forma de pago en que será pagada o fue pagada la factura.')


    persona_fisica  =  fields.Boolean('Persona Fisica', help='Indica si el registro de Partner es de una persona Física')
    curp            = fields.Char(string="CURP")
    num_reg_trib    =  fields.Char('NumRegIdTrib', size=40, 
                                   help="Atributo requerido para incorporar el número de identificación o registro fiscal"
                                        "del país de residencia para efectos fiscales del receptor del CFDI.\n Obligatorio"
                                        "para Clientes Extranjeros." )
    l10n_mx_street_reference =  fields.Char('Referencias', size=128, 
                                            help="Atributo requerido si el cliente recipara incorporar el número de identificación "
                                                 "o registro fiscal del país de residencia para efectos fiscales "
                                                 "del receptor del CFDI." )
    township_sat_id = fields.Many2one('res.country.township.sat.code', string='Municipio', 
                                      help='Indica el Codigo del Sat para Comercio Exterior.')
    locality_sat_id = fields.Many2one('res.country.locality.sat.code',string='Localidad',
                                      help='Indica el Codigo del Sat para Comercio Exterior.')
    zip_sat_id      = fields.Many2one('res.country.zip.sat.code', string='CP Sat', 
                                      help='Indica el Codigo del Sat para Comercio Exterior.')
    colonia_sat_id  = fields.Many2one('res.colonia.zip.sat.code', string='Colonia Sat', 
                                      help='Indica el Codigo del Sat para Comercio Exterior.')
    
    country_code_rel = fields.Char('Codigo Pais', related="country_id.code")

    company_type2 = fields.Selection([('person', 'Contacto'), 
                                      ('company', 'Persona Moral'),
                                      ('physical_person', 'Persona Fisica')], 
                                     string='Tipo Compañia', readonly=False, default="person")

    
    
    uso_cfdi_id = fields.Many2one('sat.uso.cfdi', string='Uso CFDI', required=False)

    direccion_line1 = fields.Char(string="Linea 1", compute="_get_direccion")
    direccion_line2 = fields.Char(string="Linea 2", compute="_get_direccion")
    direccion_line3 = fields.Char(string="Linea 3", compute="_get_direccion")

    regimen_fiscal_id = fields.Many2one('sat.regimen.fiscal', string="Régimen Fiscal")

    
    @api.depends('zip_sat_id', 'colonia_sat_id', 'locality_sat_id', 'township_sat_id', 'state_id', 'country_id')
    def _get_direccion(self):
        for rec in self:
            rec.direccion_line1 = ''
            rec.direccion_line2 = ''
            rec.direccion_line3 = ''
            if rec.country_id.code!='MX':
                continue
            rec.direccion_line1 = rec.colonia_sat_id.name
            direccion_line2 = ""
            if rec.township_sat_id:
                direccion_line2 = direccion_line2 + rec.township_sat_id.name
            if rec.locality_sat_id:
                direccion_line2 = direccion_line2 + ', Loc: ' + rec.locality_sat_id.name + ', '
            if rec.state_id:
                direccion_line2 = direccion_line2 + rec.state_id.code
            rec.direccion_line2 =  direccion_line2
            rec.direccion_line3 = 'CP: ' + rec.zip_sat_id.code
    
    
    @api.onchange('company_type2')
    def onchange_company_type(self):
        if self.company_type2 in ('company','physical_person'):
            self.company_type = 'company'
            self.is_company = True
            if self.company_type2 == 'physical_person':
                self.persona_fisica = True
        else:
            self.company_type = 'person'

    @api.onchange('colonia_sat_id')
    def onchange_colonia_sat_id(self):
        if self.colonia_sat_id:
            #colonia_name = "[ "+str(self.colonia_sat_id.code)+"] "+str(self.colonia_sat_id.zip_sat_code.code if self.colonia_sat_id.zip_sat_code else "")+"/ "+str(self.colonia_sat_id.name or "")
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
            
            self.city = self.township_sat_id.name

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

    
    
    
class res_partner_bank(models.Model):
    _inherit = 'res.partner.bank'

    
    def _get_take_digits(self):
        for rec in self:
            rec.last_acc_number = rec.acc_number and len(rec.acc_number) >=4 and rec.acc_number[-4:] or False
        
    clabe           = fields.Char(string='Clabe Interbancaria', size=64, required=False)
    last_acc_number = fields.Char(compute='_get_take_digits', string="Ultimos 4 digitos")
    reference       = fields.Char(string='Reference', size=64, help='Referencia para este banco')

    _sql_constraints = [
        ('unique_number', 'unique(acc_number,partner_id,bank_id)', 'Número de cuenta debe ser único por Partner y Banco'),
    ]

    
    @api.depends('bank_id', 'acc_number', 'currency_id')
    def name_get(self):
        result = []
        for x in self:
            name = (x.bank_id and (x.bank_id.name + ' - ') or '') + x.acc_number + (x.currency_id and (' (%s)' %  x.currency_id.name) or '')
            result.append((x.id, name))
        return result

### Datos Bancarios en XML  Ger ###
class ResBank(models.Model):
    _inherit ='res.bank'

    vat = fields.Char('RFC', size=64)
    country_code_rel = fields.Char('Codigo Pais', related="country.code")
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:    