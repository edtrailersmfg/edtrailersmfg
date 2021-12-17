# -*- encoding: utf-8 -*-
from odoo import api, fields, models, _, tools, release
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
import odoo.addons.decimal_precision as dp
import logging
_logger = logging.getLogger(__name__)


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    @api.depends('quantity','product_uom_id','product_id')
    def _compute_cce_quantity(self):
        for rec in self:
            if not rec.display_type and rec.product_id and rec.product_id.sat_factor_conversion:
                if rec.product_id.uom_id != rec.product_uom_id:
                    rec.cce_quantity = rec.product_uom_id._compute_quantity(rec.quantity, rec.product_id.uom_id) * rec.product_id.sat_factor_conversion
                    
                else:
                    rec.cce_quantity = rec.quantity * rec.product_id.sat_factor_conversion
            else:
                rec.cce_quantity = 0
            
    
    cce_complemento = fields.Selection(related="move_id.cfdi_complemento")
    cce_quantity = fields.Float(string='Cant. CCE', digits='Product Unit of Measure',
                               compute="_compute_cce_quantity", store=True)
    cce_sat_arancel_id = fields.Many2one('sat.arancel', string="Fracción Arancelaria",
                                        related="product_id.sat_arancel_id", store=True, readonly=True)
    cce_uom = fields.Selection(related="cce_sat_arancel_id.unidad_de_medida",
                              store=True)

        
