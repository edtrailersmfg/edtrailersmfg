# -*- encoding: utf-8 -*-

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from lxml import etree as et
import xmltodict
import base64
from xml.dom.minidom import parse, parseString
import requests
import logging
_logger = logging.getLogger(__name__)

def create_list_html(data):
    if not data:
        return ''
    msg = ''    
    for x in data.keys():
        if 'xmlns' not in x:
            msg += "<li>%s : %s</li>" % (x.replace('a:',''), data[x])
    return '<ul>' + msg + '</ul>'


class AccountInvoice(models.Model):
    _inherit = 'account.move'

    foreign_invoice      = fields.Char(string='No. factura extranjera', size=36, readonly=True, states={'draft': [('readonly', False)]})
    validate_attachment  = fields.Boolean(string='Validar sin XML', tracking=True,
                                         help='Active esta casilla cuando quiera validar una factura sin haber adjuntado el archivo XML del CFDI')
    validate_attachment2 = fields.Boolean(string='Sin Validar en SAT', tracking=True,
                                         help='Active esta casilla cuando quiera validar una factura cuyo CFDI no se encuentre vigente en el SAT')
    
    
    def do_something_with_xml_attachment(self, attach):
        self.ensure_one()
        res = super(AccountInvoice, self).do_something_with_xml_attachment(attach)
        line_id = [ ln.id for ln in self.line_ids if ln.account_id.internal_type in ("payable", "receivable") ]
        if len(line_id):
            cmplObj = self.env['eaccount.complements']
            cmpl_vals = cmplObj.onchange_attached(attachment=attach.datas, currency_id=self.currency_id)['value']
            cmpl_vals['type_id'] = self.env['eaccount.complement.types'].search([('key', '=', 'cfdi')], limit=1).id
            cmpl_vals['type_key'] = 'cfdi'
            cmpl_vals['move_line_id'] = line_id[0]
            cmpl_vals['file_data'] = base64.decodebytes(attach.datas)
            cmplObj.create(cmpl_vals)            
            self.write({'item_concept': self.env.user.company_id._assembly_concept(self.move_type, invoice=self)})
        return res
    
    
    # def action_move_create(self):
    #     """
    #     ### Codigo para validar si es Ingreso Credito o de Contado
    #     for invoice in self:
    #         if not invoice.amount_total:
    #             continue
    #         payment_term_obj = self.env['account.payment.term']
    #         inv_line_obj = self.env['account.invoice.line']
    #         if invoice.type == 'out_invoice':
    #             for line in invoice.invoice_line_ids:
    #                 # Validacion para contabilizar Ingreso a Credito o Contado (segun tenga configurada la cuenta la categoria del producto y/o el producto)
    #                 if line.product_id and line.account_id.id in (line.product_id.property_account_income_id.id, line.product_id.property_account_income_id2.id,line.product_id.categ_id.property_account_income_categ_id.id,line.product_id.categ_id.property_account_income_categ_id2.id):
    #                     new_account = bool(invoice.date_invoice == invoice.date_due) and \
    #                                       (line.product_id.property_account_income_id2.id or line.product_id.categ_id.property_account_income_categ_id2.id) or \
    #                                       (line.product_id.property_account_income_id.id or line.product_id.categ_id.property_account_income_categ_id.id)
    #                     if new_account and line.account_id.id != new_account:
    #                         line.write({'account_id': new_account})
    #     ### Fin de Codigo para validar si es Ingreso Credito o de Contado
    #     """
    #     # Continuación código original
    #     cmplsObj = self.env['eaccount.complements']
    #     compl_type_id = self.env['eaccount.complement.types'].search([('key', '=', 'foreign')], limit=1)
    #     res = super(AccountInvoice, self).action_move_create()
    #     company = self.env.user.company_id
    #     if not company.auto_mode_enabled:
    #         return True
    #     for inv in self:
    #         if not inv.amount_total:
    #             continue
    #         line_id = []
    #         if inv.type not in ('in_invoice', 'in_refund'):
    #             continue
    #         if inv.type == 'in_invoice':
    #             line_id = [ ln.id for ln in inv.move_id.line_ids if ln.account_id.internal_type == 'payable' ]
    #             msg = u'No se encontró ningún asiento con una cuenta de tipo "A pagar" en la póliza %s' % inv.move_id.name
    #         else:
    #             line_id = [ ln.id for ln in inv.move_id.line_ids ]
    #             msg = u'No se encontraron asientos en la poliza %s' % str(inv.move_id.name)
    #         if not line_id:
    #             msg = u'No se encontraron asientos en la poliza %s' % str(inv.move_id.name)
    #             raise UserError(_('Información faltante\n\n %s') % (msg))
    #         cmpl_vals = {}
    #         xpartner = inv.partner_id.parent_id or inv.partner_id
    #         if xpartner.type_of_third == '05' and not xpartner.number_fiscal_id_diot:
    #             raise UserError(_('Información faltante\n\nSe necesita un ID fiscal para el complemento a extranjeros, verifique la configuración de la DIOT para este proveedor.'))
    #         cmpl_vals['foreign_taxid'] = xpartner.number_fiscal_id_diot
    #         cmpl_vals['foreign_invoice'] = inv.reference
    #         if cmpl_vals['foreign_taxid'] and cmpl_vals['foreign_invoice']:
    #             cmpl_vals.update({'amount'          : inv.amount_total,
    #                              'compl_date'       : inv.invoice_date,
    #                              'compl_currency_id': inv.currency_id.id,
    #                              'type_key'         : 'foreign',
    #                              'type_id'          : compl_type_id.id,
    #                              'move_line_id'     : line_id[0]
    #                              })
    #             curr_rate = False
    #             rate_lines = [ rate for rate in inv.currency_id.rate_ids if rate.name == inv.invoice_date ]
    #             if len(rate_lines) and rate_lines[0].rate:
    #                 curr_rate = 1 / rate_lines[0].rate
    #             else:
    #                 rate_lines = [{'name':val.name,'rate':val.rate} for val in inv.currency_id.rate_ids]
    #                 #rate_lines = sorted(rate_lines, reverse=True)
    #                 for ln in rate_lines:
    #                     if ln['name'] < inv.invoice_date and ln['rate']:
    #                         curr_rate = 1 / ln['rate']
    #                         break
                    
    #                 #inv.currency_id.rate_ids = sorted(inv.currency_id.rate_ids, key=lambda k: k.name, reverse=True)
    #                 #for ln in inv.currency_id.rate_ids:
    #                 #    if ln.name < inv.date_invoice and ln.rate:
    #                 #        curr_rate = 1 / ln.rate
    #                 #        break

    #             cmpl_vals['exchange_rate'] = str(curr_rate) if curr_rate else False
    #             compl_rec = cmplsObj.create(cmpl_vals)
    #         else:
    #             attachment = self.env['ir.attachment'].search([('name', 'ilike', '.xml'), ('res_model', '=', 'account.move'), ('res_id', '=', inv.id)], limit=1)
    #             if attachment:
    #                 cmplObj = self.env['eaccount.complements']
    #                 user = self.env.user
    #                 cmpl_vals = cmplObj.onchange_attached(attachment=attachment.datas, currency_id=inv.currency_id)['value']
    #                 if not xpartner.vat:
    #                     raise UserError(_('Información faltante\n\nEl proveedor %s no tiene configurado un R.F.C.') % xpartner.name)
    #                 partner_vat = xpartner.vat[2:] if len(xpartner.vat) > 13 else xpartner.vat
    #                 if xpartner.type_of_third == '04' and partner_vat != cmpl_vals['rfc']:
    #                     raise UserError(_('Inconsistencia de datos.\n\nEl RFC emisor ("%s") no coincide con el RFC del proveedor ("%s")') % (cmpl_vals['rfc'], partner_vat))
    #                 if user.company_id.partner_id.vat != cmpl_vals['rfc2']:
    #                     raise UserError(_('Inconsistencia de datos\n\nEl RFC receptor ("%s") no coincide con el RFC de la empresa ("%s")') % (cmpl_vals['rfc2'], user.company_id.partner_id.vat))
    #                 parameter = float(self.env['ir.config_parameter'].get_param('argil_tolerance_range_between_invoice_record_and_cfdi_xml_file')) or 0
    #                 low = inv.amount_total - parameter
    #                 upp = inv.amount_total + parameter
    #                 if not low < cmpl_vals['amount'] < upp:
    #                     raise UserError(_('Inconsistencia de datos\n\nEl total del XML (%f) está fuera del rango de tolerancia de +/- %f') % (cmpl_vals['amount'], parameter))
    #                 cmpl_vals['type_id'] = self.env['eaccount.complement.types'].search([('key', '=', 'cfdi')], limit=1).id
    #                 cmpl_vals['type_key'] = 'cfdi'
    #                 cmpl_vals['move_line_id'] = line_id[0]
    #                 cmplObj.create(cmpl_vals)
                        
    #         inv.move_id.write({'item_concept': company._assembly_concept(inv.type, invoice=inv)})
        # return True
                                

    def action_post(self):
        cmplsObj = self.env['eaccount.complements']
        compl_type_id = self.env['eaccount.complement.types'].search([('key', '=', 'foreign')], limit=1)
        company = self.env.user.company_id

        result = super(AccountInvoice, self).action_post()
        for rec in self:
            if rec.move_type in ('in_invoice','in_refund'):
                type_of_third = rec.partner_id.type_of_third
                if rec.partner_id.parent_id:
                    type_of_third = rec.partner_id.parent_id.type_of_third
                if rec.validate_attachment == False and type_of_third in ('04','15'):
                    
                    attachment_xml_ids = self.env['ir.attachment'].search([('res_model', '=', 'account.move'), 
                                                                           ('res_id', '=', rec.id), 
                                                                           ('name', 'ilike', '.xml')], limit=1)
                    if not attachment_xml_ids:
                        raise UserError(_('No Puede Validar la Factura o Nota de Credito sin el archivo XML del CFDI...'))
                    elif attachment_xml_ids and not rec.validate_attachment2:
                        uuid = False
                        #-------------
                        body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/"><soapenv:Header/><soapenv:Body><tem:Consulta><!--Optional:--><tem:expresionImpresa><![CDATA[?re={0}&rr={1}&tt={2}&id={3}]]></tem:expresionImpresa></tem:Consulta></soapenv:Body></soapenv:Envelope>
                        """
                        url = 'https://consultaqr.facturaelectronica.sat.gob.mx/ConsultaCFDIService.svc?wsdl'
                        headers = {'Content-type': 'text/xml;charset="utf-8"', 
                                   'Accept' : 'text/xml', 
                                   'SOAPAction': 'http://tempuri.org/IConsultaCFDIService/Consulta'}
                        #-------------
                        for att in attachment_xml_ids:
                            xml_data = base64.b64decode(att.datas).replace(b'http://www.sat.gob.mx/registrofiscal ', b'').replace(b'http://www.sat.gob.mx/cfd/3 ', b'').replace(b'Rfc=',b'rfc=').replace(b'Fecha=',b'fecha=').replace(b'Total=',b'total=').replace(b'Folio=',b'folio=').replace(b'Serie=',b'serie=')
                            result, res = False, False
                            estado_cfdi = ''
                            try:
                                xmlTree = et.ElementTree(et.fromstring(xml_data))
                                vouchNode = xmlTree.getroot()
                                uuid = vouchNode.find('{http://www.sat.gob.mx/cfd/3}Complemento').find('{http://www.sat.gob.mx/TimbreFiscalDigital}TimbreFiscalDigital').attrib['UUID'].upper()
                                
                                rfc_emisor = vouchNode.find('{http://www.sat.gob.mx/cfd/3}Emisor').attrib['rfc'].upper()
                                rfc_emisor = rfc_emisor.replace('&','&amp;')
                                rfc_emisor = rfc_emisor.replace('<','&lt;')
                                rfc_emisor = rfc_emisor.replace('>','&gt;')

                                rfc_receptor = vouchNode.find('{http://www.sat.gob.mx/cfd/3}Receptor').attrib['rfc'].upper()
                                rfc_receptor = rfc_receptor.replace('&','&amp;')
                                rfc_receptor = rfc_receptor.replace('<','&lt;')
                                rfc_receptor = rfc_receptor.replace('>','&gt;')
                                
                                monto_total = float(vouchNode.attrib['total'])
                                #-------------
                                bodyx = body.format(rfc_emisor, rfc_receptor, monto_total, uuid)
                                result = requests.post(url=url, headers=headers, data=bodyx)
                                res = xmltodict.parse(result.text)
                                if result.status_code == 200:
                                    estado_cfdi = res['s:Envelope']['s:Body']['ConsultaResponse']['ConsultaResult']['a:Estado']
                                else:
                                    raise UserError(_('No Puede Validar la Factura o Nota de Credito, error en la llamada al WebService del SAT: .\n\n'
                                          'Codigo Estatus: %s\n'
                                          'Folio Fiscal: %s\n'
                                          'RFC Emisor: %s\n'
                                          'RFC Receptor: %s\n'
                                          'Monto Total: %d') % (result.status_code, uuid, rfc_emisor, rfc_receptor, monto_total))
                                #-------------
                            except:
                                continue
                            
                            if estado_cfdi != 'Vigente':
                                raise UserError(
                                        _('No Puede Validar la Factura o Nota de Credito, el SAT devolvió lo siguiente: .\n\n'
                                          'Codigo Estatus: %s\n'
                                          'Resultado Webservice: %s\n'
                                          'Estado: %s\n\n'
                                          'Folio Fiscal: %s\n'
                                          'RFC Emisor: %s\n'
                                          'RFC Receptor: %s\n'
                                          'Monto Total: %d') % (result.status_code, res and create_list_html(res['s:Envelope']['s:Body']['ConsultaResponse']['ConsultaResult']) or '', estado_cfdi, uuid, rfc_emisor, rfc_receptor, monto_total))
                        if not uuid:
                            raise UserError(_('Formato de archivo XML incorrecto\n\nSe necesita cargar un archivo de extensión ".xml" (CFDI)'))
                    
                    rec.message_post(body=_("La factura (XML) adjunta se encuentra Vigente en el SAT\n%s") % (res and create_list_html(res['s:Envelope']['s:Body']['ConsultaResponse']['ConsultaResult']) or ''))
        if not company.auto_mode_enabled:
            return result
        ############## Creando los Complementos ########
        for inv in self:
            if not inv.amount_total:
                continue
            line_id = []
            if inv.move_type not in ('in_invoice', 'in_refund'):
                continue
            if inv.move_type == 'in_invoice':
                line_id = [ ln.id for ln in inv.line_ids if ln.account_id.internal_type == 'payable' ]
                msg = u'No se encontró ningún asiento con una cuenta de tipo "A pagar" en la póliza %s' % inv.name
            else:
                line_id = [ ln.id for ln in inv.line_ids ]
                msg = u'No se encontraron asientos en la poliza %s' % str(inv.name)
            if not line_id:
                msg = u'No se encontraron asientos en la poliza %s' % str(inv.name)
                raise UserError(_('Información faltante\n\n %s') % (msg))
            cmpl_vals = {}
            xpartner = inv.partner_id.parent_id or inv.partner_id
            if xpartner.type_of_third == '05' and not xpartner.number_fiscal_id_diot:
                raise UserError(_('Información faltante\n\nSe necesita un ID fiscal para el complemento a extranjeros, verifique la configuración de la DIOT para este proveedor.'))
            cmpl_vals['foreign_taxid'] = xpartner.number_fiscal_id_diot
            cmpl_vals['foreign_invoice'] = inv.ref
            if cmpl_vals['foreign_taxid'] and cmpl_vals['foreign_invoice']:
                cmpl_vals.update({'amount'          : inv.amount_total,
                                 'compl_date'       : inv.invoice_date,
                                 'compl_currency_id': inv.currency_id.id,
                                 'type_key'         : 'foreign',
                                 'type_id'          : compl_type_id.id,
                                 'move_line_id'     : line_id[0]
                                 })
                curr_rate = False
                rate_lines = [ rate for rate in inv.currency_id.rate_ids if rate.name == inv.invoice_date ]
                if len(rate_lines) and rate_lines[0].rate:
                    curr_rate = 1 / rate_lines[0].rate
                else:
                    rate_lines = [{'name':val.name,'rate':val.rate} for val in inv.currency_id.rate_ids]
                    #rate_lines = sorted(rate_lines, reverse=True)
                    for ln in rate_lines:
                        if ln['name'] < inv.invoice_date and ln['rate']:
                            curr_rate = 1 / ln['rate']
                            break
                    
                    #inv.currency_id.rate_ids = sorted(inv.currency_id.rate_ids, key=lambda k: k.name, reverse=True)
                    #for ln in inv.currency_id.rate_ids:
                    #    if ln.name < inv.date_invoice and ln.rate:
                    #        curr_rate = 1 / ln.rate
                    #        break

                cmpl_vals['exchange_rate'] = str(curr_rate) if curr_rate else False
                compl_rec = cmplsObj.create(cmpl_vals)
            else:
                attachment = self.env['ir.attachment'].search([('name', 'ilike', '.xml'), ('res_model', '=', 'account.move'), ('res_id', '=', inv.id)], limit=1)
                if attachment:
                    cmplObj = self.env['eaccount.complements']
                    user = self.env.user
                    cmpl_vals = cmplObj.onchange_attached(attachment=attachment.datas, currency_id=inv.currency_id)['value']
                    if not xpartner.vat:
                        raise UserError(_('Información faltante\n\nEl proveedor %s no tiene configurado un R.F.C.') % xpartner.name)
                    partner_vat = xpartner.vat[2:] if len(xpartner.vat) > 13 else xpartner.vat
                    if xpartner.type_of_third == '04' and partner_vat != cmpl_vals['rfc']:
                        raise UserError(_('Inconsistencia de datos.\n\nEl RFC emisor ("%s") no coincide con el RFC del proveedor ("%s")') % (cmpl_vals['rfc'], partner_vat))
                    #if user.company_id.partner_id.vat != cmpl_vals['rfc2']:
                    if inv.company_id.partner_id.vat != cmpl_vals['rfc2']:
                        raise UserError(_('Inconsistencia de datos\n\nEl RFC receptor ("%s") no coincide con el RFC de la empresa ("%s")') % (cmpl_vals['rfc2'], user.company_id.partner_id.vat))
                    parameter = float(self.env['ir.config_parameter'].get_param('argil_tolerance_range_between_invoice_record_and_cfdi_xml_file')) or 0
                    low = inv.amount_total - parameter
                    upp = inv.amount_total + parameter
                    if not low < cmpl_vals['amount'] < upp:
                        raise UserError(_('Inconsistencia de datos\n\nEl total del XML (%f) está fuera del rango de tolerancia de +/- %f') % (cmpl_vals['amount'], parameter))
                    cmpl_vals['type_id'] = self.env['eaccount.complement.types'].search([('key', '=', 'cfdi')], limit=1).id
                    cmpl_vals['type_key'] = 'cfdi'
                    cmpl_vals['move_line_id'] = line_id[0]
                    cmplObj.create(cmpl_vals)
                        
            inv.write({'item_concept': company._assembly_concept(inv.move_type, invoice=inv)})

        return result


