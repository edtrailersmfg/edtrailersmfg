# -*- coding:utf-8 -*-
from odoo import fields, models, api


class MrpRepairCauses(models.Model):
    _name = 'mrp.repair.causes'

    code = fields.Char('Código')
    descrip = fields.Char('Descripción')

    @api.multi
    def name_get(self):
        res = []
        for record in self:
            display = '[%s] - %s' % (
                record.code or '', record.descrip
            )
            res.append((record.id, display))

        return res

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if name:
            filtro = ['|', ('code', 'ilike', name), ('descrip', 'ilike', name)]
            recs = self.search(filtro, limit=limit)
            
        return recs.name_get()