class AccountMove(models.Model):
    _inherit = 'account.move'
                
       
    
    @api.depends('invoice_line_ids', 'state','invoice_date')
    def _get_comercio_exterior_total_usd(self):
        currency_usd = self.env['res.currency'].search([('name','=','USD')], limit=1)
        for rec in self:            
            totalusd = 0.0
            if rec.move_type == 'out_invoice' and rec.cfdi_complemento=='comercio_exterior':
                for line in self.invoice_line_ids:
                    totalusd += rec.currency_id._convert((line.price_unit * line.quantity), currency_usd, rec.company_id, rec.invoice_date or fields.Date.today())
                    #totalusd += round(rec.currency_id.with_context(date=rec.invoice_date).compute(line.price_unit * line.quantity, currency_usd),2)
            rec.cfdi_comercio_exterior_total_usd = totalusd
    
        
    
    cfdi_complemento = fields.Selection(selection_add=[('comercio_exterior', 'Comercio Exterior')], 
                                        ondelete={'comercio_exterior': 'set default'})
    cfdi_motivo_traslado =fields.Selection([('01','Envío de mercancias facturadas con anterioridad'),
                                            ('02','Reubicación de mercancías propias'),
                                            ('03','Envío de mercancías objeto de contrato de consignación'),
                                            ('04','Envío de mercancías para posterior enajenación'),
                                            ('05','Envío de mercancías propiedad de terceros'),
                                            ('99','Otros')],
                                           readonly=True, states={'draft': [('readonly', False)]}, copy=False,
                                         string="Motivo de Traslado")
    cfdi_certificado_origen = fields.Selection([('0','[0] No Funge como certificado de origen'),
                                                ('1','[1] Funge como certificado de origen')],
                                               readonly=True, states={'draft': [('readonly', False)]}, copy=False,
                                               string="Certificado Origen")
    cfdi_num_certificado_origen = fields.Char(string="Número Certificado Origen",
                                             readonly=True, states={'draft': [('readonly', False)]}, copy=False)
    #cfdi_num_exportador_confiable = fields.Char(string="Número Exportador Confiable",
    #                                           readonly=True, states={'draft': [('readonly', False)]}, copy=False)
    cfdi_comercio_exterior_notas = fields.Text(string="Observaciones (Complemento Comercio Exterior)",
                                              readonly=True, states={'draft': [('readonly', False)]}, copy=False)
    cfdi_comercio_exterior_total_usd = fields.Float(string="Total USD", digits=(16, 2), compute="_get_comercio_exterior_total_usd",
                                                   readonly=True, store=True)
    cfdi_comercio_exterior_propietario_id  = fields.Many2one('res.partner', string="Propietario",
                                                            readonly=True, states={'draft': [('readonly', False)]}, copy=False)

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        res = super(AccountMove, self)._onchange_partner_id()
        if self.partner_id.parent_id:
            if self.partner_id.parent_id.cfdi_comercio_exterior_notas:
                self.cfdi_comercio_exterior_notas = self.partner_id.parent_id.cfdi_comercio_exterior_notas
            else:
                if self.partner_id.cfdi_comercio_exterior_notas:
                    self.cfdi_comercio_exterior_notas = self.partner_id.cfdi_comercio_exterior_notas
        else:
            if self.partner_id.cfdi_comercio_exterior_notas:
                self.cfdi_comercio_exterior_notas = self.partner_id.cfdi_comercio_exterior_notas 
                
    def _get_einvoice_complement_dict(self, xcomprobante):
        if self.cfdi_complemento != 'comercio_exterior':
            return super(AccountMove, self)._get_einvoice_complement_dict(xcomprobante)
        
        if 'transport_document_cfdi' in self._fields and self.transport_document_cfdi:
            raise UserError(_('Advertencia !!! Por el momento no se soporta el Complemento de Comercio Exterior con CFDI de Traslado'))
        
        
        comprobante = xcomprobante.copy()
        
        currency_usd = self.env['res.currency'].search([('name','=','USD')], limit=1)
        rate = currency_usd.with_context(date=self.invoice_date).rate
        rate = rate != 0 and 1.0/rate or 0.0
        if rate == 1.0:
            rate = 1
        else:
            rate = '%.4f' % rate or 1
        
        if not (rate and self.cfdi_comercio_exterior_total_usd):
            raise UserError(_('Error !!! No ha definido la información relacionada al Tipo de Cambio a usar en Complemento de Comercio Exterior y/o el Total en USD no está definido'))
        complemento = {'cce11:ComercioExterior': 
                        {
                        'xmlns:cce11'       : "http://www.sat.gob.mx/ComercioExterior11",
                        'xsi:schemaLocation': "http://www.sat.gob.mx/ComercioExterior11 http://www.sat.gob.mx/sitio_internet/cfd/ComercioExterior11/ComercioExterior11.xsd",
                        'xmlns:xsi'         : "http://www.w3.org/2001/XMLSchema-instance",                            
                        'Version'           : '1.1',
                        'MotivoTraslado'    : self.cfdi_motivo_traslado,
                        'TipoOperacion'     : '2',
                        'ClaveDePedimento'  : 'A1',
                        'CertificadoOrigen' : self.cfdi_certificado_origen,
                        'NumCertificadoOrigen'  : self.cfdi_num_certificado_origen,
                        'NumeroExportadorConfiable' : self.company_id.cfdi_num_exportador_confiable or '',
                        'Incoterm'          : self.invoice_incoterm_id.code,
                        'Subdivision'       : '0', #self.cfdi_comercio_exterior_subdivision,
                        'Observaciones'     : self.cfdi_comercio_exterior_notas or '.',
                        'TipoCambioUSD'     : rate,
                        'TotalUSD'          : self.cfdi_comercio_exterior_total_usd and "{0:.2f}".format(self.cfdi_comercio_exterior_total_usd) or '',
                        }
                    }
        
        diccionario = complemento['cce11:ComercioExterior'].copy()
        for key, value in diccionario.items():
            if key not in ('CertificadoOrigen','TotalUSD') and not bool(value):
                complemento['cce11:ComercioExterior'].pop(key)
        if not complemento['cce11:ComercioExterior']['CertificadoOrigen'] and complemento['cce11:ComercioExterior']['NumCertificadoOrigen']:
            raise UserError(_('El campo "Número Certificado Origen" debe estar vacío si "Certificado Origen" está establecido como: "No funge como certificado de origen"'))
        
        # ------- ------- EMISOR ------- -------
        complemento['cce11:ComercioExterior'].update({'cce11:Emisor': {}})
        
        address_invoice_parent = self.address_issued_id or False
        if not address_invoice_parent:
            raise UserError(_('Error !!! No se encontró la Dirección de emisión'))
        
        if address_invoice_parent.persona_fisica and not address_invoice_parent.curp:
            raise UserError(_('Error !!! El Emisor está marcado como Persona Física pero no tiene definido el CURP'))
        
        if not (address_invoice_parent.street and \
                address_invoice_parent.zip_sat_id.code and \
                address_invoice_parent.state_id.code and \
                address_invoice_parent.country_id.sat_code
               ):
            raise UserError(_("Error !!! La dirección del Emisor parece estar incompleta o algún valor no tiene relacionado el Código SAT correspondiente,"
                              "por favor revise que tenga los siguientes datos en la dirección:\n"
                              "- Calle\n"
                              "- Código Postal\n"
                              "- Estado\n"
                              "- País"
                             ))        
        
        _logger.info("\n########## address_invoice_parent: %s" % address_invoice_parent)
        _logger.info("\n########## address_invoice_parent.curp: %s" % address_invoice_parent.curp)
        if address_invoice_parent.curp:
            complemento['cce11:ComercioExterior']['cce11:Emisor'].update({'Curp':address_invoice_parent.curp})
        
        complemento['cce11:ComercioExterior']['cce11:Emisor'].update({'cce11:Domicilio': {
            'Calle'     : address_invoice_parent.street,
            'CodigoPostal' : address_invoice_parent.zip_sat_id.code,
            'Estado'    : address_invoice_parent.state_id.code,
            'Pais'      : address_invoice_parent.country_id.sat_code
            }})
        
        
        if address_invoice_parent.street_number:
            complemento['cce11:ComercioExterior']['cce11:Emisor']['cce11:Domicilio'].update({'NumeroExterior': address_invoice_parent.street_number})
            
        if address_invoice_parent.street_number2:
            complemento['cce11:ComercioExterior']['cce11:Emisor']['cce11:Domicilio'].update({'NumeroInterior': address_invoice_parent.street_number2})

        if address_invoice_parent.colonia_sat_id.code:
            complemento['cce11:ComercioExterior']['cce11:Emisor']['cce11:Domicilio'].update({'Colonia': address_invoice_parent.colonia_sat_id.code})

        if address_invoice_parent.locality_sat_id.code:
            complemento['cce11:ComercioExterior']['cce11:Emisor']['cce11:Domicilio'].update({'Localidad': address_invoice_parent.locality_sat_id.code})

        if address_invoice_parent.township_sat_id.code:
            complemento['cce11:ComercioExterior']['cce11:Emisor']['cce11:Domicilio'].update({'Municipio': address_invoice_parent.township_sat_id.code})
        
        # ------- ------- PROPIETARIO ------- 
        # ------- SOLO SE AÑADE SI EL TIPO DE COMPROBANTE ES T - TRASLADO - Aun no se soporta
        if ('transport_document_cfdi' in self._fields and self.transport_document_cfdi) and not self.cfdi_comercio_exterior_propietario_id:
            raise UserError(_('Error !!! El tipo de Comprobante es de Traslado y exige que se defina el Propietario de la Mercancía'))
        elif 'transport_document_cfdi' in self._fields and self.transport_document_cfdi:
            if not (self.cfdi_comercio_exterior_propietario_id.num_reg_trib and self.cfdi_comercio_exterior_propietario_id.country_id.sat_code):
                raise UserError(_('Error !!! El Propietario no tiene definido el Registro Tributario o el País, no es posible generar el CFDI sin esa información'))
            complemento['cce11:ComercioExterior'].update({'cce11:Propietario': {
                'NumRegIdTrib'     : self.cfdi_comercio_exterior_propietario_id.num_reg_trib,
                'ResidenciaFiscal' : self.cfdi_comercio_exterior_propietario_id.country_id.sat_code,
            }})        
        
        # ------- ------- RECEPTOR ------- -------
        complemento['cce11:ComercioExterior'].update({'cce11:Receptor': {}})
        partner = self.partner_id.commercial_partner_id
        
        if partner.country_id.code != 'MX':
            if not partner.num_reg_trib:
                raise UserError(_('Error !!! El cliente es extranjero pero no tiene definido el Registro Tributario, no es posible generar el CFDI sin esa información'))
        
        if not (partner.street and partner.zip and partner.state_id and partner.country_id.sat_code):
            raise UserError(_("Error !!! La dirección del Receptor parece estar incompleta o algún valor no tiene relacionado el Código SAT correspondiente,"
                              "por favor revise que tenga los siguientes datos en la dirección:\n"
                              "- Calle\n"
                              "- Código Postal / PO BOX\n"
                              "- Estado\n"
                              "- País"
                             ))
        
        if partner.country_id.code in ('CAN','USA','MX') and not partner.state_id.code:
            raise UserError('Para los Receptores de países México / Canadá / Estados Unidos es indispensable que cree el estado esté asociado en el Catálogo de Estados del SAT, por favor revise Configuración => Catálogos SAT CFDI => Catálogo Códigos de Estados')
            
        complemento['cce11:ComercioExterior']['cce11:Receptor'].update({'cce11:Domicilio': {
            'Calle'     : partner.street,
            'CodigoPostal' : partner.zip or partner.zip_sat_id.code,
            'Estado'    : (partner.state_id.code and partner.state_id.code) or partner.state_id.name,
            'Pais'      : partner.country_id.sat_code,
            }})

        if not complemento['cce11:ComercioExterior']['cce11:Receptor']['cce11:Domicilio']['CodigoPostal']:
            complemento['cce11:ComercioExterior']['cce11:Receptor']['cce11:Domicilio'].pop('CodigoPostal')
        
        comprobante['cfdi:Comprobante']['cfdi:Receptor'].update({'NumRegIdTrib'     : partner.num_reg_trib,
                                                                 'ResidenciaFiscal' : partner.country_id.sat_code})
        
        if partner.street_number:
            complemento['cce11:ComercioExterior']['cce11:Receptor']['cce11:Domicilio'].update({'NumeroExterior': partner.street_number})
            
        if partner.street_number2:
            complemento['cce11:ComercioExterior']['cce11:Receptor']['cce11:Domicilio'].update({'NumeroInterior': partner.street_number2})
        

        # ------- ------- DESTINATARIO ------- -------
        if partner != self.partner_shipping_id and self.partner_shipping_id:
            complemento['cce11:ComercioExterior'].update({'cce11:Destinatario': {}})
            partner = self.partner_shipping_id

            if not partner.num_reg_trib:
                raise UserError(_('Error !!! El Destinatario no tiene definido el Registro Tributario, no es posible generar el CFDI sin esa información'))

            complemento['cce11:ComercioExterior']['cce11:Destinatario'].update({'NumRegIdTrib': partner.num_reg_trib})

            if not (partner.street and partner.state_id.code and partner.country_id.sat_code):
                raise UserError(_("Error !!! La dirección del Receptor parece estar incompleta o algún valor no tiene relacionado el Código SAT correspondiente,"
                                  "por favor revise que tenga los siguientes datos en la dirección:"
                                  "- Calle"
                                  "- Estado"
                                  "- País"
                                 ))

            complemento['cce11:ComercioExterior']['cce11:Destinatario'].update({'cce11:Domicilio': {
                'Calle'     : partner.street,
                'CodigoPostal' : partner.zip_sat_id.code,
                'Estado'    : partner.state_id.code,
                'Pais'      : partner.country_id.sat_code
                }})

            if partner.street_number:
                complemento['cce11:ComercioExterior']['cce11:Destinatario']['cce11:Domicilio'].update({'NumeroExterior': partner.street_number})

            if partner.street_number2:
                complemento['cce11:ComercioExterior']['cce11:Destinatario']['cce11:Domicilio'].update({'NumeroInterior': partner.street_number2})

            if partner.colonia_sat_id.code:
                complemento['cce11:ComercioExterior']['cce11:Destinatario']['cce11:Domicilio'].update({'Colonia': partner.colonia_sat_id.code or partner.street2})

            if partner.locality_sat_id.code:
                complemento['cce11:ComercioExterior']['cce11:Destinatario']['cce11:Domicilio'].update({'Localidad': partner.locality_sat_id.code})

            if partner.township_sat_id.code:
                complemento['cce11:ComercioExterior']['cce11:Destinatario']['cce11:Domicilio'].update({'Municipio': partner.township_sat_id.code or partner.city})

        # ----- ----- MERCANCIAS ----- -----
        complemento['cce11:ComercioExterior'].update({'cce11:Mercancias': []})
        group_to_ce_mercancia = {}
        for line in self.invoice_line_ids.filtered(lambda w: not w.display_type):
            if not line.cce_quantity:
                raise UserError(_("Error !!!\n\nNo definió la Cantidad de Producto Aduana para el producto %s, no es posible generar el CFDI...") % line.product_id.name)
            if not line.product_id.sat_arancel_id:
                raise UserError(_("Error !!!\n\nEl producto %s no tiene definida la Fracción Arancelaria, no es posible generar el CFDI...") % line.product_id.name)
            
            ### Añadiendo el No de Indentificacion
            product_code = ""
            if line.product_id.no_identity_type:
                if line.product_id.no_identity_type != 'none':
                    if line.product_id.no_identity_type == 'default_code':
                        product_code = line.product_id.default_code 
                    elif line.product_id.no_identity_type == 'barcode':
                        product_code = line.product_id.barcode
                    else:
                        product_code = line.product_id.no_identity_other

            if not product_code:
                product_code = line.product_id.default_code
                if not product_code:
                    raise UserError(_("Error !!!\n\nEl producto %s no tiene definido el Identificador (Referencia), no es posible generar el CFDI...") % line.product_id.name)            
            
            cantidad_aduana = 0.0
            valor_dolares = 0.0
            if line.product_id in group_to_ce_mercancia:
                vals_line_prev = group_to_ce_mercancia[line.product_id]
                cantidad_aduana = vals_line_prev['CantidadAduana']
                valor_dolares = vals_line_prev['ValorDolares']
                conversion_usd = self.currency_id.with_context(date=self.invoice_date).compute(line.price_unit * line.quantity, currency_usd)
                group_to_ce_mercancia[line.product_id].update({
                         'CantidadAduana'       : line.cce_quantity+cantidad_aduana or 0.0,
                         'ValorDolares'  : conversion_usd + valor_dolares,
                          })
            else:
                group_to_ce_mercancia.update({
                    line.product_id: {'NoIdentificacion'     : product_code,
                         'FraccionArancelaria'  : line.product_id.sat_arancel_id.code or '',
                         'CantidadAduana'       : line.cce_quantity or 0.0,
                         'UnidadAduana'         : line.product_id.sat_arancel_id.unidad_de_medida or '',
                         'ValorUnitarioAduana'  : self.currency_id.with_context(date=self.invoice_date).compute((line.price_unit * line.quantity) / line.cce_quantity, currency_usd),
                         'ValorDolares'         : self.currency_id.with_context(date=self.invoice_date).compute(line.price_unit * line.quantity, currency_usd),
                        }
                    })
            # concepto = {'cce11:Mercancia':
            #             {'NoIdentificacion'     : product_code,
            #              'FraccionArancelaria'  : line.product_id.sat_arancel_id.code or '',
            #              'CantidadAduana'       : "%.2f" % line.cce_quantity+cantidad_aduana or 0.0,
            #              'UnidadAduana'         : line.product_id.sat_arancel_id.unidad_de_medida or '',
            #              'ValorUnitarioAduana'  : self.currency_id.with_context(date=self.invoice_date).compute((line.price_unit * line.quantity) / line.cce_quantity, currency_usd),
            #              'ValorDolares'         : self.currency_id.with_context(date=self.invoice_date).compute(line.price_unit * line.quantity, currency_usd)+valor_dolares,
            #             }
            #            }
            # if line.product_id.sat_marca:
            #     concepto['cce11:Mercancia'].update({'cce11:DescripcionesEspecificas':{
            #         'xmlns' : 'http://www.sat.gob.mx/ComercioExterior', 
            #         'Marca' : line.product_id.sat_marca}})
            #     if line.product_id.sat_modelo:
            #         concepto['cce11:Mercancia']['cce11:DescripcionesEspecificas'].update({'Modelo':line.product_id.sat_modelo})
            #         if line.product_id.sat_submodelo:
            #             concepto['cce11:Mercancia']['cce11:DescripcionesEspecificas'].update({'SubModelo':line.product_id.sat_submodelo})    

            # complemento['cce11:ComercioExterior']['cce11:Mercancias'].append(concepto)
    
        for groupline in group_to_ce_mercancia:
            line_mercancia = group_to_ce_mercancia[groupline]
            cantidad_aduana_final = line_mercancia['CantidadAduana']
            valor_dolares_final =  line_mercancia['ValorDolares']
            valor_unitario_aduana_final = float(valor_dolares_final) / float(cantidad_aduana_final)
            line_mercancia.update({'CantidadAduana':"%.2f" % cantidad_aduana_final,
                                    'ValorDolares': round(valor_dolares_final,2),
                                    'ValorUnitarioAduana': round(valor_unitario_aduana_final,2),
                                    })
            product_br = groupline
            concepto = {'cce11:Mercancia':
                        line_mercancia
                       }
            if product_br.sat_marca:
                concepto['cce11:Mercancia'].update({'cce11:DescripcionesEspecificas':{
                    'xmlns' : 'http://www.sat.gob.mx/ComercioExterior', 
                    'Marca' : product_br.sat_marca}})
                if product_br.sat_modelo:
                    concepto['cce11:Mercancia']['cce11:DescripcionesEspecificas'].update({'Modelo':product_br.sat_modelo})
                    if product_br.sat_submodelo:
                        concepto['cce11:Mercancia']['cce11:DescripcionesEspecificas'].update({'SubModelo':product_br.sat_submodelo})    

            complemento['cce11:ComercioExterior']['cce11:Mercancias'].append(concepto)
        
        comprobante['cfdi:Comprobante'].update({'cfdi:Complemento':complemento})
        #print "================================================="
        #print "comprobante: \n",comprobante
        #print "================================================="
        return comprobante
    