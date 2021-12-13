# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero

class InfoReporte(models.AbstractModel):
    
    _name = "x_tire_loading_info.x_tire_loading_info_card"

    @api.model
    def _get_report_values(self, docids, data=None):
        report_obj = self.env['ir.actions.report']
        report = report_obj._get_report_from_name('x_tire_loading_info.x_tire_loading_info_card')
        return{
            'doc_ids': docids,
            'doc_model': self.env['studio_customization.x_tire_loading_info'],
            'docs': self.env['studio_customization.x_tire_loading_info'].browse(docids)
        }


