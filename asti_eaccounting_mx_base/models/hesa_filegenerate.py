# -*- encoding: utf-8 -*-
#

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from lxml import etree as et
import base64

class hesa_trialbalance_inherit(models.Model):
    _inherit = 'account.monthly_balance'

    def launch_xml_generator(self):
        if not len(self._context['active_ids']):
            raise UserError(_('Archivo vacío\n\nNo se ha seleccionado ninguna partida en la balanza.'))
        return {'type'      : 'ir.actions.act_window',
                 'res_model': 'hesa.filegenerate',
                 'view_mode': 'form',
                 'view_type': 'form',
                 'name'     : 'Parámetros para la Balanza Mensual',
                 'target'   : 'new',
                 'context'  : self._context
               }


hesa_trialbalance_inherit()

class hesa_filegenerate(models.TransientModel):
    _name = 'hesa.filegenerate'
    _description = "Wizard para generar Balanza Mensual"

    trial_delivery        = fields.Selection([('N', 'Normal'), 
                                              ('C', 'Complementario')], default='N',
                                             string='Tipo de envío', required=True)
    trial_lastchange_date = fields.Date('Última modificación contable')

    def generate_file(self):
        recs = self.env['account.monthly_balance'].browse(self._context['active_ids'])
        period_id = recs[0].period_id
        chart = False
        for line in recs:
            if not line.account_id.parent_id:
                chart = line.account_id.id
        if not chart:
            chart = self.env['account.account'].search([('parent_id', '=', False)], limit=1).id
        wizard_vals = { 'xml_target': 'trial_balance',
                        'month'     : period_id.date_start[5:7],
                        'year'      : int(period_id.date_start[0:4]),
                        'trial_delivery': self.trial_delivery,
                        'trial_lastchange_date': self.trial_lastchange_date,
                        'accounts_chart': chart
                      }
        wizId = self.env['files.generator.wizard'].create(wizard_vals)
        return wizId.process_file(balance_ids=self._context['active_ids'])



hesa_filegenerate()

